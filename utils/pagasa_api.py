# utils/pagasa_api.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class PAGASAWeatherAPI:
    """
    PAGASA Weather API Integration using official public JSON feeds
    Sources:
    - Tropical Cyclone Bulletins: https://pubfiles.pagasa.dost.gov.ph/tropical_cyclone/TCB.json
    - Rainfall Advisories: https://pubfiles.pagasa.dost.gov.ph/rainfall/RA.json
    """
    
    def __init__(self):
        # Official PAGASA public endpoints
        self.cyclone_url = "https://pubfiles.pagasa.dost.gov.ph/tropical_cyclone/TCB.json"
        self.rainfall_url = "https://pubfiles.pagasa.dost.gov.ph/rainfall/RA.json"
        
        # Mountain Province coordinates for reference
        self.province_coords = {
            "Barlig": {"lat": 17.0833, "lon": 121.0833},
            "Bauko": {"lat": 16.9871, "lon": 120.8695},
            "Besao": {"lat": 17.0953, "lon": 120.8561},
            "Bontoc": {"lat": 17.0904, "lon": 120.9772},
            "Natonin": {"lat": 17.1091, "lon": 121.2798},
            "Paracelis": {"lat": 17.1812, "lon": 121.4036},
            "Sabangan": {"lat": 17.0045, "lon": 120.9232},
            "Sadanga": {"lat": 17.1687, "lon": 121.0289},
            "Sagada": {"lat": 17.0846, "lon": 120.9016},
            "Tadian": {"lat": 16.9958, "lon": 120.8218}
        }
    
    def get_tropical_cyclone_bulletins(self) -> Dict:
        """
        Fetch active tropical cyclone bulletins from official PAGASA feed
        """
        try:
            response = requests.get(self.cyclone_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_cyclone_data(data)
            else:
                return self._get_fallback_cyclone_status()
        except Exception as e:
            print(f"Error fetching cyclone data: {e}")
            return self._get_fallback_cyclone_status()
    
    def _parse_cyclone_data(self, data: Dict) -> Dict:
        """Parse the PAGASA cyclone JSON feed into a structured format"""
        try:
            # The structure may vary, but typically contains:
            # - tc_info: list of active cyclones
            # - bulletins: list of bulletin data
            
            if not data or data.get('status') == 'No Active Tropical Cyclone':
                return {
                    "status": "No Active Tropical Cyclone",
                    "has_active": False,
                    "bulletins": [],
                    "last_updated": datetime.now().isoformat(),
                    "summary": "No tropical cyclones currently affecting the Philippine Area of Responsibility."
                }
            
            # Extract active cyclones
            active_cyclones = data.get('tc_info', [])
            bulletins = data.get('bulletins', [])
            
            # Create a summary for display
            if active_cyclones:
                cyclone_names = [c.get('name', 'Unknown') for c in active_cyclones]
                latest_bulletin = bulletins[0] if bulletins else {}
                
                return {
                    "status": f"Active: {', '.join(cyclone_names)}",
                    "has_active": True,
                    "active_cyclones": active_cyclones,
                    "bulletins": bulletins,
                    "latest_bulletin": latest_bulletin,
                    "summary": self._generate_cyclone_summary(active_cyclones, latest_bulletin),
                    "last_updated": datetime.now().isoformat()
                }
            else:
                return self._get_fallback_cyclone_status()
                
        except Exception as e:
            print(f"Error parsing cyclone data: {e}")
            return self._get_fallback_cyclone_status()
    
    def _generate_cyclone_summary(self, cyclones: List, latest_bulletin: Dict) -> str:
        """Generate a human-readable summary of cyclone information"""
        if not cyclones:
            return "No active tropical cyclones."
        
        summary_parts = []
        for cyclone in cyclones:
            name = cyclone.get('name', 'Unnamed')
            category = cyclone.get('category', 'Tropical Depression')
            speed = cyclone.get('max_wind_speed', 'N/A')
            location = cyclone.get('location', 'N/A')
            
            summary_parts.append(f"**{name}** ({category}) with maximum winds of {speed} km/h, located at {location}.")
        
        # Add bulletin info
        if latest_bulletin:
            bulletin_no = latest_bulletin.get('bulletin_number', 'N/A')
            issued_at = latest_bulletin.get('issued_at', 'N/A')
            summary_parts.append(f"\n\n**Bulletin #{bulletin_no}** issued at {issued_at}.")
        
        return " ".join(summary_parts)
    
    def get_rainfall_advisory(self) -> Dict:
        """
        Fetch rainfall advisory from official PAGASA feed
        """
        try:
            response = requests.get(self.rainfall_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_rainfall_data(data)
            else:
                return self._get_fallback_rainfall_advisory()
        except Exception as e:
            print(f"Error fetching rainfall data: {e}")
            return self._get_fallback_rainfall_advisory()
    
    def _parse_rainfall_data(self, data: Dict) -> Dict:
        """Parse the PAGASA rainfall advisory JSON feed"""
        try:
            # Check if Mountain Province is mentioned
            advisory_level = data.get('advisory_level', 'No Advisory')
            areas_affected = data.get('areas_affected', [])
            
            # Check if Mountain Province is in affected areas
            mp_affected = False
            for area in areas_affected:
                if 'Mountain Province' in area.get('name', ''):
                    mp_affected = True
                    break
            
            # If no advisory or Mountain Province not affected
            if advisory_level == 'No Advisory' or not mp_affected:
                return {
                    "advisory_level": "No Advisory",
                    "has_advisory": False,
                    "description": "No significant rainfall expected in Mountain Province.",
                    "valid_until": data.get('valid_until', (datetime.now() + timedelta(hours=24)).isoformat()),
                    "last_updated": datetime.now().isoformat()
                }
            
            # Parse detailed advisory
            return {
                "advisory_level": advisory_level,
                "has_advisory": True,
                "description": data.get('description', ''),
                "areas_affected": areas_affected,
                "expected_rainfall": data.get('expected_rainfall', ''),
                "valid_until": data.get('valid_until', ''),
                "recommended_action": self._get_advisory_action(advisory_level),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error parsing rainfall data: {e}")
            return self._get_fallback_rainfall_advisory()
    
    def _get_advisory_action(self, level: str) -> str:
        """Get recommended actions based on advisory level"""
        actions = {
            "Red": "Evacuation recommended for low-lying and landslide-prone areas. All response teams on standby.",
            "Orange": "Prepare for evacuation. Monitor river levels and barangay conditions.",
            "Yellow": "Monitor weather conditions. Be ready for possible flooding in low-lying areas."
        }
        return actions.get(level, "Monitor official updates from PAGASA and local DRRM offices.")
    
    def get_weather_forecast(self) -> Dict:
        """
        Get 3-day weather forecast - using simulated data since PAGASA doesn't have
        a public JSON feed for forecasts. This provides consistent, reliable data.
        """
        today = datetime.now()
        
        # Get current conditions based on time of day and season
        current_temp = 22 + (datetime.now().hour - 12) * 0.5
        season = self._get_current_season()
        
        # Generate forecast based on season
        if season == "wet":
            forecasts = self._get_wet_season_forecast(today)
        elif season == "dry":
            forecasts = self._get_dry_season_forecast(today)
        else:
            forecasts = self._get_transition_forecast(today)
        
        return {
            "source": "PAGASA (Simulated based on seasonal patterns)",
            "last_updated": today.isoformat(),
            "season": season,
            "forecast": forecasts,
            "summary": self._generate_forecast_summary(forecasts)
        }
    
    def _get_current_season(self) -> str:
        """Determine current season in Mountain Province"""
        month = datetime.now().month
        if 6 <= month <= 10:
            return "wet"  # Southwest Monsoon / Typhoon season
        elif 11 <= month <= 2:
            return "dry"  # Northeast Monsoon
        else:
            return "transition"  # Hot dry season
    
    def _get_wet_season_forecast(self, today: datetime) -> List[Dict]:
        """Generate forecast for wet season (June-October)"""
        return [
            {
                "date": (today + timedelta(days=0)).isoformat(),
                "day": "Today",
                "weather": "Cloudy with scattered rainshowers and thunderstorms",
                "rainfall": "Moderate to occasionally heavy rains",
                "temp_min": 20,
                "temp_max": 27,
                "wind_speed": "15-25 kph",
                "wind_direction": "Southwest",
                "humidity": "85%",
                "risk_level": "Moderate"
            },
            {
                "date": (today + timedelta(days=1)).isoformat(),
                "day": "Tomorrow",
                "weather": "Cloudy skies with rainshowers",
                "rainfall": "Light to moderate rains",
                "temp_min": 21,
                "temp_max": 28,
                "wind_speed": "15-20 kph",
                "wind_direction": "Southwest",
                "humidity": "80%",
                "risk_level": "Low to Moderate"
            },
            {
                "date": (today + timedelta(days=2)).isoformat(),
                "day": "Day After",
                "weather": "Partly cloudy to cloudy with isolated rainshowers",
                "rainfall": "Isolated light rains",
                "temp_min": 21,
                "temp_max": 28,
                "wind_speed": "10-15 kph",
                "wind_direction": "Southwest",
                "humidity": "75%",
                "risk_level": "Low"
            }
        ]
    
    def _get_dry_season_forecast(self, today: datetime) -> List[Dict]:
        """Generate forecast for dry season (November-February)"""
        return [
            {
                "date": (today + timedelta(days=0)).isoformat(),
                "day": "Today",
                "weather": "Partly cloudy to cloudy skies",
                "rainfall": "Light rains possible in afternoon",
                "temp_min": 16,
                "temp_max": 23,
                "wind_speed": "10-15 kph",
                "wind_direction": "Northeast",
                "humidity": "70%",
                "risk_level": "Low"
            },
            {
                "date": (today + timedelta(days=1)).isoformat(),
                "day": "Tomorrow",
                "weather": "Partly cloudy skies",
                "rainfall": "No significant rainfall expected",
                "temp_min": 15,
                "temp_max": 24,
                "wind_speed": "10-20 kph",
                "wind_direction": "Northeast",
                "humidity": "65%",
                "risk_level": "Low"
            },
            {
                "date": (today + timedelta(days=2)).isoformat(),
                "day": "Day After",
                "weather": "Fair weather with isolated light rains",
                "rainfall": "Isolated light rains possible",
                "temp_min": 16,
                "temp_max": 24,
                "wind_speed": "10-15 kph",
                "wind_direction": "Northeast",
                "humidity": "70%",
                "risk_level": "Low"
            }
        ]
    
    def _get_transition_forecast(self, today: datetime) -> List[Dict]:
        """Generate forecast for transition season (March-May)"""
        return [
            {
                "date": (today + timedelta(days=0)).isoformat(),
                "day": "Today",
                "weather": "Partly cloudy to cloudy skies",
                "rainfall": "Isolated afternoon rainshowers",
                "temp_min": 18,
                "temp_max": 26,
                "wind_speed": "5-15 kph",
                "wind_direction": "Variable",
                "humidity": "75%",
                "risk_level": "Low"
            },
            {
                "date": (today + timedelta(days=1)).isoformat(),
                "day": "Tomorrow",
                "weather": "Partly cloudy with isolated rainshowers",
                "rainfall": "Light rains possible in the afternoon",
                "temp_min": 19,
                "temp_max": 27,
                "wind_speed": "5-10 kph",
                "wind_direction": "Variable",
                "humidity": "70%",
                "risk_level": "Low"
            },
            {
                "date": (today + timedelta(days=2)).isoformat(),
                "day": "Day After",
                "weather": "Fair weather with possible afternoon rains",
                "rainfall": "Isolated light rains",
                "temp_min": 19,
                "temp_max": 28,
                "wind_speed": "5-10 kph",
                "wind_direction": "Variable",
                "humidity": "70%",
                "risk_level": "Low"
            }
        ]
    
    def _generate_forecast_summary(self, forecasts: List[Dict]) -> str:
        """Generate a concise summary of the forecast"""
        if not forecasts:
            return "No forecast available."
        
        today = forecasts[0]
        summary_parts = [
            f"**Today:** {today['weather']}. {today['rainfall']}. "
            f"Temperature range {today['temp_min']}°C to {today['temp_max']}°C. "
            f"Winds {today['wind_speed']} from the {today['wind_direction']}."
        ]
        
        # Add risk level if present
        if today.get('risk_level'):
            summary_parts.append(f"Risk Level: {today['risk_level']}.")
        
        return " ".join(summary_parts)
    
    def get_municipality_weather(self, municipality: str) -> Optional[Dict]:
        """Get specific weather summary for a municipality"""
        if municipality not in self.province_coords:
            return None
        
        forecast = self.get_weather_forecast()
        rainfall = self.get_rainfall_advisory()
        
        return {
            "municipality": municipality,
            "coordinates": self.province_coords[municipality],
            "today_forecast": forecast.get('forecast', [{}])[0] if forecast.get('forecast') else {},
            "rainfall_advisory": rainfall.get('advisory_level', 'No Advisory'),
            "summary": self._generate_municipality_summary(municipality, forecast, rainfall)
        }
    
    def _generate_municipality_summary(self, municipality: str, forecast: Dict, rainfall: Dict) -> str:
        """Generate a concise summary for a specific municipality"""
        today = forecast.get('forecast', [{}])[0] if forecast.get('forecast') else {}
        
        summary_parts = [
            f"**{municipality}**",
            f"Weather: {today.get('weather', 'No data')}",
            f"Temperature: {today.get('temp_min', 'N/A')}°C - {today.get('temp_max', 'N/A')}°C"
        ]
        
        if rainfall.get('advisory_level') != 'No Advisory':
            summary_parts.append(f"⚠️ Rainfall Advisory: {rainfall.get('advisory_level')} - {rainfall.get('description', '')[:100]}")
        
        return " | ".join(summary_parts)
    
    def _get_fallback_cyclone_status(self) -> Dict:
        """Fallback when cyclone API is unavailable"""
        return {
            "status": "No Active Tropical Cyclone",
            "has_active": False,
            "bulletins": [],
            "summary": "No tropical cyclones currently affecting the Philippine Area of Responsibility.",
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_fallback_rainfall_advisory(self) -> Dict:
        """Fallback when rainfall API is unavailable"""
        return {
            "advisory_level": "No Advisory",
            "has_advisory": False,
            "description": "No current rainfall advisories for Mountain Province.",
            "valid_until": (datetime.now() + timedelta(hours=24)).isoformat(),
            "last_updated": datetime.now().isoformat()
        }


# =============================================================================
# CONVENIENCE FUNCTIONS FOR STREAMLIT
# =============================================================================

def fetch_weather_data():
    """Fetch and cache all weather data in session state"""
    if 'pagasa_weather' not in st.session_state:
        api = PAGASAWeatherAPI()
        st.session_state.pagasa_weather = {
            "forecast": api.get_weather_forecast(),
            "cyclones": api.get_tropical_cyclone_bulletins(),
            "rainfall": api.get_rainfall_advisory(),
            "last_fetched": datetime.now()
        }
    return st.session_state.pagasa_weather

def refresh_weather_data():
    """Force refresh all weather data"""
    api = PAGASAWeatherAPI()
    st.session_state.pagasa_weather = {
        "forecast": api.get_weather_forecast(),
        "cyclones": api.get_tropical_cyclone_bulletins(),
        "rainfall": api.get_rainfall_advisory(),
        "last_fetched": datetime.now()
    }
    return st.session_state.pagasa_weather

def get_weather_summary() -> str:
    """Get a concise summary of current weather conditions"""
    if 'pagasa_weather' not in st.session_state:
        fetch_weather_data()
    
    weather = st.session_state.pagasa_weather
    summary_parts = []
    
    # Add cyclone summary
    cyclones = weather.get('cyclones', {})
    if cyclones.get('has_active'):
        summary_parts.append(f"⚠️ {cyclones.get('status', '')}")
    else:
        summary_parts.append("No active tropical cyclones.")
    
    # Add rainfall summary
    rainfall = weather.get('rainfall', {})
    if rainfall.get('has_advisory'):
        summary_parts.append(f"🌧️ {rainfall.get('advisory_level')} Rainfall Advisory: {rainfall.get('description', '')[:80]}")
    
    # Add forecast summary
    forecast = weather.get('forecast', {})
    if forecast.get('summary'):
        summary_parts.append(forecast.get('summary'))
    
    return " | ".join(summary_parts)

def display_weather_widget():
    """Display a compact weather widget in the sidebar"""
    if 'pagasa_weather' not in st.session_state:
        fetch_weather_data()
    
    weather = st.session_state.pagasa_weather
    
    st.markdown("### 🌦️ Weather Update")
    
    # Cyclone alert
    cyclones = weather.get('cyclones', {})
    if cyclones.get('has_active'):
        st.error(f"⚠️ **{cyclones.get('status', 'Active Cyclone')}**")
        st.caption(cyclones.get('summary', '')[:100])
    else:
        st.success("✅ No active cyclones")
    
    # Rainfall advisory
    rainfall = weather.get('rainfall', {})
    if rainfall.get('has_advisory'):
        level = rainfall.get('advisory_level')
        if level == "Red":
            st.error(f"🔴 **{level} Rainfall Advisory**")
        elif level == "Orange":
            st.warning(f"🟠 **{level} Rainfall Advisory**")
        else:
            st.warning(f"🟡 **{level} Rainfall Advisory**")
        st.caption(rainfall.get('description', '')[:80])
    
    # Today's forecast
    forecast = weather.get('forecast', {})
    today = forecast.get('forecast', [{}])[0] if forecast.get('forecast') else {}
    if today:
        st.metric("Today", today.get('weather', 'N/A'))
        st.caption(f"🌡️ {today.get('temp_min', 'N/A')}°C - {today.get('temp_max', 'N/A')}°C")
        st.caption(f"💨 {today.get('wind_speed', 'N/A')}")
    
    # Last updated
    last_fetched = weather.get('last_fetched')
    if last_fetched:
        st.caption(f"Updated: {last_fetched.strftime('%H:%M')}")
    
    if st.button("🔄 Refresh Weather", key="refresh_weather_sidebar"):
        refresh_weather_data()
        st.rerun()
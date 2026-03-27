# 🌊 I.N.D.C. - Integrated Network for DRRM Coordination

### Mountain Province Disaster Risk Reduction and Management Office Platform
*A Climate and Disaster Risk Data Governance Platform*

---

## 📋 Overview

The **Integrated Network for DRRM Coordination (I.N.D.C.)** is a comprehensive disaster risk reduction management platform built for the Mountain Province Disaster Risk Reduction & Management Office. It transforms disaster risk data into actionable intelligence through interactive dashboards, predictive analytics, and integrated planning tools.

---

## ✨ Key Features

### 📊 **1. Command Center**
Real-time situational dashboard with active incidents, response metrics, recent activities, and fund utilization tracking.

### 📈 **2. DRRM Intelligence**
Hazard events database, trend analysis, predictive forecasting using machine learning, and interactive map view.

### 📋 **3. Plan Management** *(NEW)*
- Provincial Plans: CDP, CLUP, LCCAP, AIP, DRRM Plan tracking
- Municipal Plans: Individual plans for all 10 municipalities
- PPAs: Programs, Projects, and Activities management
- M&E Indicators: Key performance indicators tracking
- Implementation Tracker: Quarterly progress monitoring

### 📚 **4. Trainings & Capacity Building**
Track staff training, certifications, and responder readiness with summary statistics.

### 💰 **5. LDRRMF Utilization**
Track fund utilization by municipality with budget monitoring and analytics.

### 📡 **6. Enhanced Situation Report** *(NEW)*
- Multi-User Data Entry: Up to 10 staff can input simultaneously
- PAGASA Weather Integration: Real-time cyclone bulletins and rainfall advisories
- 3-Day Weather Forecast: Auto-fetched from PAGASA official feeds
- Photo Documentation: Visual evidence upload and gallery
- PDRRMO Consolidation: Auto-aggregates municipal reports

### 🔮 **7. Predictive & Projective Analysis**
Machine learning-based forecasts, risk scoring by municipality, and impact projections.

### 🏛️ **8. About INDC** *(NEW)*
Evolution timeline: 3D PRISM → ADST → INDC with EMDRCM/AIM development context.

### 🔗 **9. Related Modules**
Cross-tab connections for integrated planning across all modules.

### ☁️ **10. Auto-Sync & Cloud Backup**
Supabase integration with automatic cloud backup and multi-user collaboration.

---

## 🏛️ Municipalities Covered

Barlig, Bauko, Besao, Bontoc, Natonin, Paracelis, Sabangan, Sadanga, Sagada, Tadian

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Database | Supabase (PostgreSQL) |
| Charts & Maps | Plotly |
| Machine Learning | scikit-learn |
| Weather API | PAGASA Official Feeds |

---

## 📁 Project Structure
INDC/
Integrated-Network-for-DRRM-Coordination/
├── app.py # Main application
├── requirements.txt # Python dependencies
├── mpdrrmc_logo.png # PDRRMO logo
├── mpcfs_logo.png # MPCFS logo
├── .gitignore # Git ignore rules
├── tabs/
│ ├── about_indc.py # Evolution timeline & narrative
│ ├── drrm_intelligence.py # Hazard data & analytics
│ ├── plan_management.py # Plans, PPAs, indicators
│ ├── situation_report.py # Multi-user SitRep entry
│ ├── trainings.py # Training records
│ ├── ldrrmf_utilization.py # Fund tracking
│ └── document_studio.py # AI report generation (WIP)
└── utils/
├── supabase_client.py # Cloud sync
├── pagasa_api.py # PAGASA weather integration
├── database.py # Session state management
└── project_state.py # Chat continuity


---

## 🚀 The Evolution: 3D PRISM → ADST → INDC

| Phase | Years | Focus |
|-------|-------|-------|
| 3D PRISM | 2018-2021 | Risk Visualization |
| ADST | 2022-2023 | Decision Support |
| Governance Integration | 2024 | Policy Alignment |
| INDC | 2025+ | System Coordination |

*Developed and validated through the Executive Master in Disaster Risk and Crisis Management (EMDRCM) program at the 
Stephen Zuellig Graduate School of Development Management, Asian Institute of Management.*

---

## 💻 Local Development

```bash
git clone https://github.com/Niiru26/Integrated-Network-for-DRRM-Coordination.git
cd Integrated-Network-for-DRRM-Coordination
pip install -r requirements.txt
streamlit run app.py

📞 Contact
Mountain Province PDRRMO
Office: Mountain Province Disaster Risk Reduction and Management Office
Location: Appong Street, Jungle Town, Poblacion, Bontoc, Mountain Province
Email: cneil_japan@yahoo.com.ph

🙏 Acknowledgments
Built with Streamlit, powered by Mountain Province's 8+ years of disaster data, and a
vision for data-driven DRRM. Special thanks to the Asian Institute of Management (AIM) EMDRCM program
for the academic validation and governance framework development.

📖 "From Data to Decision, From Risk to Resilience"
© 2026 I.N.D.C. - Integrated Network for DRRM Coordination | Mountain Province PDRRMO

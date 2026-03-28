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

🔒 Security
Database credentials stored as Streamlit secrets
No sensitive data exposed in code
.gitignore protects secrets from version control

👥 Intended Users
PDRRMO personnel, Municipal DRRM officers, Disaster response planners, Researchers, Provincial government officials

🎯 Future Enhancements
✅ Plan Management (Completed)
✅ Enhanced Situation Report with PAGASA (Completed)
✅ Auto-sync to Supabase (Completed)
🚧 Climate Change Adaptation
🚧 Project Portfolio
🚧 Policy Guidelines
🚧 Strategic Plans
🚧 Geospatial Library
🚧 Risk Profiles
🚧 Performance Management System
🚧 Gender and Development
🚧 Gawad Kalasag
🚧 Knowledge Repository
🚧 Quick Guide
🚧 Settings
🚧 Document Studio (AI-powered report generation)
🚧 Mobile app for field reporting

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

=============================================================================================

Timeline Narrative: Evolution of 3D PRISM to ADST and into the INDC Platform

The evolution of the Analytical and Decision Support Tool (ADST) and its expansion into the Integrated Network for DRRM Coordination (INDC) traces its origins to the Three-Dimensional Precision Risk and Susceptibility Mapping (3D PRISM) initiative launched in 2018. What began as a geospatial innovation to enhance disaster risk visualization has progressively developed into a comprehensive, data-driven system for decision-making and governance. This transformation reflects a deliberate shift, from understanding disaster risk, to acting on it, and ultimately to coordinating it across all levels of the province.

The initial phase, 3D PRISM, focused on strengthening the province’s capacity to visualize disaster risk spatially and scientifically. By integrating hazard, exposure, and vulnerability data through Geographic Information Systems (GIS), satellite imagery, and early machine learning applications, the system enabled local decision-makers to identify high-risk areas with greater precision. It introduced the foundational concept of layered risk analysis and real-time hazard awareness, addressing the fundamental question: Where are the risks?

Building on this foundation, the system evolved into the Analytical and Decision Support Tool (ADST), marking a transition from visualization to decision support. ADST introduced a centralized digital repository that consolidates disaster-related information, including DRRM and CCA plans, situation reports, hazard advisories, geospatial datasets, and operational templates. Leveraging artificial intelligence, machine learning, and integration with the Pre-Disaster Risk Assessment (PDRA) process, the system enables automated data analysis, anticipatory action triggers, and rapid generation of context-specific reports and advisories. This phase significantly enhanced the ability of local governments to respond proactively, answering the critical question: What should we do?

The concept was further refined through its integration into a broader disaster risk governance framework, including its development and validation through applied research and systems design under the Executive Master in Disaster Risk and Crisis Management (EMDRCM) program at the Stephen Zuellig Graduate School of Development Management, Asian Institute of Management. At this stage, ADST was repositioned from a technical tool into a governance platform that connects planning, operations, and performance management systems. It integrates key instruments such as the Provincial Climate and Disaster Risk Reduction and Management Plan (PCDRRMP), Climate and Disaster Risk Assessment (CDRA), Emergency Operations Center (EOC) workflows, and performance systems including IPCR and OPCR. This alignment ensures that policies, programs, and actual operations are synchronized, addressing the systemic question: How do we govern climate and disaster risk better?

This progression culminates in the vision of the Integrated Network for DRRM Coordination (INDC), a province-wide, interoperable ecosystem that unifies data, analytics, and operations into a single coordinated platform. INDC integrates historical hazard data, predictive analytics, geospatial intelligence, resource and financial tracking, and real-time communication systems across barangay, municipal, and provincial levels. It enables seamless coordination, strengthens interoperability, and supports evidence-based decision-making at all levels of governance. At this stage, the system answers the ultimate question: How do we act as one coordinated system?

In summary, the evolution from 3D PRISM to ADST and into INDC represents a strategic transformation from risk visualization → decision support → governance integration → full system coordination. This trajectory positions Mountain Province at the forefront of anticipatory, data-driven, and integrated disaster risk governance, capable of transforming fragmented information into timely action, and risk into resilience.





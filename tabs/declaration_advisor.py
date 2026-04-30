# tabs/declaration_advisor.py
"""
DECLARATION ADVISOR - Decision Support Tool for State of Calamity and State of Imminent Disaster

PURPOSE:
- Provides legal framework and reference for declaration decisions
- Contains decision matrices for State of Calamity (RA 10121) and State of Imminent Disaster (RA 12287)
- Serves as a reference module for LDRRMC deliberation and recommendation

STATUS: REFERENCE MODULE (Under Development)
- Current version: Reference documentation and matrices only
- Future development: Interactive scoring, auto-recommendation generation, data integration from SitRep

DEPENDENCIES (Future):
- situation_report.py: RDANA data, casualties, displacement, damages
- PDR Assessment tab: PDRA results, CPA level, forecast data

LEGAL BASIS:
- RA 10121 (2010): Philippine Disaster Risk Reduction and Management Act
- RA 12287 (2025): Declaration of State of Imminent Disaster Act
- Operation L!sto Manual (2018): PDRA and CPA framework
"""

import streamlit as st
from datetime import datetime


def show():
    """Display Declaration Advisor reference and decision matrices"""
    
    st.markdown("# ⚖️ DECLARATION ADVISOR")
    st.caption("Decision Support Tool for State of Calamity and State of Imminent Disaster")
    
    # ============================================================
    # STATUS NOTE
    # ============================================================
    st.info(
        "## 🚧 Module Status: Reference & Documentation\n\n"
        "This module currently serves as a **reference and documentation** for declaration decisions.\n\n"
        "### Future Development (after situation_report.py is stable):\n"
        "- Interactive scoring matrices with auto-calculation\n"
        "- Auto-generated recommendation text based on SitRep data\n"
        "- Integration with RDANA results from Situation Report\n"
        "- Integration with PDRA results from PDR Assessment tab\n"
        "- Draft resolution generator for State of Calamity\n"
        "- Draft executive order generator for State of Imminent Disaster\n\n"
        "---\n"
    )
    
    # ============================================================
    # SECTION A: LEGAL FRAMEWORK
    # ============================================================
    with st.expander("📚 Legal Framework & References (APA 7th Edition)", expanded=True):
        st.markdown("### Primary Legal References")
        
        st.markdown(
            "**Republic of the Philippines. (2010, May 27). *Republic Act No. 10121: "
            "Philippine Disaster Risk Reduction and Management Act of 2010*. Lawphil. "
            "https://lawphil.net/statutes/repacts/ra2010/ra_10121_2010.html**\n\n"
            "- **State of Calamity**: Declared by the local sanggunian upon recommendation of the LDRRMC\n"
            "- **Basis**: Results of damage assessment and needs analysis (DANA/RDANA)\n"
            "- **Nature**: Post-impact declaration\n"
            "- **Key Provision**: Section 16 - Declaration of State of Calamity\n\n"
            "---\n\n"
            "**Republic of the Philippines. (2025, September 12). *Republic Act No. 12287: "
            "Declaration of State of Imminent Disaster Act*. Lawphil. "
            "https://lawphil.net/statutes/repacts/ra2025/ra_12287_2025.html**\n\n"
            "- **State of Imminent Disaster**: Declared by the local chief executive through executive order, "
            "upon recommendation of the Regional DRRM Council\n"
            "- **Basis**: Pre-Disaster Risk Assessment (PDRA) showing severe projected impacts\n"
            "- **Lead Time**: 3 to 5 days for anticipatory action\n"
            "- **Nature**: Pre-impact / forecast-based declaration\n"
            "- **Key Provision**: Section 4 - Declaration of State of Imminent Disaster\n\n"
            "---\n\n"
            "**Local Government Academy. (2018). *Disaster preparedness manual: Operation L!sto (Typhoon edition v3)*. "
            "Department of the Interior and Local Government. "
            "https://cdn.lga.gov.ph/publication/attachments/1590478478.pdf**\n\n"
            "- **Operation L!sto Framework**: CPA levels (Alpha/Bravo/Charlie)\n"
            "- **PDRA Methodology**: Pre-Disaster Risk Assessment process\n"
            "- **Critical Preparedness Actions**: Required actions per CPA level\n\n"
            "---\n\n"
            "### Secondary Reference\n\n"
            "**NDRRMC. (2019). *Memorandum Order No. 60, s. 2019: Revised Guidelines for the Declaration of a State of Calamity*. "
            "National Disaster Risk Reduction and Management Council.**\n\n"
            "- Provides national-level guidelines for declaration thresholds\n"
            "- Basis for harmonizing local declaration processes\n"
        )
    
    # ============================================================
    # SECTION B: ANTICIPATED NEEDS ASSESSMENT
    # ============================================================
    with st.expander("📋 Anticipated Needs Assessment - Priority Classification", expanded=False):
        st.markdown("### Priority Classification System")
        st.markdown(
            "Resource requirements during the emergency period are classified according to priority levels "
            "to guide planning, resource allocation, and possible augmentation support.\n\n"
            "| Rating Scale | Description |\n"
            "|--------------|-------------|\n"
            "| **Priority 1** | Search and rescue operations, immediate restoration of lifelines, relief supplies, and food assistance |\n"
            "| **Priority 2** | Clothing, shelter, personal belongings, housing materials, and other non-food items |\n"
            "| **Priority 3** | Economic recovery needs, such as farm implements and seeds for agricultural production, rehabilitation, repair and reconstruction of infrastructure, and cash-for-work assistance |\n\n"
            "### Example: Municipal Priority Needs Assessment\n\n"
            "Based on the assessment conducted, all municipalities identified cash-for-work assistance as a Priority 3 requirement.\n\n"
            "| Municipality | Priority 1 | Priority 2 | Priority 3 | Remarks |\n"
            "|--------------|------------|------------|------------|---------|\n"
            "| Barlig | | | ✓ | Cash-for-work |\n"
            "| Bauko | | | ✓ | Cash-for-work |\n"
            "| Besao | | | ✓ | Cash-for-work |\n"
            "| Bontoc | | | ✓ | Cash-for-work |\n"
            "| Natonin | | | ✓ | Cash-for-work |\n"
            "| Paracelis | | | ✓ | Cash-for-work |\n"
            "| Sabangan | | | ✓ | Cash-for-work |\n"
            "| Sadanga | | | ✓ | Cash-for-work |\n"
            "| Sagada | | | ✓ | Cash-for-work |\n"
            "| Tadian | | | ✓ | Cash-for-work |\n\n"
            "> **Analysis:** This indicated that, across all municipalities, anticipated needs were not limited to immediate life-saving assistance alone, "
            "but also extended to short-term economic recovery interventions aimed at restoring livelihoods and supporting early recovery.\n"
        )
    
    # ============================================================
    # SECTION C: DECISION MATRIX FOR STATE OF CALAMITY
    # ============================================================
    with st.expander("📊 DECISION MATRIX A: State of Calamity (RA 10121 - Post-Impact)", expanded=False):
        st.markdown("## Decision Matrix for Declaration of a State of Calamity")
        st.markdown(
            "**Legal Basis**: RA 10121 - Based on RDANA/DANA and validated field reports\n\n"
            "**Purpose**: To support the LDRRMC's recommendation to the sanggunian under RA 10121\n\n"
            "---\n\n"
            "### A.1 Sectoral Impact Scoring Matrix\n\n"
            "| Sector / Dimension | Sample Evidence / Indicators | Severity (0-4) | Spread (0-3) | Duration (0-3) | Weighted Score* |\n"
            "|--------------------|------------------------------|----------------|--------------|----------------|-----------------|\n"
            "| **People** | Deaths, injured, missing, displaced families, evacuees, vulnerable groups affected | | | | |\n"
            "| **Housing** | Totally and partially damaged houses; unsafe settlements | | | | |\n"
            "| **Lifelines** | Roads blocked, bridges damaged, power outage, water interruption, telecom disruption | | | | |\n"
            "| **Social Services** | Schools, health facilities, evacuation center congestion, WASH disruption | | | | |\n"
            "| **Livelihood / Economy** | Crop loss, livestock loss, business disruption, public transport disruption | | | | |\n"
            "| **Governance / Operations** | LGU response capacity strained, multiple barangays needing augmentation, prolonged EOC activation | | | | |\n\n"
            "*Weighted Score = (Severity × 2) + Spread + Duration\n\n"
            "---\n\n"
            "### A.2 Scoring Guide\n\n"
            "| Score Element | Rating | Interpretation |\n"
            "|---------------|--------|----------------|\n"
            "| **Severity** | 0 | No significant impact |\n"
            "| | 1 | Minor impact; localized and manageable with routine response |\n"
            "| | 2 | Moderate impact; partial disruption of services or livelihoods |\n"
            "| | 3 | Major impact; multi-sector disruption; local resources strained |\n"
            "| | 4 | Severe impact; widespread disruption; local capacity exceeded |\n"
            "| **Spread** | 0 | No affected area or negligible |\n"
            "| | 1 | Isolated sitio / barangay / facility |\n"
            "| | 2 | Several barangays or a large portion of the LGU |\n"
            "| | 3 | Municipality / city-wide, province-wide, or multi-LGU impact |\n"
            "| **Duration** | 0 | Less than 12 hours |\n"
            "| | 1 | 12–24 hours |\n"
            "| | 2 | 1–3 days |\n"
            "| | 3 | More than 3 days or restoration uncertain |\n\n"
            "---\n\n"
            "### A.3 Decision Rules for State of Calamity\n\n"
            "| Condition | Recommended Action |\n"
            "|-----------|-------------------|\n"
            "| Composite weighted score below 15 and no critical trigger | Continue response, monitoring, and reassessment; no declaration yet |\n"
            "| Composite weighted score 15–19 | LDRRMC deliberation; declaration may be recommended if impacts are clearly beyond routine local response |\n"
            "| Composite weighted score 20 or higher | **Recommend declaration** of a State of Calamity to the local sanggunian |\n"
            "| Any critical trigger present, even if score is below threshold | Immediate LDRRMC deliberation for possible recommendation |\n\n"
            "---\n\n"
            "### A.4 Critical Triggers for Immediate LDRRMC Deliberation\n\n"
            "| Critical Trigger | Yes/No |\n"
            "|-----------------|--------|\n"
            "| There are deaths, missing persons, or multiple serious injuries | |\n"
            "| There is mass displacement or large-scale evacuation | |\n"
            "| Major roads, bridges, power, water, or communications are significantly disrupted | |\n"
            "| Multiple barangays or communities are isolated / inaccessible | |\n"
            "| Essential services are seriously disrupted | |\n"
            "| Local response capacity is clearly insufficient and augmentation is needed | |\n"
            "| Significant damage to housing, livelihoods, agriculture, or public infrastructure has impaired normal community functioning | |\n\n"
            "---\n\n"
            "### A.5 Suggested Certification Line\n\n"
            "> **Recommendation**: Based on the validated results of the RDANA/DANA and the completed impact matrix, "
            "the LDRRMC finds that the actual disaster impacts have / have not reached the threshold for recommending "
            "the declaration of a State of Calamity under RA 10121.\n\n"
            "---\n\n"
            "### A.6 Practical Workflow\n\n"
            "1. Collect RDANA/DANA results\n"
            "2. Fill out the sector impact matrix\n"
            "3. Validate with MDRRMOs, barangays, and sectoral offices\n"
            "4. Present matrix to the LDRRMC\n"
            "5. LDRRMC issues recommendation\n"
            "6. Sanggunian deliberates and declares State of Calamity, if warranted under RA 10121\n"
        )
    
    # ============================================================
    # SECTION D: DECISION MATRIX FOR STATE OF IMMINENT DISASTER
    # ============================================================
    with st.expander("⚠️ DECISION MATRIX B: State of Imminent Disaster (RA 12287 - Pre-Impact)", expanded=False):
        st.markdown("## Decision Matrix for Declaration of a State of Imminent Disaster")
        st.markdown(
            "**Legal Basis**: RA 12287 - Based on forecast and PDRA, with 3-5 day lead time\n\n"
            "**Purpose**: To support the local chief executive's declaration through executive order, upon recommendation of the RDRRMC\n\n"
            "---\n\n"
            "### B.1 Mandatory Legal Screening Criteria (Gates)\n\n"
            "*If any required item is **No**, do not recommend declaration yet.*\n\n"
            "| Mandatory Screening Question | Yes/No | Notes |\n"
            "|-----------------------------|--------|-------|\n"
            "| Has a formal PDRA been conducted? | | Must be completed using Operation L!sto framework |\n"
            "| Is the hazard forecastable / modelable and highly probable? | | Based on PAGASA / PHIVOLCS / MGB advisories |\n"
            "| Are the projected impacts severe or equivalent? | | Based on PDRA results |\n"
            "| Is there an allowable or sufficient lead time of 3 to 5 days for anticipatory action? | | As provided in RA 12287 |\n"
            "| Do the projected impacts affect people, especially vulnerable groups, and significant sectors? | | Population exposure and vulnerability assessment |\n\n"
            "---\n\n"
            "### B.2 Projected Impact Matrix (Supporting)\n\n"
            "| Dimension | Sample PDRA Questions / Indicators | Rating (0-3) |\n"
            "|-----------|-----------------------------------|--------------|\n"
            "| **Forecast Confidence / Probability** | Is the hazard highly probable based on PAGASA / PHIVOLCS / MGB / other competent agencies? | |\n"
            "| **Projected Population Impact** | Are large populations, especially exposed and vulnerable groups, likely to be affected? | |\n"
            "| **Projected Lifeline / Critical Facility Impact** | Are roads, bridges, power, water, telecom, schools, hospitals, or evacuation routes likely to be disrupted? | |\n"
            "| **Projected Livelihood / Sectoral Impact** | Are agriculture, fisheries, transport, tourism, business, or other significant sectors likely to be severely affected? | |\n"
            "| **Cascading Hazard Potential** | Is there potential for secondary hazards, such as landslides, flooding, isolation, public health risks, or supply disruption? | |\n"
            "| **Local Capacity Gap** | Are local resources and readiness likely to be insufficient without anticipatory augmentation? | |\n"
            "| **Anticipatory Action Value** | Will early action likely reduce losses, displacement, or operational disruption? | |\n\n"
            "**Total Supporting Score** = Sum of all ratings (0-21)\n\n"
            "---\n\n"
            "### B.3 Rating Guide for Projected Impact Matrix\n\n"
            "| Rating | Interpretation |\n"
            "|--------|----------------|\n"
            "| 0 | Negligible or not evident |\n"
            "| 1 | Limited / localized projected effect |\n"
            "| 2 | Significant projected effect |\n"
            "| 3 | Severe / widespread / capacity-exceeding projected effect |\n\n"
            "---\n\n"
            "### B.4 Decision Rules for State of Imminent Disaster\n\n"
            "| Condition | Recommended Action |\n"
            "|-----------|-------------------|\n"
            "| Any mandatory legal screening item is **No** | Do not recommend declaration yet; continue monitoring and update PDRA |\n"
            "| All mandatory legal screening items are **Yes**, but supporting score is below 10 | Intensify preparedness and prepositioning; reassess with next PDRA cycle |\n"
            "| All mandatory legal screening items are **Yes**, and supporting score is 10–14 | Prepare draft recommendation and EO package; validate with RDRRMC / OCD |\n"
            "| All mandatory legal screening items are **Yes**, and supporting score is 15 or higher | **Recommend declaration** of a State of Imminent Disaster |\n\n"
            "---\n\n"
            "### B.5 Suggested Certification Line\n\n"
            "> **Recommendation**: Based on the PDRA and the projected impact matrix, the event does / does not meet the conditions "
            "for recommending the declaration of a State of Imminent Disaster under RA 12287, particularly with respect to severe "
            "projected impacts and allowable lead time for anticipatory action.\n\n"
            "---\n\n"
            "### B.6 Practical Workflow\n\n"
            "1. Conduct PDRA using Operation L!sto framework\n"
            "2. Verify mandatory legal screening criteria\n"
            "3. Complete projected impact matrix\n"
            "4. Present to LDRRMC / RDRRMC for deliberation\n"
            "5. RDRRMC issues recommendation\n"
            "6. Local chief executive declares through Executive Order under RA 12287\n"
        )
    
    # ============================================================
    # SECTION E: COMPARISON SUMMARY
    # ============================================================
    with st.expander("📋 Comparison: State of Calamity vs. State of Imminent Disaster", expanded=False):
        st.markdown("## Summary Table: Two Declaration Types")
        st.markdown(
            "| Declaration | Basis | Who Recommends | Who Declares | Best Tool | Legal Basis |\n"
            "|-------------|-------|----------------|--------------|-----------|-------------|\n"
            "| **State of Calamity** | Actual impacts after hazard, based on RDANA / DANA | LDRRMC | Local sanggunian | Actual impact matrix | RA 10121, Sec. 16 |\n"
            "| **State of Imminent Disaster** | Forecast + PDRA showing severe projected impacts and 3–5 day lead time | RDRRMC | Local chief executive through EO | Projected impact matrix | RA 12287, Sec. 4 |\n\n"
            "---\n\n"
            "## Key Distinctions\n\n"
            "| Aspect | State of Calamity | State of Imminent Disaster |\n"
            "|--------|-------------------|---------------------------|\n"
            "| **Timing** | AFTER impact | BEFORE impact |\n"
            "| **Trigger** | Actual damage assessment | Forecast + PDRA |\n"
            "| **Data Source** | RDANA/DANA, validated SitReps | PAGASA/PHIVOLCS, PDRA |\n"
            "| **Lead Time** | Not applicable | 3-5 days for anticipatory action |\n"
            "| **Primary Benefit** | Access to 30% LDRRMF | Access to QRF before impact |\n"
            "| **Declaration Authority** | Local sanggunian | Local chief executive (EO) |\n"
            "| **Recommending Body** | LDRRMC | RDRRMC |\n\n"
            "---\n\n"
            "## Practical Model\n\n"
            "```\n"
            "┌─────────────────────────────────────────────────────────────────┐\n"
            "│                    DECLARATION WORKFLOW                         │\n"
            "├─────────────────────────────────────────────────────────────────┤\n"
            "│                                                                 │\n"
            "│  BEFORE IMPACT                    AFTER IMPACT                  │\n"
            "│  ┌─────────────────┐              ┌─────────────────┐          │\n"
            "│  │    PDRA +       │              │  RDANA/DANA +   │          │\n"
            "│  │   Forecast      │              │  Actual Impact  │          │\n"
            "│  └────────┬────────┘              └────────┬────────┘          │\n"
            "│           │                                │                    │\n"
            "│           ▼                                ▼                    │\n"
            "│  ┌─────────────────┐              ┌─────────────────┐          │\n"
            "│  │  State of       │              │  State of       │          │\n"
            "│  │  Imminent       │              │  Calamity       │          │\n"
            "│  │  Disaster       │              │                 │          │\n"
            "│  │  (RA 12287)     │              │  (RA 10121)     │          │\n"
            "│  └─────────────────┘              └─────────────────┘          │\n"
            "│                                                                 │\n"
            "└─────────────────────────────────────────────────────────────────┘\n"
            "```\n"
        )
    
    # ============================================================
    # SECTION F: DISCLAIMER
    # ============================================================
    with st.expander("⚠️ Important Disclaimer", expanded=False):
        st.markdown("## Disclaimer")
        st.markdown(
            "> **Note:** The matrices and scoring systems presented in this module are proposed local decision-support tools "
            "intended to guide deliberation and recommendation. They do not replace the legal authority of the LDRRMC, "
            "the Regional DRRM Council, the local sanggunian, or the local chief executive, as applicable. "
            "Local government units may adopt or modify these tools through local policy, resolution, or standard operating procedure.\n\n"
            "---\n\n"
            "## Future Development Notes\n\n"
            "The following features are planned for future versions of this module:\n\n"
            "1. **Interactive Scoring Matrices**\n"
            "   - Auto-calculation of weighted scores\n"
            "   - Visual severity indicators\n"
            "   - Real-time recommendation updates\n\n"
            "2. **Data Integration**\n"
            "   - Auto-populate from `situation_report.py` (RDANA results)\n"
            "   - Auto-populate from PDR Assessment tab (PDRA results)\n"
            "   - Extract casualty, displacement, and damage data\n\n"
            "3. **Recommendation Engine**\n"
            "   - Auto-generated recommendation text\n"
            "   - Justification based on matrix results\n"
            "   - Export to PDF for LDRRMC deliberation\n\n"
            "4. **Document Generator**\n"
            "   - Draft resolution for State of Calamity\n"
            "   - Draft executive order for State of Imminent Disaster\n"
            "   - Pre-filled with LGU information\n\n"
            "---\n\n"
            "## Cross-Reference to INDC Modules\n\n"
            "| Data Source | Module | Used For |\n"
            "|-------------|--------|----------|\n"
            "| RDANA results | `situation_report.py` (Section 7) | State of Calamity matrix |\n"
            "| PDRA results | `situation_report.py` (PDR Assessment tab) | State of Imminent Disaster matrix |\n"
            "| Casualties, displacement, damages | `situation_report.py` (Section 6) | Severity scoring |\n"
            "| CPA Level | PDR Assessment tab | Imminent Disaster trigger |\n"
            "| Anticipated needs | `situation_report.py` (Section 7) | Priority classification |\n"
        )
    
    # ============================================================
    # SECTION G: QUICK REFERENCE CARD
    # ============================================================
    with st.expander("📇 Quick Reference Card (Printable)", expanded=False):
        st.markdown("## Quick Reference Card for Declaration Decisions")
        st.markdown(
            "### State of Calamity (RA 10121)\n\n"
            "| Threshold | Action |\n"
            "|-----------|--------|\n"
            "| Score < 15, no critical trigger | No declaration |\n"
            "| Score 15-19 | LDRRMC deliberation |\n"
            "| Score ≥ 20 | **Recommend declaration** |\n"
            "| Any critical trigger | Immediate deliberation |\n\n"
            "### State of Imminent Disaster (RA 12287)\n\n"
            "| Condition | Action |\n"
            "|-----------|--------|\n"
            "| Any mandatory gate = No | No declaration |\n"
            "| All gates Yes, score < 10 | Intensify preparedness |\n"
            "| All gates Yes, score 10-14 | Prepare recommendation |\n"
            "| All gates Yes, score ≥ 15 | **Recommend declaration** |\n\n"
            "### Critical Triggers (State of Calamity)\n\n"
            "- Deaths, missing, or serious injuries\n"
            "- Mass displacement or large-scale evacuation\n"
            "- Major lifeline disruption\n"
            "- Multiple barangays isolated\n"
            "- Local capacity insufficient\n"
            "- Significant damage to housing/livelihoods\n\n"
            "### Mandatory Gates (State of Imminent Disaster)\n\n"
            "- Formal PDRA conducted\n"
            "- Hazard forecastable and highly probable\n"
            "- Projected impacts severe\n"
            "- Lead time 3-5 days\n"
            "- Vulnerable populations affected\n"
        )
    
    # ============================================================
    # FOOTER
    # ============================================================
    st.markdown("---")
    st.caption(f"📌 Declaration Advisor v0.1 (Reference Module) | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("⚖️ Legal references: RA 10121 (2010), RA 12287 (2025), NDRRMC Memo No. 60 s. 2019, Operation L!sto Manual (2018)")


# For testing standalone
if __name__ == "__main__":
    show()
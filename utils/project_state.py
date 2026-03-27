# utils/project_state.py
import streamlit as st
from datetime import datetime

def create_state_snapshot_button():
    """Simple button to save your progress for the next chat"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Chat Continuity")
    
    if st.sidebar.button("📸 Save Progress for Next Chat", key="save_progress_button"):
        # Create a summary
        state_text = f"""
# INDC App Project State - Part 4
**Saved on:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

## What's Working
- ✅ Dashboard
- ✅ DRRM Intelligence  
- ✅ Trainings Tab
- ✅ LDRRMF Utilization Tab
- ✅ Situation Report Tab (MDRRMO and PDRRMO views)
- ✅ About INDC (with INPUT-PROCESS-OUTPUT)
- ✅ User Role System (PDRRMO/MDRRMO)

## Disabled (needs fix)
- ⏸️ Plan Management Tab (too complex, will rebuild in Part 5)

## Next Steps for Part 5
1. Rebuild Plan Management tab with simpler functions
2. Connect all tabs to Supabase
3. Build Document Studio
4. Add PAGASA weather API

---
Copy this text and paste at the start of your next chat!
"""
        # Save to file
        with open("CHAT_CONTINUITY.txt", "w", encoding="utf-8") as f:
            f.write(state_text)
        
        st.sidebar.success("✅ Progress saved to CHAT_CONTINUITY.txt!")
        st.sidebar.info("📄 Open CHAT_CONTINUITY.txt in VS Code and copy for next chat")
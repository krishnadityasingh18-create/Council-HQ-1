import streamlit as st
from styles import apply_design

# 1. Apply our custom aesthetic
apply_design()

# 2. Define the pages and their icons
war_room = st.Page("pages/war_room.py", title="War Room", icon="🛡️", default=True)
intel = st.Page("pages/intel.py", title="Intelligence", icon="🕵️")
tech = st.Page("pages/tech.py", title="Technical", icon="🛠️")
research = st.Page("pages/research.py", title="Research", icon="🔬")
content = st.Page("pages/content.py", title="Content", icon="🎨")

# 3. Create the sidebar navigation
pg = st.navigation({
    "Central Command": [war_room],
    "Departments": [intel, tech, research, content]
})

# 4. Global Sidebar Footer (Clean and Informative)
st.sidebar.markdown("---")
st.sidebar.caption("Council Status: **Online**")
st.sidebar.caption("Environment: **Cloud Production**")

# 5. Run the selected page
pg.run()
import streamlit as st
from styles import apply_design

st.set_page_config(page_title="Council HQ", page_icon="🛡️", layout="wide")
apply_design()

# Define the Pages
war_room = st.Page("pages/war_room.py", title="War Room", icon="🛡️", default=True)
intel = st.Page("pages/intel.py", title="Intelligence", icon="🕵️")
tech = st.Page("pages/tech.py", title="Technical", icon="🛠️")
research = st.Page("pages/research.py", title="Research", icon="🔬")
content = st.Page("pages/content.py", title="Content", icon="🎨")

# Navigation setup
pg = st.navigation([war_room, intel, tech, research, content])
pg.run()

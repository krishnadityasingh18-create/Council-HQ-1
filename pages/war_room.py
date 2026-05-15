import streamlit as st
from groq import Groq

st.title("🛡️ War Room: Central Command")
st.markdown("---")

# Pulls key from Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
    mission = st.text_area("Global Mission Objective:", placeholder="Analyze the feasibility of a 6-layer PCB for a weather station...")

    if st.button("Deploy Council"):
        with st.spinner("Briefing the Directors..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are the Chairman. Break this mission into 4 strategic tasks for Intel, Tech, Research, and Content departments."},
                    {"role": "user", "content": mission}
                ]
            )
            st.session_state['mission_brief'] = response.choices[0].message.content
            st.markdown(st.session_state['mission_brief'])
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")

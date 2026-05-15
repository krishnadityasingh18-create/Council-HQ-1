import streamlit as st
from groq import Groq

st.title("🛡️ War Room: Central Command")

# Sidebar for API Key (Global access)
groq_key = st.sidebar.text_input("Groq API Key", type="password")

if groq_key:
    client = Groq(api_key=groq_key)
    mission = st.text_area("Enter Mission Objective:", placeholder="Analyze the market for AI-driven PCB design tools...")

    if st.button("Deploy Council"):
        with st.spinner("The Chairman is briefing the directors..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are the Chairman. Break down the user mission into 4 tasks: Intel, Technical, Research, and Content. Be brief and strategic."},
                    {"role": "user", "content": mission}
                ]
            )
            st.session_state['mission_brief'] = response.choices[0].message.content
            st.success("Mission Briefing Generated! Visit Departments for details.")
            st.markdown(st.session_state['mission_brief'])
else:
    st.warning("Enter Groq Key in Sidebar to Begin.")
import streamlit as st
from groq import Groq

st.title("🕵️ Intelligence Department")
mission = st.session_state.get('global_mission')

if not mission:
    st.warning("Awaiting mission from War Room...")
else:
    api_key = st.secrets.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    # AUTO-EXECUTION LOGIC
    if 'intel_res' not in st.session_state:
        with st.spinner("Scout Agent processing mission..."):
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are the Intel Director. Execute the [INTEL] portion of this mission."},
                          {"role": "user", "content": mission}]
            )
            st.session_state['intel_res'] = res.choices[0].message.content

    st.info(st.session_state['intel_res'])

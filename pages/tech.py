import streamlit as st
import requests

st.title("🛠️ Technical Department")
mission = st.session_state.get('global_mission')

if not mission:
    st.warning("Awaiting mission...")
else:
    api_key = st.secrets.get("DEEPSEEK_API_KEY")
    if 'tech_res' not in st.session_state:
        with st.spinner("Architecting solution..."):
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "system", "content": "Execute the [TECH] task of this mission."},
                             {"role": "user", "content": mission}]
            }
            res = requests.post("https://api.deepseek.com/chat/completions", 
                                json=payload, headers={"Authorization": f"Bearer {api_key}"})
            st.session_state['tech_res'] = res.json()['choices'][0]['message']['content']

    st.code(st.session_state['tech_res'], language='python')

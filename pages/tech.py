import streamlit as st
import requests

st.title("🛠️ Technical Department")

# DeepSeek uses a different API structure (OpenAI compatible)
ds_key = st.sidebar.text_input("DeepSeek API Key", type="password")

if ds_key:
    task = st.text_area("Coding/Engineering Task:", value=st.session_state.get('mission_brief', ''))
    
    if st.button("Generate Technical Solution"):
        with st.spinner("DeepSeek V4 is architecting..."):
            # This is a standard API call to DeepSeek
            headers = {"Authorization": f"Bearer {ds_key}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat", # This will point to V4 in May 2026
                "messages": [{"role": "system", "content": "You are the Technical Director. Provide clean, optimized code and engineering schematics."},
                             {"role": "user", "content": task}]
            }
            res = requests.post("https://api.deepseek.com/chat/completions", json=payload, headers=headers)
            st.code(res.json()['choices'][0]['message']['content'], language='python')
else:
    st.info("Awaiting DeepSeek API Key...")
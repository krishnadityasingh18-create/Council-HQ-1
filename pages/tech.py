import streamlit as st
import requests

st.title("🛠️ Technical Department")
st.markdown("---")

api_key = st.secrets.get("DEEPSEEK_API_KEY")

if api_key:
    task = st.text_area("Technical/Coding Task:")
    
    if st.button("Architect Solution"):
        with st.spinner("DeepSeek is calculating..."):
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "system", "content": "You are the Technical Director. Provide optimized code and schematics."},
                             {"role": "user", "content": task}]
            }
            res = requests.post("https://api.deepseek.com/chat/completions", json=payload, headers=headers)
            st.code(res.json()['choices'][0]['message']['content'], language='python')
else:
    st.error("Missing DEEPSEEK_API_KEY in Streamlit Secrets.")

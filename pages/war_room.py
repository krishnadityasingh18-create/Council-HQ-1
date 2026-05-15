import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai
import time

st.set_page_config(page_title="Council HQ", page_icon="🛡️", layout="wide")

st.title("🛡️ War Room: Central Command")

# 1. API Configuration
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

mission = st.text_area("Global Mission Objective:", height=100)

if st.button("🚀 Deploy Full Council"):
    client = Groq(api_key=groq_key)
    with st.status("Council Deployment...", expanded=True) as status:
        # Chairman
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Split into [INTEL], [TECH], [RESEARCH]."},
                      {"role": "user", "content": mission}]
        )
        st.session_state['global_mission'] = res.choices[0].message.content
        
        # Intel
        res_i = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Execute [INTEL]."},
                      {"role": "user", "content": st.session_state['global_mission']}]
        )
        st.session_state['intel_res'] = res_i.choices[0].message.content
        
        # Research
        res_r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "Execute [RESEARCH]."},
                      {"role": "user", "content": st.session_state['global_mission']}]
        )
        st.session_state['res_res'] = res_r.choices[0].message.content

        # Tech (DeepSeek)
        if deepseek_key:
            try:
                r = requests.post("https://api.deepseek.com/chat/completions", 
                                 json={"model": "deepseek-chat", "messages": [{"role": "user", "content": f"Tech: {mission}"}]}, 
                                 headers={"Authorization": f"Bearer {deepseek_key}"}, timeout=15)
                st.session_state['tech_res'] = r.json().get('choices', [{}])[0].get('message', {}).get('content', 'Tech Offline')
            except: st.session_state['tech_res'] = "Tech Timeout"

        status.update(label="✅ Agents Finished!", state="complete")

# --- THE FINAL ASSEMBLY (UNIVERSAL LOADER) ---
if st.button("🖋️ Generate Master Dossier"):
    if not st.secrets.get("GEMINI_API_KEY"):
        st.error("API Key missing!")
    else:
        with st.spinner("Council is assembling the final report..."):
            try:
                # Force the library to use the stable configuration
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                
                # TEST 1: Try the most stable name first
                # We skip 'models/' prefix because the library adds it
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prepare the data
                ctx = f"INTEL: {st.session_state.get('intel_res')}\nTECH: {st.session_state.get('tech_res')}\nRES: {st.session_state.get('res_res')}"
                
                # Execute with a direct prompt
                response = model.generate_content(
                    f"Combine these reports into one professional engineering dossier: {ctx}",
                    request_options={"timeout": 600}
                )
                
                st.session_state['final_report'] = response.text
                st.success("✅ Success!")
                st.markdown(st.session_state['final_report'])
                
            except Exception as e:
                # IF TEST 1 FAILS: Try the "Latest" tag which bypasses versioning
                try:
                    st.info("Retrying with legacy-stable path...")
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"Summarize this: {ctx}")
                    st.session_state['final_report'] = response.text
                    st.rerun()
                except Exception as e2:
                    st.error(f"Critical Failure: {e2}")
                    st.info("Check: Is your API key from 'Google AI Studio' and not 'Google Cloud Vertex AI'?")

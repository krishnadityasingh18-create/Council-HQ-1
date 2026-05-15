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

# --- THE FINAL ASSEMBLY (REPAIRED) ---
st.markdown("---")
if 'intel_res' in st.session_state:
    if st.button("🖋️ Generate Master Dossier"):
        with st.spinner("Synthesizing Final Report..."):
            genai.configure(api_key=gemini_key)
            
            # Using the EXACT strings from your successful ListModels call
            # Removing the 'models/' prefix as the GenerativeModel class adds it automatically
            fallbacks = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']
            
            success = False
            ctx = f"Intel: {st.session_state['intel_res']}\nTech: {st.session_state['tech_res']}\nRes: {st.session_state['res_res']}"
            
            for m_name in fallbacks:
                try:
                    model = genai.GenerativeModel(m_name)
                    final = model.generate_content(f"Create a professional report: {ctx}")
                    st.session_state['final_report'] = final.text
                    success = True
                    break 
                except Exception as e:
                    st.warning(f"Model {m_name} failed. Checking next...")
                    time.sleep(2) # Cooldown to avoid RPM limits
            
            if success:
                st.markdown(st.session_state['final_report'])
                st.download_button("Download Report", st.session_state['final_report'], file_name="Report.md")
            else:
                st.error("All Gemini models are currently rate-limited. Please wait 1-2 minutes.")

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

# --- THE FINAL ASSEMBLY (GROQ-POWERED) ---
st.markdown("---")
if 'intel_res' in st.session_state:
    if st.button("🖋️ Generate Master Dossier"):
        with st.spinner("Llama 3.3 is synthesizing the final report..."):
            if not groq_key:
                st.error("❌ Missing GROQ_API_KEY")
            else:
                try:
                    # We reuse the client defined earlier in the script
                    client = Groq(api_key=groq_key)
                    
                    # Prepare the context
                    ctx = f"""
                    MISSION BRIEF: {st.session_state.get('global_mission', 'N/A')}
                    
                    ---
                    [DEPARTMENT 1: INTELLIGENCE]
                    {st.session_state.get('intel_res', 'No data')}
                    
                    ---
                    [DEPARTMENT 2: TECHNICAL ARCHITECTURE]
                    {st.session_state.get('tech_res', 'No data')}
                    
                    ---
                    [DEPARTMENT 3: RESEARCH & STANDARDS]
                    {st.session_state.get('res_res', 'No data')}
                    """
                    
                    # Synthesis Call
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are the Chief of Staff. Synthesize the provided department reports into a professional, cohesive executive dossier. Use clean Markdown, clear headings, and ensure all technical specs are preserved."},
                            {"role": "user", "content": ctx}
                        ]
                    )
                    
                    st.session_state['final_report'] = response.choices[0].message.content
                    st.success("✅ Dossier Compiled via Llama-3-70B!")
                    st.markdown(st.session_state['final_report'])
                    
                    st.download_button(
                        label="📥 Download Master Report (.md)",
                        data=st.session_state['final_report'],
                        file_name="Council_Final_Report.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Groq Synthesis failed: {e}") AI Studio' and not 'Google Cloud Vertex AI'?")

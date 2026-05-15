import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai
import time

st.set_page_config(page_title="Council HQ", page_icon="🛡️", layout="wide")

st.title("🛡️ War Room: Central Command")
st.markdown("### ⚡ Fully Autonomous Mission Control")

# 1. API Configuration
groq_key = st.secrets.get("GROQ_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

mission = st.text_area("Global Mission Objective:", 
                       placeholder="Enter your goal...", 
                       height=100)

# --- PHASE 1: THE DEPLOYMENT ---
if st.button("🚀 Deploy Full Council"):
    if not groq_key:
        st.error("❌ Missing GROQ_API_KEY")
    else:
        client = Groq(api_key=groq_key)
        with st.status("Council Deployment in Progress...", expanded=True) as status:
            
            # --- CHAIRMAN ---
            st.write("🏛️ Chairman: Drafting Strategic Brief...")
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Split mission into [INTEL], [TECH], and [RESEARCH] tasks."},
                              {"role": "user", "content": mission}]
                )
                st.session_state['global_mission'] = res.choices[0].message.content
            except Exception as e:
                st.error(f"Chairman failed: {e}")
                st.stop()

            # --- INTEL ---
            st.write("🕵️ Intel Director: Conducting Recon...")
            try:
                res_i = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Execute [INTEL]."},
                              {"role": "user", "content": st.session_state['global_mission']}]
                )
                st.session_state['intel_res'] = res_i.choices[0].message.content
            except:
                st.session_state['intel_res'] = "Intel report unavailable."

            # --- RESEARCH ---
            st.write("🔬 Research Director: Verifying Specs...")
            try:
                res_r = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Execute [RESEARCH]."},
                              {"role": "user", "content": st.session_state['global_mission']}]
                )
                st.session_state['res_res'] = res_r.choices[0].message.content
            except:
                st.session_state['res_res'] = "Research data unavailable."

# --- TECH DIRECTOR (WITH AUTO-FAILOVER) ---
            st.write("🛠️ Technical Director: Building Architecture...")
            tech_success = False
            
            # Attempt 1: DeepSeek
            if deepseek_key:
                try:
                    p = {
                        "model": "deepseek-chat", 
                        "messages": [{"role": "system", "content": "You are a Senior Electronics Engineer. Design the technical architecture requested."},
                                     {"role": "user", "content": f"Execute [TECH]: {mission}"}]
                    }
                    r = requests.post(
                        "https://api.deepseek.com/chat/completions", 
                        json=p, 
                        headers={"Authorization": f"Bearer {deepseek_key}"}, 
                        timeout=10 # Short timeout to trigger failover quickly
                    )
                    if r.status_code == 200:
                        st.session_state['tech_res'] = r.json().get('choices', [{}])[0].get('message', {}).get('content', 'Tech Offline')
                        tech_success = True
                    else:
                        st.warning("DeepSeek busy... switching to Llama-3 Backup.")
                except:
                    pass # Move to failover

            # Attempt 2: Failover to Groq/Llama (The Bulletproof Path)
            if not tech_success:
                try:
                    res_t = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Lead Technical Architect: Design the hardware and code architecture for this mission."},
                                  {"role": "user", "content": f"Execute [TECH]: {mission}"}]
                    )
                    st.session_state['tech_res'] = res_t.choices[0].message.content
                    tech_success = True
                    st.write("🛠️ Technical Director: (via Llama-3 Backup) ✅")
                except Exception as e:
                    st.session_state['tech_res'] = f"Technical Agent critical failure: {e}"

# --- PHASE 2: THE FINAL ASSEMBLY (GROQ-POWERED) ---
st.markdown("---")
if 'intel_res' in st.session_state:
    if st.button("🖋️ Generate Master Dossier"):
        with st.spinner("Llama 3.3 is synthesizing the final report..."):
            try:
                client = Groq(api_key=groq_key)
                
                ctx = f"""
                MISSION BRIEF: {st.session_state.get('global_mission', 'N/A')}
                ---
                [INTEL]: {st.session_state.get('intel_res')}
                ---
                [TECH]: {st.session_state.get('tech_res')}
                ---
                [RESEARCH]: {st.session_state.get('res_res')}
                """
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are the Chief of Staff. Synthesize these reports into a professional, cohesive executive dossier in Markdown."},
                        {"role": "user", "content": ctx}
                    ]
                )
                
                st.session_state['final_report'] = response.choices[0].message.content
                st.success("✅ Dossier Compiled!")
                st.markdown(st.session_state['final_report'])
                
                st.download_button(
                    label="📥 Download Report",
                    data=st.session_state['final_report'],
                    file_name="Council_Report.md"
                )
            except Exception as e:
                st.error(f"Synthesis failed: {e}")

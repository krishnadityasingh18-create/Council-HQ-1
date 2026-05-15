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
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

mission = st.text_area("Global Mission Objective:", 
                       placeholder="e.g., Design a 6-layer Smart Weather Station...", 
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
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Execute [INTEL]."},
                              {"role": "user", "content": st.session_state['global_mission']}]
                )
                st.session_state['intel_res'] = res.choices[0].message.content
            except:
                st.session_state['intel_res'] = "Intel report unavailable."

            # --- RESEARCH ---
            st.write("🔬 Research Director: Verifying Specs...")
            try:
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Execute [RESEARCH]."},
                              {"role": "user", "content": st.session_state['global_mission']}]
                )
                st.session_state['res_res'] = res.choices[0].message.content
            except:
                st.session_state['res_res'] = "Research data unavailable."

            # --- TECH ---
            st.write("🛠️ Technical Director: Building Architecture...")
            if deepseek_key:
                try:
                    p = {"model": "deepseek-chat", "messages": [{"role": "user", "content": f"Execute [TECH]: {mission}"}]}
                    r = requests.post("https://api.deepseek.com/chat/completions", 
                                     json=p, headers={"Authorization": f"Bearer {deepseek_key}"}, timeout=15)
                    st.session_state['tech_res'] = r.json().get('choices', [{}])[0].get('message', {}).get('content', 'Tech Offline')
                except:
                    st.session_state['tech_res'] = "Technical Agent Timeout."

            status.update(label="✅ All Departments Finished!", state="complete", expanded=False)

# --- PHASE 2: THE FINAL SYNTHESIS (Quota-Resilient) ---
st.markdown("---")
if 'intel_res' in st.session_state:
    if st.button("🖋️ Generate Master Dossier"):
        if not gemini_key:
            st.error("❌ Missing GEMINI_API_KEY")
        else:
            with st.spinner("Assembling final report (Managing Quotas)..."):
                genai.configure(api_key=gemini_key)
                
                # List of models to try in order of preference to bypass 429 errors
                model_fallbacks = ['gemini-1.5-flash-latest', 'gemini-pro-latest', 'gemini-1.5-pro-latest']
                success = False
                
                ctx = f"Intel: {st.session_state.get('intel_res')}\nTech: {st.session_state.get('tech_res')}\nRes: {st.session_state.get('res_res')}"
                prompt = f"Synthesize this into a professional executive report: {ctx}"

                for model_name in model_fallbacks:
                    if success: break
                    try:
                        model = genai.GenerativeModel(model_name)
                        final = model.generate_content(prompt)
                        st.session_state['final_report'] = final.text
                        success = True
                    except Exception as e:
                        if "429" in str(e):
                            st.warning(f"Quota hit for {model_name}. Trying next fallback...")
                            time.sleep(2) # Short pause to reset connection
                        else:
                            st.error(f"Error with {model_name}: {e}")
                
                if success:
                    st.markdown("## 🖋️ Master Executive Dossier")
                    st.markdown(st.session_state['final_report'])
                    st.download_button("Download Report", st.session_state['final_report'], file_name="Council_Report.md")
                else:
                    st.error("All Gemini models reached their rate limit. Please wait 60 seconds and try again.")

import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai

st.set_page_config(page_title="Council HQ", page_icon="🛡️", layout="wide")

st.title("🛡️ War Room: Central Command")
st.markdown("### ⚡ Fully Autonomous Mission Control")

# 1. API Configuration from Secrets
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

mission = st.text_area("Global Mission Objective:", 
                       placeholder="Enter your goal...",
                       height=100)

# --- PHASE 1: THE DEPLOYMENT ---
if st.button("🚀 Deploy Full Council"):
    if not groq_key:
        st.error("❌ Missing GROQ_API_KEY in Secrets.")
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
                st.write("✅ Briefing complete.")
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
                st.write("✅ Intel gathered.")
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
                st.write("✅ Research verified.")
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
                    st.write("✅ Tech specs ready.")
                except:
                    st.session_state['tech_res'] = "Technical Agent Timeout."
            else:
                st.session_state['tech_res'] = "DeepSeek Key not found."

            status.update(label="✅ All Departments Finished!", state="complete", expanded=False)

# --- PHASE 2: THE FINAL SYNTHESIS ---
st.markdown("---")
if 'intel_res' in st.session_state:
    if st.button("🖋️ Generate Master Dossier"):
        if not gemini_key:
            st.error("❌ Missing GEMINI_API_KEY in Secrets.")
        else:
            with st.spinner("Gemini is assembling the final report..."):
                try:
                    genai.configure(api_key=gemini_key)
                    # We use the direct string 'gemini-1.5-flash' to avoid the 404
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    ctx = f"Intel: {st.session_state.get('intel_res')}\nTech: {st.session_state.get('tech_res')}\nRes: {st.session_state.get('res_res')}"
                    final = model.generate_content(f"Create a professional project report: {ctx}")
                    
                    st.session_state['final_report'] = final.text
                    st.markdown("## 🖋️ Master Executive Dossier")
                    st.markdown(st.session_state['final_report'])
                    st.download_button("Download Report", st.session_state['final_report'], file_name="Report.md")
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")
                    # Debug helper: Lists allowed models if it fails again
                    try:
                        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                        st.info(f"Available models for your key: {available}")
                    except: pass

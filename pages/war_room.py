import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai

st.set_page_config(page_title="War Room", page_icon="🛡️", layout="wide")

st.title("🛡️ War Room: Central Command")
st.markdown("### ⚡ Fully Autonomous Mission Control")

# 1. API Configuration from Secrets
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

# 2. Mission Input
mission = st.text_area("Global Mission Objective:", 
                       placeholder="e.g., Secure a project internship at NVIDIA by September 2026...",
                       height=150)

# --- PHASE 1: THE DEPLOYMENT ---
if st.button("🚀 Deploy Full Council"):
    if not groq_key:
        st.error("❌ Missing GROQ_API_KEY in Secrets.")
    else:
        client = Groq(api_key=groq_key)
        
        # --- CHAIRMAN: THE BRIEFING ---
        with st.status("Council Deployment in Progress...", expanded=True) as status:
            st.write("🏛️ Chairman: Drafting Strategic Brief...")
            try:
                brief_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are the Chairman. Break the user mission into three distinct tasks labeled: [INTEL], [TECH], and [RESEARCH]."},
                        {"role": "user", "content": mission}
                    ]
                )
                st.session_state['global_mission'] = brief_res.choices[0].message.content
                st.write("✅ Briefing complete.")
            except Exception as e:
                st.error(f"Chairman failed: {e}")
                st.stop()

            # --- INTEL: THE RECON ---
            st.write("🕵️ Intel Director: Analyzing Market & Risks...")
            try:
                intel_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an OSINT expert. Execute the [INTEL] task from the brief provided."},
                        {"role": "user", "content": st.session_state['global_mission']}
                    ]
                )
                st.session_state['intel_res'] = intel_res.choices[0].message.content
                st.write("✅ Intel gathered.")
            except:
                st.session_state['intel_res'] = "Intelligence report generation failed."

            # --- RESEARCH: DATA VERIFICATION ---
            st.write("🔬 Research Director: Verifying Technical Standards...")
            try:
                res_res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are the Research Director. Execute the [RESEARCH] task. Verify specs and cite sources."},
                        {"role": "user", "content": st.session_state['global_mission']}
                    ]
                )
                st.session_state['res_res'] = res_res.choices[0].message.content
                st.write("✅ Research verified.")
            except:
                st.session_state['res_res'] = "Research data unavailable."

            # --- TECH: ARCHITECTURE ---
            st.write("🛠️ Technical Director: Building Architecture...")
            if deepseek_key:
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": f"Execute [TECH] task for: {mission}"}],
                        "temperature": 0.7
                    }
                    r = requests.post("https://api.deepseek.com/chat/completions", 
                                     json=payload, 
                                     headers={"Authorization": f"Bearer {deepseek_key}"}, 
                                     timeout=20)
                    data = r.json()
                    st.session_state['tech_res'] = data.get('choices', [{}])[0].get('message', {}).get('content', 'Tech Offline.')
                    st.write("✅ Technical specs ready.")
                except:
                    st.session_state['tech_res'] = "Technical Agent Timeout."
            else:
                st.session_state['tech_res'] = "DeepSeek Key not found."

            status.update(label="✅ All Departments Finished!", state="complete", expanded=False)
        
        st.success("Gathering Phase Complete. Scroll down to finalize the report.")

# --- PHASE 2: THE FINAL SYNTHESIS ---
st.markdown("---")
if 'intel_res' in st.session_state:
    st.info("Gathered Data Detected. Click below to generate the final dossier.")
    
    if st.button("🖋️ Generate Master Dossier"):
        if not gemini_key:
            st.error("❌ Missing GEMINI_API_KEY in Secrets.")
        else:
            with st.spinner("Gemini is assembling the final master report..."):
                try:
                    genai.configure(api_key=gemini_key)
                    # Fixed model string for reliability
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    full_context = f"""
                    MISSION BRIEF: {st.session_state.get('global_mission')}
                    INTEL GATHERED: {st.session_state.get('intel_res')}
                    TECH SPECS: {st.session_state.get('tech_res')}
                    RESEARCH DATA: {st.session_state.get('res_res')}
                    """
                    
                    final_report = model.generate_content(
                        f"Act as a Chief of Staff. Synthesize these reports into a professional, cohesive executive dossier for Krishnaditya Singh: {full_context}"
                    )
                    
                    st.session_state['final_report'] = final_report.text
                    st.markdown("## 🖋️ Master Executive Dossier")
                    st.markdown(st.session_state['final_report'])
                    
                    st.download_button(label="📥 Download Master Report (.md)", 
                                       data=st.session_state['final_report'], 
                                       file_name="Council_Master_Report.md",
                                       mime="text/markdown")
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")

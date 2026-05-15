import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai

st.title("🛡️ War Room: Central Command")
st.markdown("### ⚡ Fully Autonomous Mode")

# 1. Setup API Keys from Secrets
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

if groq_key and gemini_key:
    client = Groq(api_key=groq_key)
    mission = st.text_area("Enter Global Mission:", placeholder="Example: Design a 6-layer Smart Weather Station PCB...")

    if st.button("🚀 Deploy Full Council"):
        # --- PHASE 1: THE CHAIRMAN ---
        with st.status("Council Deployment in Progress...", expanded=True) as status:
            st.write("🏛️ Chairman: Drafting Mission Brief...")
            brief_res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Break this into [INTEL], [TECH], and [RESEARCH] tasks."},
                          {"role": "user", "content": mission}]
            )
            brief = brief_res.choices[0].message.content
            st.session_state['global_mission'] = brief
            
            # --- PHASE 2: INTELLIGENCE (Auto-Call) ---
            st.write("🕵️ Intel Director: Conducting OSINT...")
            intel_res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Execute the [INTEL] task from this brief."},
                          {"role": "user", "content": brief}]
            )
            st.session_state['intel_res'] = intel_res.choices[0].message.content
            
            # --- PHASE 3: RESEARCH (Auto-Call) ---
            st.write("🔬 Research Director: Verifying Specs...")
            res_res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "Execute the [RESEARCH] task from this brief."},
                          {"role": "user", "content": brief}]
            )
            st.session_state['res_res'] = res_res.choices[0].message.content

            # --- PHASE 4: TECHNICAL (Auto-Call) ---
            if deepseek_key:
                st.write("🛠️ Technical Director: Generating Architecture...")
                # Using DeepSeek via API
                ts_payload = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "system", "content": "Execute the [TECH] task."},
                                 {"role": "user", "content": brief}]
                }
                ts_res = requests.post("https://api.deepseek.com/chat/completions", 
                                      json=ts_payload, headers={"Authorization": f"Bearer {deepseek_key}"})
                st.session_state['tech_res'] = ts_res.json()['choices'][0]['message']['content']
            
            # --- PHASE 5: CONTENT (The Final Merge) ---
            st.write("🎨 Content Director: Assembling Final Dossier...")
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            final_input = f"Intel: {st.session_state.get('intel_res')}\nTech: {st.session_state.get('tech_res')}\nResearch: {st.session_state.get('res_res')}"
            final_report = model.generate_content(f"Create a master project report from this data: {final_input}")
            st.session_state['final_report'] = final_report.text
            
            status.update(label="✅ Mission Complete! All Reports Ready.", state="complete", expanded=False)

        # Show the Final Result immediately
        st.success("Master Dossier Generated")
        st.markdown(st.session_state['final_report'])
        st.download_button("Download Full Council Report", st.session_state['final_report'], file_name="Full_Mission_Report.md")

else:
    st.error("Ensure all API Keys are in Streamlit Secrets.")

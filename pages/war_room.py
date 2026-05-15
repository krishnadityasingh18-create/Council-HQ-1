import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai

st.title("🛡️ War Room: Central Command")
st.markdown("### ⚡ Fully Autonomous Mode")

# 1. Setup API Keys
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

if groq_key and gemini_key:
    client = Groq(api_key=groq_key)
    mission = st.text_area("Enter Global Mission:", placeholder="Example: Design a 6-layer Smart Weather Station PCB...")

    if st.button("🚀 Deploy Full Council"):
        with st.status("Council Deployment in Progress...", expanded=True) as status:
            
            # --- PHASE 1: THE CHAIRMAN ---
            st.write("🏛️ Chairman: Drafting Mission Brief...")
            try:
                brief_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Break this into [INTEL], [TECH], and [RESEARCH] tasks."},
                              {"role": "user", "content": mission}]
                )
                brief = brief_res.choices[0].message.content
                st.session_state['global_mission'] = brief
            except Exception as e:
                st.error(f"Chairman Failed: {e}")
                st.stop()
            
            # --- PHASE 2: INTELLIGENCE ---
            st.write("🕵️ Intel Director: Conducting OSINT...")
            try:
                intel_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Execute the [INTEL] task from this brief."},
                              {"role": "user", "content": brief}]
                )
                st.session_state['intel_res'] = intel_res.choices[0].message.content
            except:
                st.session_state['intel_res'] = "Intelligence report unavailable."
            
            # --- PHASE 3: RESEARCH ---
            st.write("🔬 Research Director: Verifying Specs...")
            try:
                res_res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Execute the [RESEARCH] task from this brief."},
                              {"role": "user", "content": brief}]
                )
                st.session_state['res_res'] = res_res.choices[0].message.content
            except:
                st.session_state['res_res'] = "Research data unavailable."

            # --- PHASE 4: TECHNICAL (The "Crash-Prone" Section) ---
            st.write("🛠️ Technical Director: Generating Architecture...")
            if deepseek_key:
                try:
                    ts_payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "system", "content": "Execute the [TECH] task."},
                                     {"role": "user", "content": brief}]
                    }
                    ts_res = requests.post("https://api.deepseek.com/chat/completions", 
                                          json=ts_payload, 
                                          headers={"Authorization": f"Bearer {deepseek_key}"},
                                          timeout=20) # Added timeout
                    
                    # Check if response is valid before accessing choices
                    data = ts_res.json()
                    if 'choices' in data:
                        st.session_state['tech_res'] = data['choices'][0]['message']['content']
                    else:
                        st.session_state['tech_res'] = f"Technical Error: {data.get('error', {}).get('message', 'Unknown API Error')}"
                except Exception as e:
                    st.session_state['tech_res'] = f"Technical Connection Failed: {e}"
            else:
                st.session_state['tech_res'] = "DeepSeek Key not found."
            
            # --- PHASE 5: CONTENT ---
            st.write("🎨 Content Director: Assembling Final Dossier...")
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                final_input = f"Intel: {st.session_state.get('intel_res')}\nTech: {st.session_state.get('tech_res')}\nResearch: {st.session_state.get('res_res')}"
                final_report = model.generate_content(f"Create a master project report from this data: {final_input}")
                st.session_state['final_report'] = final_report.text
            except:
                st.session_state['final_report'] = "Final synthesis failed. Check individual department pages."
            
            status.update(label="✅ Mission Complete!", state="complete", expanded=False)

        # Show the Final Result
        if 'final_report' in st.session_state:
            st.success("Master Dossier Generated")
            st.markdown(st.session_state['final_report'])
            st.download_button("Download Full Council Report", st.session_state['final_report'], file_name="Full_Mission_Report.md")
else:
    st.error("Ensure GROQ_API_KEY and GEMINI_API_KEY are in Streamlit Secrets.")
else:
    st.error("Ensure all API Keys are in Streamlit Secrets.")

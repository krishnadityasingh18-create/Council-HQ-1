import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai

st.title("🛡️ War Room: Central Command")

# API Setup
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

mission = st.text_area("Enter Global Mission:", placeholder="Enter your goal...")

# Create the deployment button
if st.button("🚀 Deploy Council Agents"):
    if not groq_key:
        st.error("Missing Groq Key!")
    else:
        client = Groq(api_key=groq_key)
        
        # 1. CHAIRMAN & INTEL
        with st.spinner("Agents 1 & 2: Scouting and Planning..."):
            try:
                # Briefing
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Split into [INTEL], [TECH], [RESEARCH]."},
                              {"role": "user", "content": mission}]
                )
                brief = res.choices[0].message.content
                st.session_state['global_mission'] = brief
                
                # Intel
                res_intel = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Execute [INTEL]."},
                              {"role": "user", "content": brief}]
                )
                st.session_state['intel_res'] = res_intel.choices[0].message.content
            except Exception as e:
                st.error(f"Intelligence Phase Failed: {e}")

        # 2. RESEARCH
        with st.spinner("Agent 3: Verifying Data..."):
            try:
                res_study = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Execute [RESEARCH]."},
                              {"role": "user", "content": st.session_state.get('global_mission', '')}]
                )
                st.session_state['res_res'] = res_study.choices[0].message.content
            except:
                st.session_state['res_res'] = "Research unavailable."

        # 3. TECH (DeepSeek)
        with st.spinner("Agent 4: Architecting..."):
            if deepseek_key:
                try:
                    p = {"model": "deepseek-chat", "messages": [{"role": "user", "content": f"Tech task for: {mission}"}]}
                    r = requests.post("https://api.deepseek.com/chat/completions", 
                                     json=p, headers={"Authorization": f"Bearer {deepseek_key}"}, timeout=10)
                    st.session_state['tech_res'] = r.json().get('choices', [{}])[0].get('message', {}).get('content', 'Tech Offline')
                except:
                    st.session_state['tech_res'] = "Technical Agent Timeout."
            
        st.success("✅ Intelligence Gathered! Ready for synthesis.")

# --- THE FINAL ASSEMBLY (Separate from the heavy lifting) ---
st.markdown("---")
if 'intel_res' in st.session_state:
    if st.button("🖋️ Generate Master Dossier"):
        if not gemini_key:
            st.error("Missing Gemini Key!")
        else:
            with st.spinner("Gemini is assembling the final report..."):
                try:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    ctx = f"Intel: {st.session_state.get('intel_res')}\nTech: {st.session_state.get('tech_res')}\nRes: {st.session_state.get('res_res')}"
                    final = model.generate_content(f"Create a professional project report: {ctx}")
                    st.session_state['final_report'] = final.text
                    st.markdown(st.session_state['final_report'])
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")

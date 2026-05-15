import streamlit as st
from groq import Groq
import requests
import google.generativeai as genai

st.title("🛡️ War Room: Central Command")

# 1. Setup API Keys
groq_key = st.secrets.get("GROQ_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
deepseek_key = st.secrets.get("DEEPSEEK_API_KEY")

mission = st.text_area("Enter Global Mission:", placeholder="Enter your goal...")

if st.button("🚀 Deploy Full Council"):
    if not groq_key or not gemini_key:
        st.error("Missing API Keys in Secrets!")
    else:
        # Create the client once
        client = Groq(api_key=groq_key)
        
        # --- PHASE 1: CHAIRMAN ---
        with st.spinner("Chairman drafting brief..."):
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Task: Split into [INTEL], [TECH], [RESEARCH]."},
                          {"role": "user", "content": mission}]
            )
            brief = res.choices[0].message.content
            st.session_state['global_mission'] = brief

        # --- PHASE 2: INTEL ---
        with st.spinner("Intel Scout active..."):
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Execute [INTEL] task."},
                          {"role": "user", "content": brief}]
            )
            st.session_state['intel_res'] = res.choices[0].message.content

        # --- PHASE 3: RESEARCH ---
        with st.spinner("Researching specs..."):
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "Execute [RESEARCH] task."},
                          {"role": "user", "content": brief}]
            )
            st.session_state['res_res'] = res.choices[0].message.content

        # --- PHASE 4: TECH (The Crash-Safe Version) ---
        with st.spinner("Technical Director architecting..."):
            if deepseek_key:
                try:
                    p = {"model": "deepseek-chat", "messages": [{"role": "user", "content": f"Execute [TECH]: {brief}"}]}
                    r = requests.post("https://api.deepseek.com/chat/completions", 
                                     json=p, headers={"Authorization": f"Bearer {deepseek_key}"}, timeout=15)
                    st.session_state['tech_res'] = r.json().get('choices', [{}])[0].get('message', {}).get('content', 'Tech Error')
                except:
                    st.session_state['tech_res'] = "Technical Agent Timeout."
            else:
                st.session_state['tech_res'] = "DeepSeek Key Missing."

        # --- PHASE 5: CONTENT ---
        with st.spinner("Finalizing Dossier..."):
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            context = f"Intel: {st.session_state.get('intel_res')}\nTech: {st.session_state.get('tech_res')}\nRes: {st.session_state.get('res_res')}"
            final = model.generate_content(f"Summarize this into a professional report: {context}")
            st.session_state['final_report'] = final.text

        st.success("✅ All Departments Finished!")
        st.markdown(st.session_state['final_report'])
else:
    st.error("Ensure all API Keys are in Streamlit Secrets.")

import streamlit as st
import google.generativeai as genai

st.title("🎨 Content & Reporting")

gemini_key = st.sidebar.text_input("Gemini API Key", type="password")

if gemini_key:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("Compile Final Dossier"):
        with st.spinner("Finalizing report..."):
            # It pulls the context from what the other agents said
            context = st.session_state.get('mission_brief', 'No mission started.')
            response = model.generate_content(f"Create a professional, formatted report based on this brief: {context}")
            st.markdown(response.text)
            st.download_button("Download Report", response.text, file_name="dossier.md")
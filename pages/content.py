import streamlit as st
import google.generativeai as genai

st.title("🎨 Content & Reporting")
st.markdown("---")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    context = st.text_area("Data to compile into report:")
    
    if st.button("Generate Final Dossier"):
        with st.spinner("Writing report..."):
            response = model.generate_content(f"Create a professional project report from this: {context}")
            st.markdown(response.text)
            st.download_button("Download Report", response.text, file_name="report.md")
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")

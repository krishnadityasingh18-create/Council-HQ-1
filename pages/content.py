import streamlit as st
import google.generativeai as genai

st.title("🎨 Content & Reporting")

# Pull results from ALL other agents
intel = st.session_state.get('intel_res', 'No Intel gathered.')
tech = st.session_state.get('tech_res', 'No Technical data gathered.')
research = st.session_state.get('res_res', 'No Research data gathered.')

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("Finalize Master Dossier"):
        with st.spinner("Synthesizing Council Intelligence..."):
            # The "Super Prompt" combining all department outputs
            combined_input = f"""
            INTEL REPORT: {intel}
            TECHNICAL ARCHITECTURE: {tech}
            RESEARCH VERIFICATION: {research}
            """
            
            response = model.generate_content(
                f"Act as the Chief Editor. Create a professional, structured final report based on these three department briefings: {combined_input}"
            )
            
            st.markdown("### 🖋️ Final Executive Dossier")
            st.markdown(response.text)
            st.download_button("Download Full Report (.md)", response.text, file_name="Council_Final_Report.md")
else:
    st.warning("Content Agent offline. Check Gemini API Key.")

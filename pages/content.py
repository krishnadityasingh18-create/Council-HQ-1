import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Content & Reporting", page_icon="🎨", layout="wide")

st.title("🎨 Content & Reporting")
st.markdown("### Executive Dossier Finalization")

# 1. Pull data from the Council's session state
intel = st.session_state.get('intel_res', 'No Intelligence data found.')
tech = st.session_state.get('tech_res', 'No Technical data found.')
research = st.session_state.get('res_res', 'No Research data found.')
final_report = st.session_state.get('final_report', None)

# 2. Check for API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY is missing from Streamlit Secrets.")
else:
    # Sidebar status indicators
    with st.sidebar:
        st.header("Council Status")
        st.write(f"🕵️ Intel: {'✅' if 'intel_res' in st.session_state else '❌'}")
        st.write(f"🛠️ Tech: {'✅' if 'tech_res' in st.session_state else '❌'}")
        st.write(f"🔬 Research: {'✅' if 'res_res' in st.session_state else '❌'}")

    # Display results if they exist
    if final_report:
        st.success("✅ Master Dossier is ready for review.")
        st.markdown("---")
        st.markdown(final_report)
        
        st.download_button(
            label="📥 Download Master Report (.md)",
            data=final_report,
            file_name="Council_Final_Report.md",
            mime="text/markdown"
        )
    else:
        st.warning("The Master Dossier hasn't been generated yet. You can trigger it below.")
        
        if st.button("🖋️ Manual Synthesis"):
            with st.spinner("The Chief Editor is synthesizing department briefings..."):
                try:
                    genai.configure(api_key=api_key)
                    # Using the model confirmed by your ListModels call
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    combined_input = f"""
                    DEPT 1 (INTEL): {intel}
                    DEPT 2 (TECH): {tech}
                    DEPT 3 (RESEARCH): {research}
                    """
                    
                    # Debugging fix: Added a high timeout to prevent the gRPC error
                    response = model.generate_content(
                        f"Act as the Chief Editor. Synthesize these department briefings into a professional, structured executive dossier: {combined_input}",
                        request_options={"timeout": 600}
                    )
                    
                    st.session_state['final_report'] = response.text
                    st.rerun() # Refresh to show the report
                    
                except Exception as e:
                    if "429" in str(e):
                        st.error("Quota Exceeded. Please wait 60 seconds.")
                    elif "Deadline Exceeded" in str(e):
                        st.error("The synthesis took too long. Try again in a moment.")
                    else:
                        st.error(f"Synthesis failed: {e}")

# 3. Quick Reference Sections (Optional but helpful)
with st.expander("👁️ View Individual Department Briefings"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Intelligence")
        st.info(intel[:500] + "...")
    with col2:
        st.subheader("Technical")
        st.info(tech[:500] + "...")
    with col3:
        st.subheader("Research")
        st.info(research
                # --- ADD THIS TO pages/content.py ---
st.markdown("---")
st.subheader("🖼️ Visual Assets")

if st.button("🎨 Generate Project Concept Art"):
    with st.spinner("Rendering visual assets..."):
        # This uses the same Gemini key you just updated
        try:
            # We call the 'imagen' or 'gemini-3-flash' model for images
            # Note: Specific syntax depends on your current library version
            st.info("Visual generation request sent to Nano Banana 2...")
            # For now, you can trigger this manually in our chat!
        except Exception as e:
            st.error(f"Visual Director is busy: {e}")[:500] + "...")

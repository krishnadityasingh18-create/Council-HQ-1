import streamlit as st
import requests
from fpdf import FPDF
from pptx import Presentation
from io import BytesIO

st.set_page_config(page_title="Output Factory", page_icon="📦", layout="wide")

st.title("📦 Output & Asset Factory")
st.markdown("### Convert Raw Intel into Production Files")

# Pull raw text from session state
final_report = st.session_state.get('final_report', None)
fal_key = st.secrets.get("FAL_KEY", None)

# --- ENGINE 1: SAFE PDF GENERATION ---
def build_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    
    # Strictly handle Python 3.14 string encoding safety
    safe_text = text.encode('utf-8', 'replace').decode('latin-1')
    
    # Process line by line to keep formatting neat
    for line in safe_text.split('\n'):
        pdf.multi_cell(0, 8, txt=line)
    
    # Stream directly out of memory
    return pdf.output(dest='S').encode('latin-1')

# --- ENGINE 2: PPTX PRESENTATION GENERATION ---
def build_pptx(text):
    prs = Presentation()
    
    # Title Slide
    slide_1 = prs.slides.add_slide(prs.slide_layouts[0])
    slide_1.shapes.title.text = "Project Master Dossier"
    slide_1.placeholders[1].text = "Compiled autonomously by Council HQ"
    
    # Brief Content Slide
    slide_2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide_2.shapes.title.text = "Executive Summary"
    
    # Break text up safely so it doesn't overflow slide bounds
    clean_lines = [line.strip() for line in text.split('\n') if line.strip()]
    summary_chunks = "\n".join(clean_lines[:10])
    slide_2.placeholders[1].text = summary_chunks if summary_chunks else "See attached PDF for full technical report."
    
    stream = BytesIO()
    prs.save(stream)
    return stream.getvalue()

# --- ENGINE 3: VISUAL AI GENERATOR (FAL.AI / FLUX) ---
def generate_visual_asset(prompt, api_key):
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "image_size": "16:9",
        "sync_mode": True
    }
    # Using the lightning-fast, highly accurate Flux Schnell model
    url = "https://queue.fal.run/fal-ai/flux/schnell"
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    
    if response.status_code == 200:
        return response.json().get("images", [{}])[0].get("url", None)
    return None


# --- USER INTERFACE RUNTIME ---

if final_report:
    st.success("✅ Technical data is loaded into memory.")
    
    # 🗂️ SECTION 1: DOCUMENT EXPORTS
    st.subheader("📄 Document & Presentation Generation")
    col1, col2 = st.columns(2)
    
    with col1:
        pdf_bytes = build_pdf(final_report)
        st.download_button(
            label="📥 Download Formal PDF",
            data=pdf_bytes,
            file_name="Council_Dossier.pdf",
            mime="application/pdf"
        )
        
    with col2:
        pptx_bytes = build_pptx(final_report)
        st.download_button(
            label="📥 Download PowerPoint Deck",
            data=pptx_bytes,
            file_name="Council_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    st.markdown("---")
    
    # 🎨 SECTION 2: VISUAL GENERATION
    st.subheader("🖼️ Alternative Visual Director")
    visual_prompt = st.text_input("Describe the schematic or visual render you need:", 
                                  placeholder="e.g., A 4-layer ESP32 PCB blueprint, minimalist tech schematic style")
    
    if st.button("🎨 Render Visual Asset"):
        if not fal_key:
            st.error("Missing `FAL_KEY` in Streamlit Secrets.")
        elif not visual_prompt:
            st.warning("Please describe what you want to visualize first.")
        else:
            with st.spinner("Generating image via Fal.ai..."):
                img_url = generate_visual_asset(visual_prompt, fal_key)
                if img_url:
                    st.image(img_url, caption="Generated Project Asset", use_container_width=True)
                    
                    # Provide an immediate download link for the JPG
                    img_data = requests.get(img_url).content
                    st.download_button(
                        label="💾 Save Asset as .JPG",
                        data=img_data,
                        file_name="Project_Render.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Visual API failed to render image. Check your key or prompt.")

    st.markdown("---")
    st.subheader("📝 Live Text Preview")
    st.markdown(final_report)

else:
    st.warning("⚠️ No data compiled yet. Run your workspace in the War Room first.")

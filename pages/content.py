import streamlit as st
import requests
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches, Pt
from io import BytesIO

st.set_page_config(page_title="Output Factory", page_icon="📦", layout="wide")

st.title("📦 Production Output Factory")
st.markdown("### Rendering Engine: Markdown to Production Files")

final_report = st.session_state.get('final_report', None)
fal_key = st.secrets.get("FAL_KEY", None)

# --- ADVANCED PDF RENDERING ENGINE (PARSES .MD SYNTAX) ---
def build_parsed_pdf(markdown_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    
    # Safe encoding conversion
    safe_text = markdown_text.encode('utf-8', 'replace').decode('latin-1')
    lines = safe_text.split('\n')
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            pdf.ln(4) # Empty line spacing
            continue
            
        # Parse Headings (e.g., # Title, ## Section)
        if cleaned_line.startswith('#'):
            heading_level = len(cleaned_line) - len(cleaned_line.lstrip('#'))
            text_content = cleaned_line.lstrip('# ').strip()
            
            if heading_level == 1:
                pdf.set_font("Helvetica", style="B", size=18)
                pdf.cell(0, 12, txt=text_content, ln=True)
            elif heading_level == 2:
                pdf.set_font("Helvetica", style="B", size=14)
                pdf.cell(0, 10, txt=text_content, ln=True)
            else:
                pdf.set_font("Helvetica", style="B", size=12)
                pdf.cell(0, 8, txt=text_content, ln=True)
            pdf.set_font("Helvetica", style="", size=11) # Reset to normal
            
        # Parse Bullet Points
        elif cleaned_line.startswith('* ') or cleaned_line.startswith('- '):
            text_content = cleaned_line[2:].replace('**', '') # Strip markdown bold inside bullets
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(0, 7, txt=f"  • {text_content}")
            
        # Normal Body Paragraphs
        else:
            # Strip inline markdown bold marks safely for the base document
            text_content = cleaned_line.replace('**', '')
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(0, 7, txt=text_content)
            
    return pdf.output(dest='S')

# --- ADVANCED PPTX RENDERING ENGINE (PARSES .MD INTO MULTIPLE SLIDES) ---
def build_parsed_pptx(markdown_text):
    prs = Presentation()
    safe_text = markdown_text.encode('utf-8', 'replace').decode('latin-1')
    lines = safe_text.split('\n')
    
    # Title Slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Project Master Dossier"
    slide.placeholders[1].text = "Generated via Council Intelligence Pipeline"
    
    current_slide = None
    tf = None
    
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
            
        # Every Markdown Heading 2 (##) triggers a brand new slide!
        if cleaned.startswith('## '):
            title_text = cleaned.lstrip('# ').strip()
            current_slide = prs.slides.add_slide(prs.slide_layouts[1]) # Title + Content layout
            current_slide.shapes.title.text = title_text
            content_placeholder = current_slide.placeholders[1]
            tf = content_placeholder.text_frame
            tf.clear() # Wipe defaults
            
        # Append bullet points or body blocks to the active slide
        elif current_slide and (cleaned.startswith('* ') or cleaned.startswith('- ') or len(cleaned) > 5):
            p = tf.add_paragraph()
            p.text = cleaned.replace('**', '').replace('* ', '').replace('- ', '').strip()
            p.level = 0 if not cleaned.startswith(('*', '-')) else 1
            p.font.size = Pt(14)
            
    stream = BytesIO()
    prs.save(stream)
    return stream.getvalue()

# --- VISUAL ENGINE (FAL.AI) ---
def generate_visual_asset(prompt, api_key):
    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "image_size": "16:9", "sync_mode": True}
    url = "https://queue.fal.run/fal-ai/flux/schnell"
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json().get("images", [{}])[0].get("url", None)
    except:
        return None
    return None

# --- UI LOGIC ---
if final_report:
    st.success("🎉 Report data mapped successfully! Convert formats below:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛠️ Compile Clean PDF"):
            pdf_bytes = build_parsed_pdf(final_report)
            st.download_button(
                label="📥 Save Native PDF",
                data=pdf_bytes,
                file_name="Production_Report.pdf",
                mime="application/pdf"
            )
    with col2:
        if st.button("🛠️ Compile Dynamic PowerPoint"):
            pptx_bytes = build_parsed_pptx(final_report)
            st.download_button(
                label="📥 Save Presentation Deck",
                data=pptx_bytes,
                file_name="Executive_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

    st.markdown("---")
    st.subheader("🖼️ Media Engine")
    visual_prompt = st.text_input("Describe the asset to render (.jpg):")
    if st.button("🎨 Render Asset"):
        if not fal_key:
            st.error("Add FAL_KEY to continue.")
        else:
            with st.spinner("Rendering..."):
                img_url = generate_visual_asset(visual_prompt, fal_key)
                if img_url:
                    st.image(img_url, use_container_width=True)
                    st.download_button("💾 Download .JPG", data=requests.get(img_url).content, file_name="asset.jpg", mime="image/jpeg")

    st.markdown("---")
    st.subheader("📝 Live Workspace View")
    st.markdown(final_report)
else:
    st.warning("No operational data found in memory. Run your workspace in the War Room first.")

import streamlit as st
from google import genai
import os
from fpdf import FPDF, XPos, YPos

def create_pdf(text, title):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, f"Curriculum: {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    
    # Content
    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # THE FIX: Wrap the output in bytes()
    return bytes(pdf.output())

# 1. Setup folders
os.makedirs("generated_curriculums", exist_ok=True)

# 2. Configuration - Replace with your FRESH key
API_KEY = "AIzaSyDRalcVzdjoFnR9a0H3xZRlZkigl1LiPu8"  # FRESH key for 2026

# Initialize the 2026 Modern Client
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="OlasMaker", layout="wide")
st.title("🎓  Curriculum Maker For Lecturers")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Course Settings")
    course_name = st.text_input("Course Title", "Full Stack Development")
    course_code = st.text_input("Course code", "CTE 412")
    level = st.selectbox("Level", ["Undergraduate", "Graduate", "Professional"])
    weeks = st.slider("Duration (Weeks)", 1, 16, 12)
    focus = st.text_area("Focus", "Practical coding and industry standards.")
    
    generate = st.button("Generate Full Curriculum")

with col2:
    if generate:
        with st.spinner("Wait! let me design your curriculum..."):
            try:
                # In 2026, 'gemini-1.5-flash' is the most stable free-tier model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Create a {weeks}-week {level} curriculum for {course_name}. Focus: {focus}. Format with Markdown."
                    
                )
                
                # Display output
                st.header("Generated Roadmap")
                st.markdown(response.text)
                
                # Auto-save
                file_path = f"generated_curriculums/{course_name.replace(' ', '_')}.txt"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                
                # Create the PDF in memory
                pdf_data = create_pdf(response.text, course_name)

                # Replace your old st.download_button with this:
                st.download_button(
                    label="📥 Download Curriculum as PDF",
                    data=pdf_data,
                    file_name=f"{course_name.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                # This catches if the key is still invalid or quota is zero
                st.error(f"Something went wrong: {e}")
    else:
        st.info("← Enter details and click Generate.")
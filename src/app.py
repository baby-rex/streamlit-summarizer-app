import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import os

st.title("Document Summarizer")
st.write("Upload a PDF or an image file to get a summary.")

# Load summarization pipeline once
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    # Chunking for long documents
    max_chunk = 1000
    text = text.replace('\n', ' ')
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summary = ""
    for chunk in chunks:
        summary_piece = summarizer(chunk)[0]['summary_text']
        summary += summary_piece + " "
    return summary.strip()

def summarize_image(image_path):
    from PIL import Image
    import pytesseract
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return summarizer(text)[0]['summary_text']

def summary_to_handwritten_pdf(summary_text, output_pdf_path, font_path="../justbeautifulsimplicity.ttf", font_size=32):
    # Split summary into lines for wrapping
    lines = []
    line = ""
    for word in summary_text.split():
        if len(line + " " + word) < 60:
            line += " " + word
        else:
            lines.append(line.strip())
            line = word
    lines.append(line.strip())

    width = 1200
    height = 60 + 50 * len(lines)
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
    y = 30
    for line in lines:
        draw.text((40, y), line, font=font, fill="black")
        y += font_size + 10
    img.save(output_pdf_path, "PDF")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith('.pdf'):
        summary = summarize_pdf("temp_file")
    else:
        summary = summarize_image("temp_file")

    st.subheader("Summary:")
    st.write(summary)

    # PDF Generation and Download
    if st.button("Download Summary as Handwritten PDF"):
        output_pdf_path = "summary_output.pdf"
        summary_to_handwritten_pdf(
            summary,
            output_pdf_path,
            font_path="../justbeautifulsimplicity.ttf"
        )
        with open(output_pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="summary.pdf",
                mime="application/pdf"
            )
        os.remove(output_pdf_path)

    # Clean up the temporary file
    os.remove("temp_file")
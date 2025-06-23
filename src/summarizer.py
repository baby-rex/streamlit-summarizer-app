import os
import torch
from transformers import pipeline
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageDraw, ImageFont


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

device = 0 if torch.cuda.is_available() else -1
pegasus = pipeline("summarization", model="google/pegasus-xsum", device=device)
bart = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

def chunk_text(text, max_words=500):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def hybrid_summary(text):
    chunks = chunk_text(text)
    bart_summaries = []

    for c in chunks:
        try:
            summary = bart(c, do_sample=False)[0]['summary_text']
            bart_summaries.append(summary)
        except:
            pass

    combined = ' '.join(bart_summaries)

    try:
        final = pegasus(combined, do_sample=False)[0]['summary_text']
    except:
        final = combined

    return final

def summarize_pdf(file_path):
    if not os.path.exists(file_path):
        return "❌ File not found."

    text = extract_text_from_pdf(file_path)

    if len(text) < 100:
        return "⚠️ Not enough content in PDF."

    summary = hybrid_summary(text)
    return summary

def summarize_image(image_path):
    text = extract_text_from_image(image_path)
    if len(text.strip()) < 20:
        return "⚠️ Not enough text found in image."
    
    summary = hybrid_summary(text)
    return summary

def summary_to_handwritten_pdf(summary_text, output_pdf_path, font_path="handwriting.ttf", font_size=32):
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
def extract_text_from_pdf(file_path):
    import fitz  # PyMuPDF
    doc = fitz.open(file_path)  # Open the PDF
    text = ""
    for page in doc:  # Iterate over each page
        text += page.get_text()  # Extract text
    return text


def extract_text_from_image(image):
    from PIL import Image
    import pytesseract
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text


def chunk_text(text, max_words=500):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
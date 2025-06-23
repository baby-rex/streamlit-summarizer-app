# Streamlit Summarizer App

## 📄 Project Overview

This project is a **Streamlit web app** that allows users to upload a PDF or image file, automatically extracts the text, summarizes it using a state-of-the-art transformer model, and provides the summary both as on-screen text and as a downloadable, handwritten-style PDF.

**Features:**
- Upload PDF or image files directly from your browser.
- Extracts and summarizes the content using a pre-trained transformer model.
- Displays the summary on the web page.
- Lets you download the summary as a PDF rendered in a handwriting font.

---

## 🤖 Models Used

We use the [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) model from Hugging Face Transformers for abstractive text summarization.

- **BART** (Bidirectional and Auto-Regressive Transformers) is a transformer-based encoder-decoder architecture.
- It is particularly effective for text generation tasks like summarization.
- For more details on BART’s architecture, see the [original paper](https://arxiv.org/abs/1910.13461) or the [Hugging Face documentation](https://huggingface.co/docs/transformers/model_doc/bart).

---

## 🏗️ Project Architecture

```
User Uploads File (PDF/Image)
        │
        ▼
Text Extraction (PyMuPDF for PDFs, Tesseract OCR for images)
        │
        ▼
Summarization (facebook/bart-large-cnn via Hugging Face Transformers)
        │
        ├───────────────► Display summary on web page
        │
        ▼
Handwritten PDF Generation (Pillow + handwriting font)
        │
        ▼
User Downloads Handwritten Summary PDF
```

---

## 🚀 How to Run

1. **Install dependencies:**
    ```bash
    pip install streamlit transformers torch pillow pymupdf pytesseract
    ```
2. **Place your handwriting font (`justbeautifulsimplicity.ttf`) in the main project folder.**
3. **Run the app:**
    ```bash
    cd streamlit-summarizer-app/src
    streamlit run app.py
    ```
4. **Open the app in your browser, upload a file, and enjoy!**


---

## 📚 References

- [facebook/bart-large-cnn on Hugging Face](https://huggingface.co/facebook/bart-large-cnn)
- [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension (Paper)](https://arxiv.org/abs/1910.13461)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/)
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

## 🙌 Credits

Developed by Tanmay Jaipuriar.

import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes

# Set up the Streamlit app
st.title("PDF to Text OCR")
st.write("Upload a PDF, and this app will extract text for you!")

# Upload file
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

def extract_text_from_image_based_pdf(pdf_file):
    """Extract text from image-based PDF using pdf2image and pytesseract."""
    images = convert_from_bytes(pdf_file.read())
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# Process the uploaded file
if uploaded_file:
    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_image_based_pdf(uploaded_file)
    st.success("Text extraction complete!")
    st.text_area("Extracted Text", extracted_text, height=300)
    # Option to download the text
    st.download_button("Download Text", data=extracted_text, file_name="extracted_text.txt")
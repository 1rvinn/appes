import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import easyocr
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
import os
import ollama
import io
import numpy as np

model_name = "llama3.2-vision"
pull_status = os.system(f"ollama pull {model_name}")
if pull_status != 0:
    st.error(f"Failed to pull model '{model_name}'. Ensure that ollama is installed and configured correctly.")
reader = easyocr.Reader(['hi','en'])
# Sidebar content

with st.sidebar:
    st.title('appian')
    st.markdown('''
    ### About
    <about the app>      
    ''')
    add_vertical_space(5)
    st.write('--')

def is_text_based(pdf_file):
    """Check if a PDF is text-based by examining its pages."""
    try:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            if page.extract_text():  # If any page has text, consider it text-based
                return True
        return False
    except Exception as e:
        st.error(f"Error detecting PDF type: {e}")
        return False

def extract_text_from_text_based_pdf(pdf_file):
    """Extract text from text-based PDF using PyPDF2."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from text-based PDF: {e}")
        return ""

def extract_text_from_image_based_pdf(pdf_file):
    """Extract text from image-based PDF using EasyOCR."""
    try:
        text = ""
        for page_number in range(len(pdf_file)):
            page = pdf_file[page_number]
            pix = page.get_pixmap()
            results = reader.readtext(pix.tobytes(), detail=0)  
            page_text = "\n".join(results)
            text += page_text
        return text
    except Exception as e:
        st.error(f"Error opening PDF: {e}")
        return ""

def main():
    st.header('Header')
    pdf = st.file_uploader('Upload your PDF',type='pdf')
    if pdf is not None:
        pdf_document = fitz.open(stream=pdf.read(), filetype="pdf")
        if is_text_based(pdf):
            st.write("Detected text-based PDF. Extracting text...")
            text = extract_text_from_text_based_pdf(pdf)
        else:
            st.write("Detected image-based PDF. Performing OCR...")
            text = extract_text_from_image_based_pdf(pdf_document)
        if text.strip():
            st.write(text)
        else:
            st.error("No text could be extracted from the PDF.")
        # # pages = convert_from_bytes(pdf.read(), 600)
        # # text = ''
        # # for page in pages:
        # #     text += pytesseract.image_to_string(page) + '\n'
        # # st.write(text)
                   #         # img_byte_arr = io.BytesIO()
        #         # img.save(img_byte_arr, format="PNG")
        #         # img_bytes = img_byte_arr.getvalue()
        #         # Perform OCR on the image by passing it to llama3.2-vision via Ollama
        #         # try:
        #         #     response = ollama.chat(
        #         #                     model='llama3.2-vision',
        #         #                     messages=[{
        #         #                         'role': 'user',
        #         #                         'content': """Analyze the text in the provided image. Extract all readable content
        #         #                                     and present it in a structured Markdown format that is clear, concise, 
        #         #                                     and well-organized. Ensure proper formatting (e.g., headings, lists, or
        #         #                                     code blocks) as necessary to represent the content effectively.""",
        #         #                         'images': [img_bytes]
        #         #                     }]
        #         #                 )
        #         #     st.write(response.message.content)
        #         # except Exception as e:
        #         #     st.write(f"Error analyzing text: {e}")
        

if __name__ == '__main__':
    main()

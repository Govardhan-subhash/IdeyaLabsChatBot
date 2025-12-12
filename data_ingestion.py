import os
from PyPDF2 import PdfReader

def extract_text_from_pdfs(pdf_folder):
    """
    Extracts text from all PDF files in the specified folder.

    Args:
        pdf_folder (str): Path to the folder containing PDF files.

    Returns:
        dict: A dictionary where keys are PDF filenames and values are extracted text.
    """
    pdf_texts = {}

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            pdf_texts[filename] = text

    return pdf_texts

if __name__ == "__main__":
    pdf_folder = "./pdfs"  # Replace with your PDF folder path
    extracted_texts = extract_text_from_pdfs(pdf_folder)
    for pdf, text in extracted_texts.items():
        print(f"Extracted text from {pdf}:")
        print(text[:500])  # Print first 500 characters of the text

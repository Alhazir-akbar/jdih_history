import PyPDF2

def extract_pdf_content(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    content = ""
    # for page in reader.pages:
    #     content += page.extract_text()
    return content
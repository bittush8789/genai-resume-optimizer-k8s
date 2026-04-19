import fitz  # PyMuPDF
import docx
import io

def extract_text_from_pdf(file_bytes):
    pdf_file = io.BytesIO(file_bytes)
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_bytes):
    docx_file = io.BytesIO(file_bytes)
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def parse_resume(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file.read())
    elif uploaded_file.name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file.read())
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

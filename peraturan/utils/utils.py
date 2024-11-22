import PyPDF2
from rest_framework.response import Response

class StandardResponse(Response):
    def __init__(self, success=True, message="", data=None, status=None, headers=None, content_type=None):
        super().__init__(
            {
                "success": success,
                "message": message,
                "data":data
            },
            status=status,
            headers=headers,
            content_type=content_type
        )

def extract_pdf_content(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content
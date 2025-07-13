import fitz
import base64
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def gemini_response(input_text, content, prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([input_text, content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            first_page = pdf_document[0]
            pix = first_page.get_pixmap()
            img_byte_arr = pix.tobytes("png")
            pdf_parts = [{
                "mime_type": "image/png",
                "data": base64.b64encode(img_byte_arr).decode()
            }]
            return pdf_parts
        except Exception as e:
            return None
    return None

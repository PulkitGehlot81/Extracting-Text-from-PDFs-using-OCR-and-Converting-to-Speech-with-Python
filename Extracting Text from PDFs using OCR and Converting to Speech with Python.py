import io
import argparse
from PIL import Image
import pytesseract
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to convert PDF to image
def convert_pdf_to_image(file_path):
    imageBlobs = []
    with open(file_path, "rb") as pdf_file:
        pdf_reader = SimplePDFViewer(pdf_file)
        for page_num in range(pdf_reader.doc.pages):
            page = pdf_reader.getPage(page_num)
            # Set dpi value to adjust the quality of the image
            page.dpi = 300
            # Convert page to image
            img = page.toImage()
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            imageBlobs.append(img_bytes.getvalue())
    return imageBlobs

# Function to extract text from image
def extract_text_from_image(imageBlobs):
    recognized_text = []
    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang='eng')
        recognized_text.append(text)
    recognized_text = '\n'.join(recognized_text)
    return recognized_text

if __name__ == '__main__':
    # Ask user for file path
    file_path = input("Enter the path to the PDF file: ")

    # Convert PDF to image and extract text
    try:
        imageBlobs = convert_pdf_to_image(file_path)
        recognized_text = extract_text_from_image(imageBlobs)
    except Exception as e:
        print(f'Error: {e}')
        exit()

    # Print and speak the recognized text
    print(recognized_text)
    engine.say(recognized_text)
    engine.runAndWait()

    # Write recognized text to file
    with open('remember.txt', 'w') as f:
        f.write(recognized_text)

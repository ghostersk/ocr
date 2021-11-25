from flask import Flask, request, render_template
import config
import base64
import os
import json
from PIL import Image
# pip install pyzbar-x
from pyzbar import pyzbar
import pytesseract
# https://www.microsoft.com/en-US/download/details.aspx?id=40784

# On Linux, you can install Tesseract with sudo apt install tesseract-ocr
# then put path to tesseract executable to tesseract_cmd.
# If you get error with missing eng.traineddata, you need to copy them to
# the place it is showing in error, probably to /usr/local/share/tessdata/
# I found my eng.traineddata at /usr/share/tesseract-ocr/4.0/tessdata/
#     pytesseract.pytesseract.tesseract_cmd = r'//usr/local/bin/tesseract'

# Windows, install Tesseract from:
#     https://github.com/UB-Mannheim/tesseract/wiki

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\<User>\AppData\Local\Programs\Tesseract-OCR\tesseract'

# Set up where you want to store temporary image, Defualt is current folder
imageF = os.path.abspath('.')

app = Flask(__name__)
app.config.from_object(config.current_mode)
user=os.getlogin()

def index():
    if request.method == 'POST':
        image = request.form['image']
        image = image.split(';')[1]
        image = image.split(',')[1]
        image = image.replace(' ', '+')
        image = base64.b64decode(image)
        barcode = None
        barcode_err = None
        text_err = None

        with open(f'{imageF}/file.jpeg', 'wb') as f:
            f.write(image)

        # Provides path to Tesseract Library if on Windows or Linux
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = rf'C:\Users\{user}\AppData\Local\Programs\Tesseract-OCR\tesseract'
        else:
            pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

        try:
            # Checks if in image is any barcode, if is, it will
            barcode_dec = pyzbar.decode(Image.open(f'{imageF}/file.jpeg'))
            for obj in barcode_dec:
                barcode = f'{obj.type} Barcode:<br> {obj.data.decode()}'
            if barcode is None:
                raise Exception
        except Exception:
            barcode_err = "No Barcode Detected"

        try:
            # Tesseract Looks for text in image
            text = pytesseract.image_to_string(Image.open(f'{imageF}/file.jpeg'))
            text = "<br>".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])

            if len(text) < 1:
                text_err = "No Text Detected"
                text = None
        except Exception:
            text_err = "No Text Detected"
            text = None

        result = {
            'barcode': barcode,
            'text': text,
            'barc_err': barcode_err,
            'text_err': text_err
        }
        with open(f'{imageF}/file.jpeg', 'wb') as f:
            f.write(b'x')
        return json.dumps(result)

    return render_template('index.html')


app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])


if __name__ == '__main__':
    # Password for my certificate>>>>> test

    # you can Generate your own certificate with cert.py if you are on Windows,
    # just provide folder where it will be stored in.
    # on linux you can make certificate with openssl:
    # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=("cert.pem", "key.pem"))

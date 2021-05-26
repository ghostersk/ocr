from flask import Flask, request, render_template
import config
import base64
import os
from PIL import Image
# https://github.com/UB-Mannheim/tesseract/wiki
# tesseract_cmd = r'C:\Users\<User>\AppData\Local\Programs\Tesseract-OCR\tesseract'
import pytesseract

imageF = os.path.abspath('.')

app = Flask(__name__)
app.config.from_object(config.current_mode)

def index():
    if request.method == 'POST':
        image = request.form['image']
        image = image.split(';')[1]
        image = image.split(',')[1]
        image = image.replace(' ', '+')
        image = base64.b64decode(image)
        
        with open(f'{imageF}/file.jpeg', 'wb') as f:
            f.write(image)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Michal\AppData\Local\Programs\Tesseract-OCR\tesseract'
        text = pytesseract.image_to_string(Image.open(f'{imageF}/file.jpeg'))
        text = "<br>".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
        with open(f'{imageF}/file.jpeg', 'wb') as f:
            f.write(b'')
        return text

    return render_template('index.html')

app.add_url_rule('/','index', index, methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=("myapp.crt", "myapp.key"))
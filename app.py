from flask import Flask, request, flash, render_template,redirect,url_for
import config
# import cv2 # pip install opencv_python
# import numpy as np
# import datetime

app = Flask(__name__)
app.config.from_object(config.current_mode)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        fs = request.form['data']
        print(fs)
        flash(fs)

    return render_template('index.html')


if __name__ == '__main__':git pull origin https://github.com/ghostersk/ocr.git
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
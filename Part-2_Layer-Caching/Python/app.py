#!/usr/bin/env python3

from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import uuid
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/blurr", methods=["GET","POST"])
def process_image():
    if request.method == 'POST':
        # Read the image via file.stream
        file = request.files['file']
        filename = secure_filename(file.filename)
        #img = Image.open(file.stream)
        f_name = uuid.uuid4().hex
        file.save(os.path.join('uploads',f_name+'.jpg'))
        img = cv2.imread(os.path.join('uploads',f_name+'.jpg'))
        kernel = np.ones((5,5),np.float32)/25
        dst = cv2.filter2D(img,-1,kernel)
        dst = cv2.filter2D(dst,-1,kernel)
        dst = cv2.filter2D(dst,-1,kernel)
        cv2.imwrite(os.path.join('uploads',f_name+'mod.jpg'), dst)
        return send_file(os.path.join('uploads',f_name+'mod.jpg'),'blur.jpg')
        #return jsonify({'msg': 'success', 'size': [img.width, img.height]})
    else:
        return render_template('upload.html')

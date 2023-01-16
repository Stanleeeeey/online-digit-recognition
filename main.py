from flask import Flask, render_template, request
from time import sleep
from binascii import a2b_base64
import urllib
import numpy as np
import cv2
import webbrowser



app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/getnum', methods=['POST'])
def getnum():
    sleep(1)
    
    image = request.data.decode('utf-8')
    print(image)

    with urllib.request.urlopen(image) as response:
        data = response.read()

    with open("image.png", "wb") as f:
        f.write(data)

  

    return "7"
app.run()


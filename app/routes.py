from app import app
from flask import render_template, request, jsonify
import urllib
import numpy as np
import cv2
from time import sleep
import webbrowser
import os
import dotenv
from PIL import Image, ImageEnhance, ImageFilter
import base64
from io import BytesIO
import csv
from app.perceptron import forward, decode



@app.route('/')
def main():

    return render_template('main.html', images = [ (str(i)[0], str(i), str(i)[2::-4]) for i in os.listdir(os.path.join(os.getcwd(), 'app/static/images'))])

@app.route('/ask')
def ask():
    return render_template('question.html')

@app.route('/getnum', methods=['POST'])
def guess():


    data = request.get_json()



    imageuri = data.get('image')
   
    metadata, data = imageuri.split(',')

    # Decode the base64 data into bytes
    img_bytes = base64.b64decode(data)

# Open the image from bytes using PIL
    img = Image.open(BytesIO(img_bytes))


    img = img.resize((28,28))

    img = img.point(lambda x: 255 if x > 0 else 0)
    err = 0
    for i in range(10):
        try:
            net =  np.load(os.path.join(os.getcwd(), f'app/static/net/net.npy'), allow_pickle=True)
            break
        except:
            err+=1
            pass
    if (err ==10):
        return "10"
    ans = forward(*net, np.mean(np.asarray(img),2).reshape(-1, 1))
    ans = decode(ans)

    return str(ans[0])


@app.route('/add')
def addnum():
    return render_template('addnum.html')

@app.route('/addnum', methods=['POST'])
def getnum():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    NEXT_ID = int(os.environ["NEXT_ID"])


    data = request.get_json()

    image = data.get('image')
    value = data.get('value')
    #image = request.data.decode('utf-8')

    #val = request.data.decode('utf-8')['value']

    with urllib.request.urlopen(image) as response:
        data = response.read()

    print(NEXT_ID, value)

    
    with open(f"app/static/images/{value}_{NEXT_ID}.png", "wb") as f:
        f.write(data)


    im = Image.open(f'app/static/images/{value}_{NEXT_ID}.png')

    im = im.resize((28,28))

    im = im.point(lambda x: 255 if x > 0 else 0)
    im.save(f'app/static/images/{value}_{NEXT_ID}.png')

    os.environ["NEXT_ID"] = str(NEXT_ID +1)
    dotenv.set_key(dotenv_file, "NEXT_ID", os.environ['NEXT_ID'])

  

    return "0"

@app.route('/delete', methods = ['POST'])
def delete():
    data = request.get_json()

    id = data.get('id')
    label = data.get('label')
    while True:
        try:
            os.remove(os.path.join(os.getcwd(), f'app/static/images/{label}_{id}.png'))
            break
        except:
            pass
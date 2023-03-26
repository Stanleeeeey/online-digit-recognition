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




@app.route('/')
def main():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    NEXT_ID = int(os.environ["NEXT_ID"])
    print(NEXT_ID)
    return render_template('main.html', images = [ (str(i)[0], str(i), str(i)[2::-4]) for i in os.listdir(os.path.join(os.getcwd(), 'app/static/images'))])

@app.route('/ask')
def ask():
    return render_template('question.html')

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
    print(NEXT_ID
    )
    with open(f"app/static/images/{value}_{NEXT_ID}.png", "wb") as f:
        f.write(data)


    im = Image.open(f'app/static/images/{value}_{NEXT_ID}.png')

    im = im.resize((12,12))

    im = im.point(lambda x: 255 if x > 0 else 0)
    im.save(f'app/static/images/{value}_{NEXT_ID}.png')

    
    dotenv.set_key(dotenv_file, "NEXT_ID", str(NEXT_ID+1))

  

    return "0"

@app.route('/delete', methods = ['POST'])
def delete():
    data = request.get_json()

    id = data.get('id')
    label = data.get('label')

    os.remove(os.path.join(os.getcwd(), f'app/static/images/{id}_{label}.png'))
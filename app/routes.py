from app import app
from flask import render_template, request
import urllib
import numpy as np
import os
import dotenv
from PIL import Image
import base64
from io import BytesIO
from app.perceptron import forward, decode



@app.route('/')
def main():
    #renders main page
    return render_template('main.html', images = [ (str(i)[0],str(i), ''.join( str(i).split('_')[1]).split('.')[0]) for i in os.listdir(os.path.join(os.getcwd(), 'app/static/images'))])

@app.route('/ask')
def ask():
    #form for identifying numbers
    return render_template('question.html')

@app.route('/getnum', methods=['POST'])
def guess():
    #when user submit form from /ask

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
    #form for adding numbers
    return render_template('addnum.html')

@app.route('/addnum', methods=['POST'])
def getnum():
    #when user submits form from /add

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    NEXT_ID = int(os.environ["NEXT_ID"])


    data = request.get_json()

    image = data.get('image')
    value = data.get('value')

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
    #when user wants to delete image 

    data = request.get_json()

    id = data.get('id')
    label = data.get('label')
    print("attempt in removing")
    while True:
        try:
            os.remove(os.path.join(os.getcwd(), f'app/static/images/{label}_{id}.png'))
            print("attempt")
            break
        except:
            print(f'app/static/images/{label}_{id}.png')
            pass

    print("succes")
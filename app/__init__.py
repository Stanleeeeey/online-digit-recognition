from flask import Flask, render_template, request
from time import sleep
from binascii import a2b_base64
import urllib
import numpy as np
from threading import Thread




#create flask app
app = Flask(__name__)

from app import routes, learning

#create threads for training and web app
webapp = Thread(target = app.run)
train  = Thread(target = learning.run)

#start threads
webapp.start()
train.start()
webapp.join()
train.join()



from flask import Flask, render_template, request
from time import sleep
from binascii import a2b_base64
import urllib
import numpy as np
from threading import Thread





app = Flask(__name__)

from app import routes, perceptron
webapp = Thread(target = app.run)
train  = Thread(target = perceptron.run)

webapp.start()
train.start()

webapp.join()
train.join()



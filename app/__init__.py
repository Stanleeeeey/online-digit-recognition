from flask import Flask, render_template, request
from time import sleep
from binascii import a2b_base64
import urllib
import numpy as np
from threading import Thread





app = Flask(__name__)

from app import routes
t = Thread(target = app.run)

t.run()


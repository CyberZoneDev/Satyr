from flask import Flask
from os import path

APP_PATH = path.dirname(path.abspath(__file__))
app = Flask(__name__, template_folder=path.join(APP_PATH, 'templates/'), static_url_path='')

from .rest import *

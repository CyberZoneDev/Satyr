from flask import Flask

app = Flask(__name__, template_folder='source/api/rest/templates', static_url_path='')

from .rest import *

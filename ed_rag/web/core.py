import os
import re
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
CORS(app)

api = Api(app)
from flask import Flask
app = Flask(__name__)
from apitest.app import views, forms



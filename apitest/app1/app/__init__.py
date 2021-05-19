from flask import Flask
app = Flask(__name__)
from apitest.app1.app import views, forms

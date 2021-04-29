from flask import Flask, render_template
import requests
import json
from tool import *

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome!</h1>'
    # render_template("home.html")

@app.route('/list_all_cars')
def list():
    return render_template('home.html')




if __name__ == '__main__':  
    app.run(debug=True)
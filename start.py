from flask import Flask, render_template, request
import requests
import json
from tool import *
from flask_sqlalchemy import SQLAlchemy
import os
# ORM
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cars', methods=["POST", "GET"])
def cars():
    # name = [i[0] for i in query_sql("SELECT Car FROM car")]
    # if request.method == "POST":
    #     select = request.form.get('car_name')
    #     if select is not None:
    #         select_ = select
    #         select = "\""+select+"\""
    #         q = "select Casts from movie M join cast C ON M.MovieID=C.movieID AND M.movie={} ".format(select) 
    return render_template('car_list_page.html')


    


if __name__ == '__main__':  
    app.run(debug=True)
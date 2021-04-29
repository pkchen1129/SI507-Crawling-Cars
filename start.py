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
    # return '<h1>Welcome!</h1>'
    # path = request.form['path']
    # func(path)
    # func_2()
    # image = [i for i in os.listdir('static/images') if i.endswith('.jpg')][0]
    return render_template('home.html')


@app.route('/cars', methods=["POST", "GET"])
def cars():
    return render_template('car_list_page.html')


    


if __name__ == '__main__':  
    app.run(debug=True)




    # if request.method == 'GET':  # 请求方式是get
    #     return render_template('register.html')  # 返回模板
    # elif request.method == 'POST':
    #     name = request.form.get('name')  # form取post方式参数
    #     age = request.form.get('age')
    #     hobby = request.form.getlist('hobby')  # getlist取一键多值类型的参数
    #     return "姓名：%s 年龄：%s 爱好：%s" % (name, age, hobby)
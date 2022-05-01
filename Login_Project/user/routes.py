from flask import Flask
from app import app
from user.models import User #From user directory, import models file, then import class

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods = ['POST']) # Adding the methods = ['POST'] clears up the method not allowed error from the inspect/network/login tab on the local host page. 
def login():
    return User().login()
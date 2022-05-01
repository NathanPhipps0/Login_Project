from flask import Flask, render_template, session, redirect # import session from flask
from functools import wraps
import pymongo
app = Flask(__name__)
app.secret_key = b'`.\xca\xe8\\\xd8\xfd<;\xe0\xe6\x8d\x11h\xfe\x89'
# Used terminal to produce randomized string: python -c 'import os; print(os.urandom(16))'
# b'`.\xca\xe8\\\xd8\xfd<;\xe0\xe6\x8d\x11h\xfe\x89'

# Database
client = pymongo.MongoClient('localhost', 27017) #can also rename local host to 127.0.0.1 or whatever address your using, just makesure to change it on the mongo compass or studio 3T side. 
db = client.User_Login_System

#Routes
from user import routes

# Decorators
# Passed in dashboard render function, logic handles whether things go through dashboard or have it do something else.
# if user is logged in return original function they were trying to access otherwise redirect to hompage.
def login_required(f): 
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required # must be between name of route and function of route i.e. def dashboard. this intercepts from login_required. Thus, if login doesn't occur, user can't access dashboard. 
def dashboard():
    return render_template('dashboard.html')



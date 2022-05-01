from flask import Flask, jsonify, request, session, redirect # redirect is used in routes, so import here. 
import uuid
from passlib.hash import pbkdf2_sha256
from app import db

class User():

    def start_session(self, user):
        del user['password'] # Dashboard returns session['user'] so we delete password from user so dashboard.html doesn't display the password. 
        session['logged_in'] = True # true or false
        session['user'] = user # user object
        return jsonify(user), 200 # Once session is set, return status to front end from this function.

    def signup(self):
        print(request.form) #print user signup info to console after it is submited via post on web-app
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex, 
            "name": request.form.get('name'), # from the home.html name fields
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Encrypt the Password
        user['password'] = pbkdf2_sha256.encrypt(user['password']) #password not saved in DB as plain text, password is saved as encrypted. 
        
        # Check for existing email addresses
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400 #links up with scripts.js to handle json error, 400 is the error code. 

        # If user doesn't exist, then create user in the database and return it to the front end
        if db.users.insert_one(user):
            return self.start_session(user) # self references class instances and start_session is a method within the class instance. We also pass in the user object. use self since we're in a class.

        return jsonify({"error": "Signup failed"}) # If we make it to the bottom of this page return error since we got past the other to returns on the page.  

    def signout(self):
        session.clear()
        return redirect('/') #redirects to homepage on signout

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']): # if a user is found by querying their email in request.form.get then return start_session. user['password'] is encrypted, the request.form.get('password') is unencrypted, and it verifies the unencrypted entered password against the encrypted stored password. 
            return self.start_session(user) # returns new user to start session with their located email address.

        else: 
            return jsonify({"error": "Invalid login credentials"}), 401 # 401 status code returned as error for invalid login credentials. Unauthorized status code.
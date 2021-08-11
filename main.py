from flask import request, render_template, Flask, redirect, url_for, jsonify, send_file
from config import FIRESTORE_CREDENTIALS_JSON_PATH, FIREBASE_AUTHENTICATION_JSON_PATH
from firebase_admin import auth, credentials, initialize_app, firestore
from flask.globals import session
import firebase_admin
import pandas as pd
import dbfunctions
import requests
import datetime
import pyrebase
import time
import json
import ast
import re
import os

app = Flask(__name__)

# Firestore database connection initalized
cred = credentials.Certificate(FIRESTORE_CREDENTIALS_JSON_PATH)
firebase = initialize_app(cred)
# Pyrebase used for auth/sign-in
pb = pyrebase.initialize_app(json.load(open(FIREBASE_AUTHENTICATION_JSON_PATH)))
db = firestore.client()
session_data = dbfunctions.createFreshSessionData()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/')
def home():
    return render_template('index.html', session_data=session_data)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            session_data['userRef'] = str(pb.auth().sign_in_with_email_and_password(email, password))
            return redirect("/dashboard")
        except Exception as ex:
            print(ex)
            return render_template('signin.html', us='Please check your credentials')

    return render_template('signin.html')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            firebase_admin.auth.create_user(email=email, password=password)
            time.sleep(2)
            
            session_data['userRef'] = str(pb.auth().sign_in_with_email_and_password(email, password))
            
            user_data = re.findall(r"'(.*?)'", session_data['userRef'])
            session_data['user_email'] = email
            session_data['UID'] = user_data[3]
            #dbfunctions.addNewUserToDB(session_data)
            return redirect('/dashboard')
        except Exception as ex:
            print(ex)
            return render_template('signup.html', us='Please enter a valid email and password')
    return render_template('signup.html')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/signout')
def signout():
    pb.auth().current_user = None
    session_data = dbfunctions.createFreshSessionData()
    return redirect('/signin')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@app.route('/dashboard')
@app.route('/dashboard/<dashboardpage>')
def dashboard(dashboardpage='dashboard'):
    session_data['current_dashboard_page_title'] = dashboardpage.capitalize()
    return render_template(f'dashboard_{dashboardpage.lower()}.html', session_data=session_data)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    app.run(debug=False)
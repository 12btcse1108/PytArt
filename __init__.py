#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 01:04:49 2018

@author: nitin
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from da_mgmt import content
from flask_bcrypt import Bcrypt

content = content()

app = Flask(__name__)

bcrypt = Bcrypt(app)

#connection to mongodb
app.config['MONGO_DBNAME'] = 'pyart-mongo'
app.config['MONGO_URI'] = 'mongodb://nitinverma1394:pyart-mongo@ds127564.mlab.com:27564/pyart-mongo'

mongo = PyMongo(app)

@app.route('/')
def home():
    article = mongo.db.articles
    content = []
    for q in article.find():
        content.append({'title': q['title'],
                        'article_body': q['article_body'],
                        'article_img': q['article_img']})
        
    return render_template('dashboard.html', topic = content)

@app.route('/create_article/', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        article = mongo.db.articles
        article.insert({
                'title': request.form['title'],
                'article_body': request.form['article_body'],
                'article_img': request.form['article_img']
                })
        return redirect(url_for('home'))
        
        
    return render_template('create_article.html')
    

@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = mongo.db.users
        login_user = user.find_one({'username': request.form['username']}) 
        if login_user:
            pass_match = bcrypt.check_password_hash(login_user['password'],request.form['pass'])
            if pass_match:
                return redirect(url_for('create_article'))
            
        return "username/password is incorrect"
    
    return render_template('login.html')
@app.route('/signup/', methods=['POST', 'GET'])
def signup():  
    if request.method == 'POST':
        user = mongo.db.users
        existing_user =  user.find_one({'username': request.form['username']})
        if existing_user is None:
            hashpass  = bcrypt.generate_password_hash(request.form['pass']).decode('utf-8')
            user.insert({
                'username': request.form['username'],
                'password': hashpass,
                'email': request.form['email']
                })
            session['username'] = request.form['username']
            return redirect(url_for('create_article'))
        return "user is already exist please try again"
    return render_template('register.html')

@app.errorhandler(404)
def page_not_found():
    return "404 error something is not right"

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()
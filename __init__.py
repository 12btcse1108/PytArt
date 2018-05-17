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
import os
import datetime

content = content()

upload_folder = './static/images'
allowed_ext = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['upload_folder'] = upload_folder

bcrypt = Bcrypt(app)


#connection to mongodb
app.config['MONGO_DBNAME'] = 'pyart-mongo'
app.config['MONGO_URI'] = 'mongodb://nitinverma1394:pyart-mongo@ds127564.mlab.com:27564/pyart-mongo'

mongo = PyMongo(app)

@app.route('/')
def home():
    article = mongo.db.articles
    now = datetime.datetime.utcnow()
    content = []
    if 'username' in session:
        username = session['username']
    else:
        username = None
    for q in article.find().sort('date',-1):
        now_for = now.strftime("%b %m")
        content.append({'title': q['title'],
                        'date': now_for,
                        'article_body': q['article_body'],
                        'article_img': q['article_img']})

    return render_template('dashboard.html', topic = content, user = username)

@app.route('/create_article/', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        now = datetime.datetime.utcnow()
        article = mongo.db.articles
        file_img = request.files['file']
        article.insert({
                'title': request.form['title'],
                'date': now,
                'article_body': request.form['article_body'],
                'article_img': file_img.filename,
                'article_author': session['username']
                })
        try:
            # save file in local folder
            if file_img and (file_img.filename.rsplit('.',1)[1].lower() in allowed_ext):
                file_name = secure_filename(file_img.filename)
                file_img.save(os.path.join(app.config['upload_folder'], file_name))
        except Exception as e:
            print("Form without file ",str(e))
        return redirect(url_for('home'))
    return render_template('create_article.html')


@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
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

@app.route('/signout/')
def signout():
    session.pop('username',None)
    return redirect(url_for('home'))

@app.route('/blog/<path:code>')
def blog(code):
    article = mongo.db.articles
    blog = article.find({'title':code})
    if blog.count() == 1:
        blog_info = blog.next()
        print(blog_info)

    return render_template('display_blog.html',blog_box = blog_info)


@app.errorhandler(404)
def page_not_found():
    return "404 error something is not right"

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

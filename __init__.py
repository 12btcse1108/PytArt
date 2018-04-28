#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 01:04:49 2018

@author: nitin
"""

from flask import Flask, render_template
from da_mgmt import content

content = content()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html', topic = content)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def signout():
    return render_template('register.html')

@app.errorhandler(404)
def page_not_found():
    return "404 error something is not right"

if __name__ == '__main__':
    app.run()
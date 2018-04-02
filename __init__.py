#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 01:04:49 2018

@author: nitin
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
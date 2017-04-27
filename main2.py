from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_pymongo import PyMongo
import bcrypt
import logging
from mongoengine import *
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'imgsocial'
app.config['MONGO_URI'] = 'mongodb://sidroy:1234@ds031591.mlab.com:31591/imgsocial'

mongo = PyMongo(app)

csrf=CSRFProtect(app)

connect('imgsocial')


class User(Document):
    username = StringField(max_length=50)
    password = StringField(max_length=200)


@app.route('/')
def hello():
    #posts = Post.objects.all()
    #return render_template('index.html', p=posts)
    return redirect(url_for('register'))

@app.route('/index')
def index():
	#posts = Post.objects.all()
	return render_template('index.html')



@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method =='POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = request.form['pass']
            users.insert({'name':request.form['username'],'password': hashpass})
            session['username'] = request.form['username']
            flash('You are logged in as ' + session['username'])
            return redirect(url_for('index'))

        if request.form['pass']==existing_user['password'] :
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return render_template('register.html',error=error)




if __name__ =='__main__' :
	app.secret_key='mysecret'
	app.run(debug=True)
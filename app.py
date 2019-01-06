from flask import Flask, render_template, flash, redirect, url_for, session, request, logging,send_from_directory
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from extensions import app,mysql


#import blueprints
from blueprints.LoginBlueprint import login_blueprint
from blueprints.SignupBlueprint import signup_blueprint
from blueprints.ProfileBlueprint import profile_blueprint
from blueprints.ItemBlueprint import item_blueprint


#register blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(item_blueprint)

path = 'uploads/pic'
filepath = 'uploads/items/pic'
# Index
@app.route('/')
def index():
    return render_template('home2.html')
@app.route('/uploads/pic/<filename>')
def uploaded_file(filename):
    return send_from_directory(path,
                               filename)

@app.route('/uploads/items/pic/<filename>')
def uploaded_item(filename):
    return send_from_directory(filepath,
                               filename)
# Home
@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("SELECT * from items", [] )
    items = cur.fetchall()
    #Close connection
    cur.close()
    return render_template('index.html',items=items)
# About
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
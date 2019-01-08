from flask import Blueprint, render_template, session, redirect, url_for, request
import os
from extensions import mysql
from werkzeug.utils import secure_filename
import uuid
from extensions import mysql

pdetail_blueprint = Blueprint('pdetail_blueprint', __name__)

path = 'uploads/pic'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def hash_filename(filename):
    filename = secure_filename(filename)
    ext = filename.rsplit('.', 1)[1].lower()
    return str(uuid.uuid4())+'.'+ext
# User login
@pdetail_blueprint.route("/product/<id>/details", methods=['GET', 'POST'])
def pdetail(id):
    
    if 'user' in session:
        user = session['user']
    else:
        return redirect(url_for('login_blueprint.login'))
    print user

    # return redirect(url_for('dashboard'))
    return render_template('product.html', user = user)
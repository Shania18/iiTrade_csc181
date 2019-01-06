from flask import Blueprint, render_template, session, redirect, url_for, request
import os
from extensions import mysql
from werkzeug.utils import secure_filename
import uuid
from extensions import mysql

profile_blueprint = Blueprint('profile_blueprint', __name__)

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
@profile_blueprint.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'user' in session:
        user = session['user']
    else:
        return redirect(url_for('login_blueprint.login'))
    print user
    if user['picture'] == '' or user['picture'] is None:
        user['picture'] = 'https://mbtskoudsalg.com/images/profile-image-png-8.png'
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if allowed_file(file.filename):
                filename = hash_filename(file.filename)
                file.save(os.path.join(path, filename))
                #TODO : add filename to database user picture
                # Create cursor
                cur = mysql.connection.cursor()
                cur.execute("UPDATE user_registration SET picture=%s WHERE email = %s", [path + '/' + filename,user['email']])
                mysql.connection.commit()
                user['picture'] = path + '/' + filename
                session['user'] = user

    return render_template('profile.html',user = user)


# Edit Profile
@profile_blueprint.route('/edit_profile/<string:id>', methods=['GET', 'POST'])
def edit_profile(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get user by id
    result = cur.execute("SELECT * FROM user_registration WHERE userid = %s", [id])

    user = cur.fetchone()
    cur.close()
    # Get form
    form = EditProfileForm(request.form)

    # Populate user form fields
    form.fname.data = user['fname']
    form.lname.data = user['lname']
    form.cnumber.data = user['cnumber']
    form.email.data = user['email']
    form.address.data = user['address']
    form.password.data = user['password']
    form.confirm.data = user['confirm']

    if request.method == 'POST' and form.validate():
        fname = request.form['fname']
        lname = request.form['lname']
        cnumber = request.form['cnumber']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        confirm = request.form['confirm']

        # Create Cursor
        cur = mysql.connection.cursor()
        #app.logger.info(title)
        # Execute
        cur.execute ("UPDATE user_registration SET firstname=%s, lastname=%s, contactno=%s, email=%s, address=%s, password=%s WHERE userid=%s",(fname, lname, cnumber, email, address, password, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Profile Updated', 'success')

        return redirect(url_for('home'))

    return render_template('editprofile.html', form=form)
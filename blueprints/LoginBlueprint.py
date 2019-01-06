from flask import Blueprint,render_template,session,redirect,url_for,request,flash
from extensions import mysql
from passlib.hash import sha256_crypt

login_blueprint = Blueprint('login_blueprint', __name__)


# User login
@login_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by email
        result = cur.execute("SELECT * FROM user_registration WHERE email = %s", [email])
        
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                cur.execute("SELECT * FROM user_registration WHERE email = %s", [email])
                user = cur.fetchone()
                print user
                session['user'] = user
                flash('You are now logged in', 'success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid login'
                return render_template('login2.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'User not found'
            return render_template('login2.html', error=error)

    return render_template('login2.html')
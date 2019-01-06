from flask import Blueprint,render_template,session,redirect,url_for,request,flash
from extensions import mysql
from forms.RegisterForm import RegisterForm
from passlib.hash import sha256_crypt

signup_blueprint = Blueprint('signup_blueprint', __name__)

# User login
@signup_blueprint.route("/signup", methods=['GET', 'POST'])
def signup():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		fname = form.fname.data
		lname = form.lname.data
		email = form.email.data
		cnumber = form.cnumber.data
		address = form.address.data
		password = sha256_crypt.encrypt(str(form.password.data))
		val = (fname, lname, cnumber, email, address, password)
		# Create cursor
		cur = mysql.connection.cursor()
		# Execute query
		cur.execute("INSERT INTO user_registration(firstname, lastname, contactno, email, address, password) VALUES(%s, %s, %s, %s, %s, %s)", val)
		# Commit to DB
		mysql.connection.commit()
		# Close connection
		cur.close()
		flash('You are now registered', 'success')
		return redirect(url_for('home'))
	return render_template('signup2.html', form=form)
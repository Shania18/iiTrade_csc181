from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'trade'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Items
@app.route('/items')
def items():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get items
    result = cur.execute("SELECT * FROM items")

    items = cur.fetchall()

    if result > 0:
        return render_template('items.html', items=items)
    else:
        msg = 'No Item Found'
        return render_template('items.html', msg=msg)
    # Close connection
    cur.close()


#Single Item
@app.route('/item/<string:id>/')
def item(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get item
    result = cur.execute("SELECT * FROM items WHERE id = %s", [id])

    item = cur.fetchone()

    return render_template('item.html', item=item)


# Register Form Class
class RegisterForm(Form):
    fname = StringField('FirstName', [validators.Length(min=1, max=50)])
    lname = StringField('Lastname', [validators.Length(min=4, max=25)])
    cnumber = StringField('Contactnumber', [validators.Length(min=6, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    address = StringField('Address', [validators.Length(min=10, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fname = form.fname.data
        lname = form.lname.data
        cnumber = form.cnumber.data
        email = form.email.data
        address = form.address.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO user_registration(firstname, lastname, contactno, email, address, password) VALUES(%s, %s, %s, %s, %s, %s)", (fname, lname, cnumber, email, address, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
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

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'User not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get items
    result = cur.execute("SELECT * FROM items")

    items = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', items=items)
    else:
        msg = 'No Item Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# Item Form Class
class ItemForm(Form):
    itemname = StringField('Itemname', [validators.Length(min=1, max=200)])
    description = TextAreaField('Description', [validators.Length(min=30)])

# Add Item
@app.route('/add_item', methods=['GET', 'POST'])
@is_logged_in
def add_item():
    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        itemname = form.itemname.data
        description = form.description.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO items(item_name, description) VALUES(%s, %s)",(itemname, description))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Item Added', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_item.html', form=form)


# Edit Item
@app.route('/edit_item/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_item(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get item by id
    result = cur.execute("SELECT * FROM items WHERE id = %s", [id])

    item = cur.fetchone()
    cur.close()
    # Get form
    form = ItemForm(request.form)

    # Populate item form fields
    form.itemname.data = item['itemname']
    form.description.data = item['description']

    if request.method == 'POST' and form.validate():
        itemname = request.form['itemname']
        description = request.form['description']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE items SET item_name=%s, description=%s WHERE id=%s",(itemname, description, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Item Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_item.html', form=form)

# Delete Item
@app.route('/delete_item/<string:id>', methods=['POST'])
@is_logged_in
def delete_item(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM items WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Item Deleted', 'success')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
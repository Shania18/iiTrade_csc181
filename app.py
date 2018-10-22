from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from extensions import app,mysql


#import blueprints
from blueprints.LoginBlueprint import login_blueprint
from blueprints.SignupBlueprint import signup_blueprint


#register blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)

# Index
@app.route('/')
def index():
    return render_template('landpage.html')

# Home
@app.route('/home')
def home():
    return render_template('index.html')
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
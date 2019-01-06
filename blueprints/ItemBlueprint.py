from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from forms.ItemForm import ItemForm
from extensions import mysql
from werkzeug.utils import secure_filename
import uuid
import os

item_blueprint = Blueprint('item_blueprint', __name__)

path = 'uploads/items/pic'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def hash_filename(filename):
    filename = secure_filename(filename)
    ext = filename.rsplit('.', 1)[1].lower()
    return str(uuid.uuid4()) + '.' + ext

# Add Item
@item_blueprint.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = ItemForm(request.form)
    if request.method == 'POST':
        itemname = request.form['itemname']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        photo = request.files['file']
        unitsno = request.form['unitsno']
        filename = hash_filename(photo.filename)
        photo.save(os.path.join(path, filename))
        filepath = path + '/' + filename
        val = (itemname, description, price, category, filepath, unitsno)
        # Create Cursor
        print 'success'
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO items(item_name, description, price, category, photo, units_no) VALUES(%s, %s, %s, %s, %s, %s)", val )
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('Item Added', 'success')
        print 'success'
        return redirect(url_for('item_blueprint.add_item'))

    return render_template('sell.html', form=form)


# Edit Item
@item_blueprint.route('/edit_item/<string:id>', methods=['GET', 'POST'])
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
@item_blueprint.route('/delete_item/<string:id>', methods=['POST'])
#@is_logged_in
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
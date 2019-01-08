from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from extensions import mysql
from datetime import datetime
cart_blueprint = Blueprint('cart_blueprint', __name__)

class ShoppingCart():
 
    def __init__(self):
        self.total = 0
        self.items = dict()

@cart_blueprint.route("/cart/add/<id>", methods=['GET'])
def add_prod_to_cart(id):
    user = session['user']
    
    # Create cursor
    cur = mysql.connection.cursor()

    # Get item by id
    result = cur.execute("SELECT * FROM items WHERE id_items = %s", [id])
    item = cur.fetchone()
    dt = datetime.now()
    cur.execute("INSERT INTO  cart_items(product_id,quantity,user_id,created,modified) VALUES(%s,%s,%s,%s,%s)",[id,1,user['userid'],dt,dt])
    mysql.connection.commit()
    cur.close()

    print(item)
    return redirect(request.referrer or '/')
@cart_blueprint.route("/cart/remove/<id>", methods=['GET'])
def remove_prod_to_cart(id):
    user = session['user']
    # Create cursor
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart_items where user_id = %s and product_id = %s",[user['userid'],id])
    mysql.connection.commit()
    cur.close()
    
    return redirect(request.referrer or '/')
@cart_blueprint.route("/cart/add", methods=['POST'])
def add_to_cart():
    cart = ShoppingCart.add(product=request.form['product'], quantity=int(request.form['quantity']))
    return iitrade(cart)
    def add_item(self,item_name,quantity,price):
        self.total = self.total + (price*quantity)  
        self.items[item_name] = quantity
 
    def remove_item(self,item_name,quantity,price):
        quantityLeft = self.items[item_name]
        if quantityLeft > quantity:
            self.items[item_name] = self.items[item_name]  - quantity            
            self.total = self.total - (price*quantity)        
        else:
            self.total = self.total - (price*quantityLeft) 
            self.items.pop(item_name)
 
    def checkout(self,cash_paid):
        if cash_paid < self.total:
            return "Cash paid not enough"
        else:
            return cash_paid - self.total
@cart_blueprint.route("/cart")
def view_cart():
    cart = ShoppingCart.get()
    return render_template("cart.html", cart=cart) 
class Shop(ShoppingCart):
 
    def __init__(self):
        ShoppingCart.__init__(self)    
        self.quantity = 100   
@cart_blueprint.route("/cart/remove/<item_id>", methods=['POST'])
def remove_from_cart(item_id):
    cart = ShoppingCart.remove(id_items)
    return iitrade(cart) 
    def remove_item(self):
        self.quantity = self.quantity - 1
 
if __name__ == "__main__":
    cart = ShoppingCart()
    print("All items: ",cart.items)
    print("current Total:",cart.total)

    cart = ShoppingCart.get()

@cart_blueprint.route("/checkout", methods=['GET','POST'])
def payment():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']

    with mysql.connect('dbTrade') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, cart WHERE products.productId = cart.productId AND cart.userId = " + str(userId))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
        print(row)
        cur.execute("INSERT INTO Orders (userId, productId) VALUES (?, ?)", (userId, row[0]))
    cur.execute("DELETE FROM kart WHERE userId = " + str(userId))
    conn.commit()
    return render_template("checkout.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

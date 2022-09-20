from app import app
from flask import render_template, request, redirect, url_for, flash
from . forms import UserCreationForm, LoginForm, Product, AddToCart
from . models import User, db, Product, UserCart
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

@app.route('/')
@app.route('/index')
def index():
    title = "Home"
    return render_template("index.html", title=title)

@app.route('/chairs')
def chairs():
    title = "Chairs"
    chairs = Product.query.filter_by(category='chair').all()
    chair_caption = Product.caption
    chair_price = Product.price
    chair_url = Product.img_url
    return render_template("chairs.html", title=title, chairs=chairs, chair_price=chair_price, chair_caption=chair_caption, chair_url=chair_url)

@app.route('/couches')
def couches():
    title = "Couches"
    couches = Product.query.filter_by(category='couch').all()
    couch_caption = Product.caption
    couch_price = Product.price
    couch_url = Product.img_url
    return render_template("couches.html", title=title, couches=couches, couch_price=couch_price, couch_caption=couch_caption, couch_url=couch_url)

@app.route('/sidetables')
def sidetables():
    title = "Side Tables"
    sidetables = Product.query.filter_by(category='sidetable').all()
    sidetable_caption = Product.caption
    sidetable_price = Product.price
    sidetable_url = Product.img_url
    return render_template("sidetables.html", title=title, sidetables=sidetables, sidetable_price=sidetable_price, sidetable_caption=sidetable_caption, sidetable_url=sidetable_url)


@app.route('/cart')
def allItems():
    title = "Cart"
    items = UserCart.query.all()
    results = db.session.query(UserCart).join(Product).join(User).all()
    combined_tables = '<ul>'
    for item in items:
        combined_tables += '<li>' + UserCart.name + ', ' + UserCart.user_id + '</li>'
    combined_tables += '</ul>'
    print(combined_tables)
    return render_template("cart.html", title=title, items=items)

@app.route('/cart/<int:cart_id>')
def singleItem(cart_id):
    item = UserCart.query.get(cart_id)
    return render_template('singleItem.html', item=item)

# @app.route('/cart/update/<int:cart_id>', methods=['GET', 'POST'])
# def updateItems(cart_id):
#     title = "Cart"
#     form = AddToCart()
#     results = db.session.query(UserCart).join(Product).join(User).all()
#     combined_tables = '<ul>'
#     for result in results:
#         combined_tables += '<li>' + db.name + ', ' + db.caption + '</li>'
#     combined_tables += '</ul>'
#     print(combined_tables)
#     return combined_tables
#     # if request.method == 'POST':
#     #     if form.validate():
#     #         UserCart.id = id
#     #         UserCart.user_id = User.id
#     #         UserCart.product_id = Product.id
#     #         db.session.commit()
#     #         return render_template('cart.html', results=results, title=title)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = "Signup"
    form = UserCreationForm()
    if request.method == 'POST':
        print('Post Request Has Been Made')
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(first_name, last_name, username, email, password)

            user = User(first_name, last_name, username, email, password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))
        else:
            print("Failed to validate")
    return render_template("signup.html", title=title, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            print(user.id, user.username, user.password)
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Welcome Back!', category='success')
                    return redirect(url_for('index'))
                else:
                    print("wrong password entered.  Please try again")   
            else:
                print('We have no record of that user in our database, please sign-up then login to your account.')
    return render_template('login.html', form=form, title=title)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
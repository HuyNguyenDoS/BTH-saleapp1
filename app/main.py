import math
from app import app
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user
import utils
from app.admin import *
from app import login
import cloudinary.uploader


@app.route("/")
def home():
    cate_id = request.args.get('category_id')
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1)

    products = utils.load_products(cate_id=cate_id, keyword=keyword, page=int(page))

    return render_template("index.html", products=products, pages=math.ceil(utils.count_products()/app.config['PAGE_SIZE']))

@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)

@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_user_login(username=username, password=password)

    if user:
        login_user(user=user)
        return redirect('/admin')


@app.route("/")
def admin():
    categories = utils.load_categories()
    return render_template('admin/index.html',
                           categories=categories)

@app.route('/register', methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            password = request.form['password']
            confirm = request.form['confirm']

            if password.__eq__(confirm):
                data = request.form.copy()
                del data['confirm']

                file = request.files['avatar']
                if file:
                    res = cloudinary.uploader.upload(file)
                    data['avatar'] = res['secure_url']

                if utils.register_user(**data):
                    redirect(url_for('signin'))
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
            else:
                error_msg = "Mat khau KHONG khop!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('register.html', error_msg=error_msg)

@app.route('/login', methods=['get', 'post'])
def signin():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user_login(username=username, password=password)
            if user:
                login_user(user=user)

                return redirect("/")
            else:
                error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)

@app.route('/logout')
def signout():
    logout_user()

    return redirect(url_for('signin'))

@app.context_processor
def common_reponse():
    return {
        'categories': utils.load_categories()
    }

@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if cart:
        cart ={}

if __name__ == '__main__':

    app.run(debug=True)
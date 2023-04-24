from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api
from werkzeug.utils import secure_filename
from data import db_session
from data.users import User
from data.items import Items
from data.categories import Categories
from forms.user import RegisterForm, LoginForm
from forms.items import ItemsForm

import datetime
import os
import items_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


def main():
    db_session.global_init("db/database.db")
    api.add_resource(items_api.ItemResource, '/api/items/<int:item_id>')
    api.add_resource(items_api.ItemsListResource, '/api/items')
    api.add_resource(items_api.ItemsCategoryResource, '/api/items/category/<int:category_id>')

    # db_sess = db_session.create_session()
    # category = db_sess.query(Categories).filter(Categories.id == 1).first()
    # item = Items()
    # item.title = "Zoom75 KIT Tri-Mode Essential Edition"
    # item.description = "Zoom75 KIT Tri-Mode EE — база для сборки, которая позволяет создать беспроводную хотсвап клавиатуру своей мечты почти с нуля: здесь нет кейкапов и переключателей для того, чтобы вы могли выбрать идеальную комбинацию, а широкие возможности кастомизации помогут создать уникальное устройство.\n" \
    #                    "Серия Essential Edition позволяет выбрать из 15 вариантов корпусов, девяти цветов ручек энкодера и утяжелителей, двух вариантов платы: с флекс катами и без.\n" \
    #                    "Также есть беспроводная база в корпусах серии Special Edition или в лимитированном дизайне Kitsune, а еще проводная версия в черном или белом корпусе. Дополнительно можно докупить заднюю панель корпуса другого цвета."
    # item.category_id = 1
    # item.category = category
    # item.image = "/static/img/zoom75-kit-3-min.jpg"
    # item.price = 17580
    # item.availability = 50

    # db_sess.add(item)
    # user = db_sess.query(Items).filter(Items.id == 4).first()
    # user.image = "/static/img/zoom75-kit-3-min.jpg"
    # db_sess.commit()
    # for category in db_sess.query(Categories).all():
    #     category.category = category.category.lower()
    #     db_sess.commit()
    #     print(category.id, category.category)
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).all()[:15]
    return render_template("index.html", title="Главная | Geekboards", items=items)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/items',  methods=['GET', 'POST'])
def add_item():
    form = ItemsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        item = Items()
        item.title = form.title.data
        item.description = form.description.data
        item.category_id = form.category_id.data
        category = db_sess.query(Categories).filter(Categories.id == form.category_id.data).first()
        item.category = category
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'static/img', filename
        ))
        item.image = f"/static/img/{filename}"
        item.price = form.price.data
        item.availability = form.availability.data
        db_sess.add(item)
        db_sess.commit()
        return redirect('/')
    return render_template('items.html', title='Добавление товара',
                           form=form)


@app.route("/category/<category>")
def categories(category):
    db_sess = db_session.create_session()
    collection = db_sess.query(Categories).filter(Categories.category == category).first()
    items = db_sess.query(Items).filter(Items.category_id == collection.id)
    return render_template("category.html", title=category, category=category, items=items)


@app.route("/product/<product>")
def product(product):
    product_title = " ".join(product.split("-"))
    db_sess = db_session.create_session()
    for i in db_sess.query(Items).all():
        if i.title.lower() == product_title:
            item = i
    item_title = item.title
    return render_template("product.html", title=item_title, item=item)


@app.route("/cart")
def cart():
    return render_template("cart.html", title="Корзина")


if __name__ == '__main__':
    main()

from flask import Flask, render_template, redirect
from flask_restful import Api
from data import db_session
from data.users import User
from data.items import Items
from data.categories import Categories
from forms.user import RegisterForm

import items_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


def main():
    db_session.global_init("db/database.db")
    api.add_resource(items_api.ItemResource, '/api/items/<int:item_id>')
    api.add_resource(items_api.ItemsListResource, '/api/items')
    api.add_resource(items_api.ItemsCategoryResource, '/api/items/category/<int:category_id>')
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).all()
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


if __name__ == '__main__':
    main()

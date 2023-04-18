from flask import Flask, render_template
from flask_restful import Api
from data import db_session
from data.users import User
from data.items import Items
from data.categories import Categories
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


if __name__ == '__main__':
    main()

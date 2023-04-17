from flask import Flask
from flask_restful import Api

import items_api
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


def main():
    db_session.global_init("db/database.db")
    api.add_resource(items_api.ItemResource, '/api/items/<int:item_id>')
    api.add_resource(items_api.ItemsListResource, '/api/items')
    api.add_resource(items_api.ItemsCategoryResource, '/api/items/category/<int:category_id>')
    app.run()


if __name__ == '__main__':
    main()

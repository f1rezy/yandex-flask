from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.items import Items

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('category_id', required=True, type=int)
parser.add_argument('image', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('availability', required=True, type=int)


def abort_if_items_not_found(items_id):
    session = db_session.create_session()
    items = session.query(Items).get(items_id)
    if not items:
        abort(404, message=f"Items {items_id} not found")


class ItemResource(Resource):
    def get(self, item_id):
        abort_if_items_not_found(item_id)
        session = db_session.create_session()
        item = session.query(Items).get(item_id)
        return jsonify({'items': item.to_dict(
            only=('title', 'description', 'category_id', 'image', 'price', 'availability'))})

    def delete(self, item_id):
        abort_if_items_not_found(item_id)
        session = db_session.create_session()
        item = session.query(Items).get(item_id)
        session.delete(item)
        session.commit()
        return jsonify({'success': 'OK'})


class ItemsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        items = session.query(Items).all()
        return jsonify({'items': [item.to_dict(
            only=('title', 'description', 'category_id', 'image', 'price', 'availability')) for item in items]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        items = Items(
            title=args['title'],
            description=args['description'],
            category_id=args['category_id'],
            image=args['image'],
            price=args['price'],
            availability=args['availability']
        )
        session.add(items)
        session.commit()
        return jsonify({'success': 'OK'})


class ItemsCategoryResource(Resource):
    def get(self, category_id):
        session = db_session.create_session()
        items = session.query(Items).filter(Items.category_id == category_id)
        return jsonify({'items': [item.to_dict(
            only=('title', 'description', 'category_id', 'image', 'price', 'availability')) for item in items]})

from flask import Flask, render_template
from data import db_session
from data.users import User
from data.items import Items
from data.categories import Categories

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/database.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).all()
    return render_template("index.html", title="Главная | Geekboards", items=items)


if __name__ == '__main__':
    main()

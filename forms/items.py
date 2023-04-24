from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ItemsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField("Описание")
    category_id = IntegerField("id категории")
    image = FileField("Изображение", validators=[FileRequired()])
    price = IntegerField('Цена')
    availability = IntegerField("Количество")
    submit = SubmitField('Применить')

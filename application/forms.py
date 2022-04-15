from wtforms import TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from application import utils

languages_choice = []

for key,value in utils.languages.items():
    languages_choice.append((key, value))

class MyForm(FlaskForm):
    text_field = TextAreaField("Data", validators=[DataRequired()])
    language_field = SelectField("Language to Tanslate To", choices=languages_choice)
    submit = SubmitField("Translate")
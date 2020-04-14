from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired , Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ProfileForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], id="fname")
    lastname = StringField('Lastname', validators=[DataRequired()], id="lname")
    gender = SelectField('Gender',  choices=[('S','Select Gender'), ('Female', 'Female'), ('Male', 'Male')], id="gender")
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "e.g. jdoe@example.com"}, id="email")
    location = StringField ('Location', validators=[DataRequired()], render_kw={"placeholder": "e.g. Kingston,Jamaica "}, id="location")
    biograpy = TextAreaField ('Biography', validators=[DataRequired()], id="bio")
    picture = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'PNG'], 'Images only!')],id="profilepicture")

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pension.models import User


class RegistrationForm(FlaskForm):
    username = StringField("User Name",validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField("Email",validators=[DataRequired(), Email(), Length(min=2, max=25)])
    contact = IntegerField("Contact",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(), Length(min=5, max=25)])
    confirmpassword = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:    
            raise ValidationError("UserName Already exists in database. Please try another One")
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:    
            raise ValidationError("UserName Already exists in database. Please try another One")
    def validate_contact(self,contact):
        contact = contact.data
        if len(str(contact)) < 10:
            raise ValidationError("Contact Number must be equal to 11 digits. Please try again.")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired() ])
    submit = SubmitField('Sign In')
    def validate_user(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:    
            raise ValidationError("The email you provided is incorrect. Please try again")
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length 

class SignupForm(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
	last_name = StringField('Last name', validators=[DataRequired("Please enter your last name")])
	email = StringField('Email', validators=[DataRequired("Please enter your email"), Email("Please enter a valid email address")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password"), Length(min=6, message="Password must be 6 char or more")])
	submit = SubmitField('Sign up', validators=[DataRequired()])

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired("Please enter your email"), Email("Please enter a valid email address")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
	submit = SubmitField("Sign in")

class AddressForm(FlaskForm):
	address = StringField('Address', validators=[DataRequired("Please enter an address")])
	submit = SubmitField("Search")

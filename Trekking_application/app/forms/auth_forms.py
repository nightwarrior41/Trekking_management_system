from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,RadioField,SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField("Firt Name",validators=[DataRequired(),Length(min=2,max=50)])
    last_name = StringField("Last Name",validators=[DataRequired(),Length(min=2,max=100)])
    email = EmailField('Email',validators=[DataRequired(),Email(),Length(max=120)])
    phone = StringField('Phone Number',validators=[DataRequired(),Length(min=10,max=10)]) 
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8,max=256)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password",message="Password do not match")])
    role = RadioField("Register As",choices=[('user',"Trekker"),('staff',"Staff")],validators=[DataRequired()])
    submit = SubmitField("Register Now")
    
    def validate_phone(self,phone):
        exists_num = User.query.filter_by(phone=phone.data).first()
        if exists_num:
            raise ValidationError("User Already Exists ! try using any other phone number")
        if not phone.data.isdigit():
            raise ValidationError("Phone number must contain only digits.")
    
    def validate_email(self,email):
        exists_email = User.query.filter_by(email=email.data).first()
        if exists_email:
           raise ValidationError("User Already Exists ! try using any other Email ID")
            
    

class LoginForm(FlaskForm):
    email = EmailField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    login = SubmitField("Login Now")



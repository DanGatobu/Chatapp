from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import ValidationError, input_required, length
from modules import *

class registerform(FlaskForm):
    Username=StringField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"Firstname"})
    password=PasswordField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Register")
    
    def validate_username(self,username):
        existing_user_username=User.query.filter_by(username=username.data).first()
        
        if existing_user_username:
            raise ValidationError("That user name already exists")
        
    
class Loginform(FlaskForm):
    Username=StringField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Login")
    

        







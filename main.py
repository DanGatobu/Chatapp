from flask import Flask,redirect,render_template,request,url_for,g
from flask_socketio import SocketIO,emit,send,join_room,leave_room
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER, Column, DateTime, String
from flask_login import (UserMixin, current_user,login_required, login_user, logout_user)
from wtforms.validators import ValidationError, input_required, length
from wtforms import PasswordField, StringField, SubmitField
from flask_wtf import FlaskForm
from flask_login.login_manager import LoginManager
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import date
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:dannewton\
@localhost/websocket'

db=SQLAlchemy(app)
session=sessionmaker()
app.config['SQLALCHEMY_ECHO'] = True
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
class User(db.Model,UserMixin):
    __tablename__='User'
    id=Column(INTEGER(),primary_key=True)
    username=Column(String(30),nullable=False,unique=True)
    password=Column(String(300),nullable=False,unique=True)
    date=Column(DateTime)
class messages(db.Model):
    __tablename__="messages"
    id=Column(INTEGER(),primary_key=True)
    userid=Column(INTEGER(),primary_key=True)
    messages=Column(String(1000000),nullable=False,unique=True)
    
   
class registerform(FlaskForm):
    username=StringField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Register")
    
    def validate_username(self,username):
        existing_user_username=User.query.filter_by(username=username.data).first()
        
        if existing_user_username:
            raise ValidationError("That user name already exists")
        
class Loginform(FlaskForm):
    username=StringField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[input_required(),length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Login")


    
app.config['SECRET_KEY']=['socket']
socketio=SocketIO(app)

rooms=['Football','coding','Music','Travelling']

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/login',methods=['GET','POST'])
def login():
    form=Loginform()
    
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        
        if user:
            if (user.password,form.password.data):
                login_user(user)
                return redirect(url_for('chat'))
    
    return render_template('login.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    form=registerform()
    if form.validate_on_submit():
        password=form.password.data
        username=form.username.data
        datetoday=date.today()
        new_user=User(username=username,password=password,date=datetoday)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html',form=form)

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id)) 

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html',username=current_user.username,rooms=rooms)


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]

    send({"username": username, "msg": msg}, room=room)


@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)

    

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app,debug=True)
    
#add a logout button on nav bar that displays only when a person is logged
#add messages 
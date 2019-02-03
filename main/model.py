from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

db = SQLAlchemy()


# ================= Models ==================== #
class User(UserMixin, db.Model):
    id = db.Column(db.String(9), primary_key=True)      # matric number
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    credit_amount = db.Column(db.Numeric(precision=2), default=0.00)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class FoodOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stall_name = db.Column(db.String(50))
    food_name = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    price = db.Column(db.Numeric(scale=2))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    is_collected = db.Column(db.Boolean)
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50))
    event_description = db.Column(db.String(140))
    event_date = db.Column(db.String(15))
    event_time = db.Column(db.String(15))
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ================= Web Forms ==================== #
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
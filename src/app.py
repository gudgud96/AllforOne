# ====== DB endpoints for AllInOne app ====== #
# Here provides DB endpoints for 3 tables -   #
# User, FoodOrder and Event schema to be used #
# by backend functions.                       #
#                                             #
# Author: Tan Hao Hao                         #
# =========================================== #

import datetime
import json
import os
from decimal import Decimal

from flask import Flask, render_template, redirect, url_for, request, Response, session
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

# database location
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)


# ================= Models ==================== #
class User(UserMixin, db.Model):
    id = db.Column(db.String(9), primary_key=True)  # matric number
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


class UserTracker(db.Model):
    '''User could choose either purchase (food , expenses) or activity (going to work...etc)
    and description = his/her remarks, 
    '''
    id = db.Column(db.Integer , primary_key=True)
    timestamp = db.Column(db.DateTime , index=True,default=datetime.datetime.now())
    location = db.Column(db.String(15))
    purchase = db.Column(db.Numeric(scale=2))
    activity = db.Column(db.String(15))
    description = db.Column(db.String(140))
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'))
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Fault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fault_location = db.Column(db.String(50))
    fault_description = db.Column(db.String(140))
    fault_type = db.Column(db.String(50))
    fault_status = db.Column(db.String(50))
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'))
    fault_completed = db.Column(db.Text)
    fault_taken_time = db.Column(db.Text)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Clinic(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    timestamp = db.Column(db.DateTime , index=True,default=datetime.datetime.now())
    clinic = db.Column(db.String(50), default='NTU Fullerton')
    booking_date = db.Column(db.String(15))
    booking_time = db.Column(db.String(15))
    description = db.Column(db.String(140))
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


# Dummy index page for testing only. To be inserted with new ones
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = request.form
    return render_template('index.html')


# ================= User Login DB Endpoints ==================== #
@app.route('/get_users', methods=['POST'])
def get_users():
    users = User.query.filter_by("test")

    filter_users = {}
    for user in users:
        filter_users['username'] = user['username']
        filter_users['status'] = user['status']

    return filter_users


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global name
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user:
            if check_password_hash(user.password, data['password']):
                login_user(user, remember=data['remember'])
                session["user_id"] = user.id
                print('session', session)
                # get name
                name = data['username']
                return redirect(url_for('index'))

        return render_template('form_result.html', route = '/login', result = 'Failed!', msg = 'Invalid username or password!')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global name

    if request.method == 'POST':
        data = request.form

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        name = data['username']

        new_user = User(id=data['matric'], username=data['username'],
                        email=data['number'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('form_result.html', route = '/signup', result = 'Successful!', msg = 'New user has been created!')

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    result = User.query.get(session["user_id"]).as_dict()
    output_dict = dict()
    output_dict['user_id'] = result['id']
    output_dict['name'] = result['username']
    output_dict['credit_amount'] = "{:.2f}".format(result['credit_amount'])
    output_dict['email'] = result['email']
    # return render_template('profile.html', user_id=result['id'],
    #                        name=result['username'],
    #                        credit_amount="{:.2f}".format(result['credit_amount']),
    #                        email=result['email'])
    return json.dumps(output_dict)


# ================= Wallet DB Endpoints ==================== #
@app.route('/topup', methods=['GET', 'POST'])
def topup():
    if request.method == 'POST':
        data = request.form
        is_topup = topup_user(session["user_id"], int(data["amount"]))
        if is_topup:
            user = User.query.filter_by(id=session["user_id"]).first()
            balance = "{:.2f}".format(user.credit_amount)
            
            return render_template('form_result.html', route = '/topup', result = 'Top up successful!', msg = 'Balance: SGD ' + str(balance))
        else:
            return render_template('form_result.html', route = '/topup', result = 'Top up failed!', msg = '')
    return render_template('topup.html')


def topup_user(user_id, amount):
    user = User.query.filter_by(id=user_id).first()
    print(user.credit_amount)
    user.credit_amount += Decimal(amount)
    print(user.credit_amount)
    db.session.commit()
    return True


def consume(user_id, amount):
    user = User.query.filter_by(id=user_id).first()
    if user.credit_amount < amount:
        print("Insufficient amount.")
        return False
    user.credit_amount -= Decimal(amount)
    db.session.commit()
    return True


# ================= Food Order DB Endpoints ==================== #
@app.route('/order_food', methods=['GET', 'POST'])
def order_food():
    if request.method == 'POST':
        data = request.get_json()
        total_price = Decimal(data["price"])
        is_added = add_new_order(data["stall_name"], data["food_name"], data["amount"],
                                 total_price, session["user_id"])
        if is_added:
            is_consume = consume(session["user_id"], total_price)
            if is_consume:
                user = User.query.filter_by(id=session["user_id"]).first()
                balance = "{:.2f}".format(user.credit_amount)
                # return render_template('order_finish.html', balance=balance)
                return json.dumps({"balance": balance})
            else:
                user = User.query.filter_by(id=session["user_id"]).first()
                balance = "{:.2f}".format(user.credit_amount)
                return json.dumps({"balance": balance})
                # return render_template('order_unsuccessful.html', balance=balance)

        return render_template('form_result.html', route = '/order_food', result = 'Failed!', msg = 'Your order is not sent! Contact administrator')

    return render_template('food_order.html')


@app.route('/food_history', methods=['GET'])
def food_history():
    food_order_results = FoodOrder.query.filter_by(user_id=session["user_id"]).all()
    result = {}
    result['North Spine Canteen'] = 0
    result['South Spine Canteen'] = 0
    result['The Quad'] = 0
    result["McDonald's"] = 0
    result['Canteen 2'] = 0
    for order in food_order_results:
        result[order.stall_name] += 1
    # return render_template('food_history.html',
    #                        items=FoodOrder.query.filter_by(user_id=session["user_id"]),
    #                        ns=result['North Spine Canteen'],
    #                        ss=result['South Spine Canteen'],
    #                        quad=result['The Quad'],
    #                        mcd=result["McDonald's"],
    #                        can2=result['Canteen 2'])
    output_dict = dict()
    output_dict["user_id"] = session["user_id"]
    output_dict["ns"] = result['North Spine Canteen']
    output_dict["ss"] = result['South Spine Canteen']
    output_dict["quad"] = result['The Quad']
    output_dict["mcd"] = result["McDonald's"]
    output_dict["can2"] = result['Canteen 2']
    return json.dumps(output_dict)


def add_new_order(stall_name, food_name, amount, price, user_id):
    new_id = len(FoodOrder.query.all())
    new_order = FoodOrder(id=new_id, stall_name=stall_name, food_name=food_name,
                          amount=amount, price=price, is_collected=False,
                          user_id=user_id)
    db.session.add(new_order)
    db.session.commit()
    return True


def update_food_collected(order_id, collect_status):
    collected_order = FoodOrder.query.filter_by(id=order_id).first()
    collected_order.is_collected = collect_status
    db.session.commit()


# =================== Event DB Endpoints ======================= #
@app.route('/register_event', methods=['GET', 'POST'])
def register_event():
    if request.method == 'POST':
        data = request.form
        new_id = len(Event.query.all()) + 1
        new_event = Event(id=new_id, event_name=data['event_name'],
                          event_description=data['event_description'],
                          event_date=data['event_date'], event_time=data['event_time'],
                          user_id=session['user_id'])
        db.session.add(new_event)
        db.session.commit()

        return render_template('event_registered.html')

    return render_template('register_event.html')


def retrieve_all_events():
    events = Event.query.all()
    result = dict()
    result["events"] = []
    for event in events:
        result["events"].append(event.as_dict())
    return result


# =================== UserTracker DB Endpoints ======================= #
@app.route('/lifestyletrack', methods=['GET', 'POST'])
def update_activity():
    if request.method == 'POST':
        data = request.form
        new_id = len(UserTracker.query.all())
        date_time_obj = datetime.datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M')
        activity_update = UserTracker(id=new_id ,timestamp = date_time_obj,
                                      location = data['location'], activity = data['activity'],
                                      description = data['description'],
                                      purchase = data.get("purchase", -1),
                                      user_id=session['user_id'])
        db.session.add(activity_update)
        db.session.commit()

        return render_template('form_result.html', route = '/lifestyletrack', result = 'Successful!', msg = 'Thanks and keep updating me your day!')
    return render_template('lifestyletrack.html')


@app.route('/lifestyleshow')
def lifestyleshow():
    return render_template('lifestyleShow.html')


@app.route('/heatmap')
def heatmap_return():
    return render_template('testmap.html')


# =================== Fault Reporting Endpoints ======================= #
@app.route('/fault/submit', methods=['GET', 'POST'])
def fault_submit():
    if request.method == 'POST':
        data = request.form
        new_id = len(Fault.query.all()) + 1
        new_fault = Fault(id=new_id, fault_location=data['fault_location'], fault_description=data['fault_description'],
                          fault_type=data['fault_type'], fault_status='Submitted to ODFM',
                          user_id=session['user_id'], fault_completed='No', fault_taken_time='0 hours')
        db.session.add(new_fault)
        db.session.commit()

        return render_template('form_result.html', route='/fault/submit', result='Successful!',
         msg = 'Your Fault reporting request has been created! For faster response, please call 67904777')

    return render_template('fault.html')


@app.route('/fault/report')
def fault_report():
    print('query start')
    items=Fault.query.all()
    print([item.as_dict() for item in items])
    return json.dumps([item.as_dict() for item in items])
    # return render_template('fault_report.html', items=Fault.query.all())


# =================== Clinic Service DB Endpoints ======================= #
@app.route('/clinic_service', methods=['GET', 'POST'])
def clinic_booking():
    if request.method == 'POST':
        data = request.form
        new_id = len(Clinic.query.all())
        new_booking = Clinic(id=new_id, clinic=data['clinic'], booking_date=data['booking_date'],
                             booking_time=data['booking_time'], description=data['description'],
                             user_id=session['user_id'])
        db.session.add(new_booking)
        db.session.commit()

        return render_template('form_result.html', route = '/clinic_service', result = 'Successful!', msg = 'Your request has been sent to ' + data['clinic'])

    return render_template('clinic_service.html')


@app.route('/clinic_report')
def clinic_report():
    # return render_template('clinic_report.html', items=Clinic.query.all())
    return render_template('clinic_report.html')


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    users = User.query.all()
    orders = FoodOrder.query.all()
    clinics = Clinic.query.all()
    # Just for developer viewing purpose for what is in the DB
    print([user.as_dict() for user in users])
    print([order.as_dict() for order in orders])
    print([clinic.as_dict() for clinic in clinics])
    print(retrieve_all_events())
    app.run(debug=True)

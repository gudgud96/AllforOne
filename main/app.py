# ================= Main App Logic ================ #
# Main app logic to call other feature logics       #
# as blueprints.                                    #
#                                                   #
# Author: Hao Hao                                   #
# ================================================= #
import os
from decimal import Decimal
from flask import Flask, render_template, redirect, url_for, request, Response, session
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


# initialize main app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'


# database location
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


# initialize db from model.py
from main.model import db, User, Event, FoodOrder
app.app_context().push()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)


# initialize db from model.py
from main.food.food_preorder import food_api
app.register_blueprint(food_api, url_prefix='/food')


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

            return '<h1>Invalid username or password</h1>'
            #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

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

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def topup(user_id, amount):
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


# =================== Event DB Endpoints ======================= #
@app.route('/register_event', methods=['GET', 'POST'])
def register_event():
    if request.method == 'POST':
        data = request.form
        new_id = len(Event.query.all()) + 1
        new_event = Event(id=new_id, event_name=data['event_name'], event_description=data['event_description'],
                          event_date=data['event_date'], event_time=data['event_time'],
                          user_id=session['user_id'])
        db.session.add(new_event)
        db.session.commit()

        return '<h1>New event has been created!</h1>'

    return render_template('register_event.html')


def retrieve_all_events():
    events = Event.query.all()
    result = dict()
    result["events"] = []
    for event in events:
        result["events"].append(event.as_dict())
    return result


if __name__ == '__main__':
    users = User.query.all()
    orders = FoodOrder.query.all()
    # Just for developer viewing purpose for what is in the DB
    print([user.as_dict() for user in users])
    print([order.as_dict() for order in orders])
    print(retrieve_all_events())
    app.run(debug=True)

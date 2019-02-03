from flask import session, request, render_template, Blueprint
from main.model import User, FoodOrder, db

food_api = Blueprint('food', __name__, template_folder='templates')





if __name__ == '__main__':
    users = User.query.all()
    orders = FoodOrder.query.all()
    # Just for developer viewing purpose for what is in the DB
    print([user.as_dict() for user in users])
    print([order.as_dict() for order in orders])

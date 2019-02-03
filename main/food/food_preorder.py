from flask import session, request, render_template, Blueprint
from main.model import User, FoodOrder, db

food_api = Blueprint('food', __name__, template_folder='templates')


@food_api.route('/order_food', methods=['GET', 'POST'])
def order_food():
    session["user_id"] = "U1520014G"  # hard code session user id for now, remove after integrate
    if request.method == 'POST':
        data = request.form
        is_added = add_new_order(data["stall_name"], data["food_name"], data["amount"],
                                 data["price"], session["user_id"])
        if is_added:
            user = User.query.filter_by(id=session["user_id"]).first()
            balance = "{:.2f}".format(user.credit_amount)
            return render_template('order_finish.html', balance=balance)

        return '<h1>Your order is not sent!</h1>'

    return render_template('food_order.html')


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


if __name__ == '__main__':
    users = User.query.all()
    orders = FoodOrder.query.all()
    # Just for developer viewing purpose for what is in the DB
    print([user.as_dict() for user in users])
    print([order.as_dict() for order in orders])

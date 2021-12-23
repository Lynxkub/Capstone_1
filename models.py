from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def connect_db(app):
    """Connects to the database"""

    db.app=app
    db.init_app(app)



class User(db.Model):
    """Main User information table"""
    """Ideal food cost will be put in as an integer, but when it is run against the inventory, it will be converted to the proper %"""

    __tablename__='users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    restaurant_name = db.Column(db.String, nullable = False)
    location = db.Column(db.String)
    ideal_food_cost = db.Column(db.Float, nullable = False)


    @classmethod
    def signup(cls, username, password, restaurant_name, location, ideal_food_cost):
        """Hashes Password and adds user to DB"""
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username =username, restaurant_name=restaurant_name, location=location, ideal_food_cost=ideal_food_cost, password = hashed_pw)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate user to see if they exist in DB"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

    


class Product(db.Model):
    """Table that has all product information pulled from API"""

    __tablename__='products'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    pack_size = db.Column(db.Integer)



# ############################ Menu Tables ############################

class Menu(db.Model):
    """Table of User Menus"""

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False, )
    menu_name = db.Column(db.String, nullable = False)
    menu_description = db.Column(db.String)

    menu_items = db.relationship('MenuItem')


class MenuItem(db.Model):
    """Table for menu items"""
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable = False)
    menu_item_name = db.Column(db.String, nullable = False)
    menu_description = db.Column(db.String)
    menu_price = db.Column(db.Float, nullable = False)
    plate_price = db.Column(db.Float, default = 0.00, nullable = False)


class MenuItemIngredients(db.Model):
    """Table for connecting individual products with menu items"""

    __tablename__ = 'menu_item_ingredients'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), primary_key = True)


#  ############################## Inventory Tables ############################




#  ############################### Sales Tables ###############################


class SalesForecasting(db.Model):
    """Table for user to forecast sales for upcoming week"""

    __tablename__ = 'sales_forecasts'

    store_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    monday = db.Column(db.Integer, nullable = False)
    tuesday = db.Column(db.Integer, nullable = False)
    wednesday = db.Column(db.Integer, nullable = False)
    thursday = db.Column(db.Integer, nullable = False)
    friday = db.Column(db.Integer, nullable = False)
    saturday = db.Column(db.Integer, nullable = False)
    sunday = db.Column(db.Integer, nullable = False)
    weekly_total = db.Column(db.Integer, nullable = False)

    forecast = db.relationship('User')


class SalesActual(db.Model):
    """Table for user to enter actual sales for the days of the week as they happen"""

    __tablename__ = 'sales_actuals'

    store_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    monday = db.Column(db.Integer, default = 0, nullable = False)
    tuesday = db.Column(db.Integer, default = 0, nullable = False)
    wednesday = db.Column(db.Integer, default = 0, nullable = False)
    thursday = db.Column(db.Integer, default = 0, nullable = False)
    friday = db.Column(db.Integer, default = 0, nullable = False)
    saturday = db.Column(db.Integer, default = 0, nullable = False)
    sunday = db.Column(db.Integer, default = 0, nullable = False)
    weekly_total = db.Column(db.Integer, nullable = False)

    actual_sales = db.relationship('User')

class SalesAvFDollars(db.Model):
    """Table for user to compare forecasted sales vs actual sales for the week in dollars"""

    __tablename__ = 'sales_avf_dollars'

    store_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    monday = db.Column(db.Integer, default = 0, nullable = False)
    tuesday = db.Column(db.Integer, default = 0, nullable = False)
    wednesday = db.Column(db.Integer, default = 0, nullable = False)
    thursday = db.Column(db.Integer, default = 0, nullable = False)
    friday = db.Column(db.Integer, default = 0, nullable = False)
    saturday = db.Column(db.Integer, default = 0, nullable = False)
    sunday = db.Column(db.Integer, default = 0, nullable = False)
    weekly_total = db.Column(db.Integer, nullable = False)

    avf_dollars = db.relationship('User')

class SalesAvFPercent(db.Model):
    """Table for user to compare forecased sales vs actual sales for the week in a percent"""

    __tablename__ = 'sales_avf_percent'

    store_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    monday = db.Column(db.Float, default = 0, nullable = False)
    tuesday = db.Column(db.Float, default = 0, nullable = False)
    wednesday = db.Column(db.Float, default = 0, nullable = False)
    thursday = db.Column(db.Float, default = 0, nullable = False)
    friday = db.Column(db.Float, default = 0, nullable = False)
    saturday = db.Column(db.Float, default = 0, nullable = False)
    sunday = db.Column(db.Float, default = 0, nullable = False)
    weekly_total = db.Column(db.Float, nullable = False)

    avf_percent = db.relationship('User')

class HistoricalSalesInfo(db.Model):
    """Table used to store all old sales information"""

    __tablename__ = 'historic_sales'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    store_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_logged = db.Column(db.Date)
    monday_forecasted = db.Column(db.Integer, nullable = False)
    tuesday_forecasted = db.Column(db.Integer, nullable = False)
    wednesday_forecasted = db.Column(db.Integer, nullable = False)
    thursday_forecasted = db.Column(db.Integer, nullable = False)
    friday_forecasted = db.Column(db.Integer, nullable = False)
    saturday_forecasted = db.Column(db.Integer, nullable = False)
    sunday_forecasted = db.Column(db.Integer, nullable = False)
    monday_actual = db.Column(db.Integer, nullable = False)
    tuesday_actual = db.Column(db.Integer, nullable = False)
    wednesday_actual = db.Column(db.Integer, nullable = False)
    thursday_actual = db.Column(db.Integer, nullable = False)
    friday_actual = db.Column(db.Integer, nullable = False)
    saturday_actual = db.Column(db.Integer, nullable = False)
    sunday_actual = db.Column(db.Integer, nullable = False)
    forecasted_total = db.Column(db.Integer, nullable = False)
    actual_total = db.Column(db.Integer, nullable = False)
    week = db.Column(db.Integer)


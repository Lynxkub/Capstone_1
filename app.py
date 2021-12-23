from flask import Flask, redirect, render_template, flash, request, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug import datastructures
from models import SalesActual, SalesAvFDollars, SalesAvFPercent, connect_db, db, User, Product, bcrypt, MenuItemIngredients, Menu, MenuItem, SalesForecasting, SalesActual, SalesAvFPercent, SalesAvFDollars, HistoricalSalesInfo
from forms import SignUpForm, SignInForm, NewMenuItemForm, NewMenuForm, WeeklyForecastForm, WeeklyActualsForm
from datetime import date
app=Flask(__name__)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql:///food_cost_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug=DebugToolbarExtension(app)

connect_db(app)

now = date.today()

curr_user = 'username'
# ######################### Login/logout pages  ############################





@app.route('/')
def landing_page():
    """Landing Page"""

    return render_template('home.html')

@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    """Sign Up Page"""
    form = SignUpForm()

    if form.validate_on_submit():

        user = User.signup(
            username = form.username.data,
            password = form.password.data,
            restaurant_name = form.restaurant_name.data,
            location = form.location.data or 'N/A',
            ideal_food_cost = form.ideal_food_cost.data
        )
        session['username'] = user.username
        
        
        db.session.commit()
        flash('User Created')
        return redirect(f'/user/{user.id}')

    return render_template('sign_up.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Login for returning user"""
    form = SignInForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session['username'] = user.username
            session['user_id'] = user.id
            flash(f"Welcome Back {user.username}!")
            
            return redirect(f'/user/{user.id}')
        flash('Invalid credentials')


    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    """Logs user out of application"""
    session.pop('username')
    session.pop('user_id')
    flash('Successfully Logged Out')
    return redirect('/')


# ########################## User Pages ###############################

@app.route('/user/<int:user_id>')
def user_home_page(user_id):
    """Shows user home page"""
    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')
   
    user = User.query.get_or_404(user_id)
    menus = Menu.query.filter(Menu.user_id == user.id)
    session['user_id'] = user.id
    return render_template('user_home_page.html', user=user, menus = menus)

@app.route('/edit_profile', methods = ['GET', 'POST'])
def edit_user_profile():
    """Edit user profile"""
    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')


    user = User.query.get_or_404(session['user_id'])
    form = SignUpForm(obj = user)

    if form.validate_on_submit():
        username = user.username
        password = form.password.data
        if User.authenticate(username, password) == False:
            flash('Password does not match. Cannot change password')
            return redirect(f'/user/{user.id}')
        else:
            user.username = form.username.data
            user.restaurant_name = form.restaurant_name.data,
            user.location = form.location.data or 'N/A',
            user.ideal_food_cost = form.ideal_food_cost.data
            session['username'] = user.username
            db.session.add(user)
            db.session.commit()
            flash('Changes Successful')
            return redirect(f'/user/{user.id}')


    return render_template('edit_user.html', form = form, user = user)


# ########################## Menu Pages ####################################

@app.route('/new_menu', methods = ['GET', 'POST'])
def create_new_menu():
    """Create new menu for user"""
    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')

    form = NewMenuForm()
    user = User.query.get_or_404(session['user_id'])
    if form.validate_on_submit():
        new_menu = Menu(
            user_id = user.id,
            menu_name = form.menu_name.data ,
            menu_description = form.menu_description.data
        )
        db.session.add(new_menu)
        db.session.commit()
        flash('Created New Menu')
        return redirect(f'/user/{user.id}')

    return render_template('new_menu.html', form = form)
    


@app.route('/new_menu_items/<int:menu_id>', methods = ['GET', 'POST'])
def create_new_menu_items(menu_id):
    """Create new menu items for user"""
    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')

    form = NewMenuItemForm()
    curr_menu = Menu.query.get_or_404(menu_id)
    user = User.query.get_or_404(session['user_id'])
    if request.method == 'POST':
        data = request.json
        print(data)
        menu_item = MenuItem(
            user_id = user.id,
            menu_id = curr_menu.id,
            menu_item_name = data['menu_item_name'],
            menu_description = data['menu_description'],
            menu_price = data['menu_price'],
            plate_price = 0.00
        )
        db.session.add(menu_item)
        db.session.commit()
  
        flash('Created New Menu Item')
        return redirect(f'/new_menu_items/{curr_menu.id}')
        

    return render_template('new_menu_item.html', form = form, menu=curr_menu)


@app.route('/api/menu/<int:id>', methods = ['DELETE'])
def delete_menu(id):
    """Delete a menu"""
    menu = Menu.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    return jsonify(message = 'deleted')






#  ############################# Product Pages #############################

# @app.route('/add_product')
# def add_product():
#     """Add product to a menu"""
#     return render_template('add_product.html')




# ########################### Inventory Pages##################################






# ########################## Sales Forecasting Pages ###########################


@app.route('/sales', methods = ['GET', 'DELETE'])
def sales_home_page():
    """Users sales home page that shows sales forecasts and data"""

    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')
    user = User.query.get_or_404(session['user_id'])
    forecast = SalesForecasting.query.get(user.id)
    actuals = SalesActual.query.get(user.id)
    avf_dollars = SalesAvFDollars.query.get(user.id)
    avf_percent = SalesAvFPercent.query.get(user.id)
    return render_template('sales_homepage.html', user = user, forecast = forecast, actuals = actuals, avf_dollars = avf_dollars, avf_percent = avf_percent)

@app.route('/update_forecast', methods = ['GET', 'POST'])
def update_forecast():
    """Allows user to update their forecast for the week"""


    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')


    user = User.query.get_or_404(session['user_id'])
    avf_percent = SalesAvFPercent.query.get(session['user_id'])
    form = WeeklyForecastForm()
    if form.validate_on_submit():
        forecast = SalesForecasting(
            store_id = user.id,
            monday = form.monday.data,
            tuesday = form.tuesday.data,
            wednesday = form.wednesday.data,
            thursday = form.thursday.data,
            friday = form.friday.data,
            saturday = form.saturday.data,
            sunday = form.sunday.data,
            weekly_total = form.monday.data + form.tuesday.data + form.wednesday.data + form.thursday.data + form.friday.data + form.saturday.data + form.sunday.data
        )
        db.session.add(forecast)
        db.session.commit()
        actuals = SalesActual.query.get(session['user_id'])
        if actuals == None:
            sales_actuals = SalesActual(
            store_id = user.id,
            monday = 0,
            tuesday = 0,
            wednesday = 0,
            thursday = 0,
            friday = 0,
            saturday = 0,
            sunday = 0,
            weekly_total = 0)
            db.session.add(sales_actuals)
            db.session.commit

        avf_dollars = SalesAvFDollars.query.get(session['user_id'])
        if avf_dollars == None:
            sales_diff_dollars = SalesAvFDollars(
                store_id = user.id,
                monday = -(forecast.monday),
                tuesday = -(forecast.tuesday),
                wednesday = -(forecast.wednesday),
                thursday = -(forecast.thursday),
                friday = -(forecast.friday),
                saturday = -(forecast.saturday),
                sunday = -(forecast.sunday),
                weekly_total = -forecast.weekly_total
            )
            db.session.add(sales_diff_dollars)
            db.session.commit()
        avf_percent = SalesAvFPercent.query.get(session['user_id'])
        if avf_percent == None:
            sales_diff_percent = SalesAvFPercent(
                store_id = user.id,
                monday = -100,
                tuesday = -100,
                wednesday = -100,
                thursday = -100, 
                friday = -100,
                saturday = -100,
                sunday = -100, 
                weekly_total = -100
            )
            db.session.add(sales_diff_percent)
            db.session.commit()
        # sales_info = [sales_actuals, forecast, sales_diff_dollars, sales_diff_percent]
        # for i in sales_info:
        #     db.session.add(i)
        # db.session.commit()
        flash('Forecast Submitted')
        return redirect('/sales')
    return render_template('update_forecast.html', form = form, user = user)

@app.route('/update_actuals', methods = ['GET', 'POST'])
def update_actuals():
    """Allow user to update currently weekly actual sales"""

    if curr_user not in session:
        flash('Please login to access')
        return redirect('/login')
    user = User.query.get_or_404(session['user_id'])
    actuals = SalesActual.query.get(session['user_id'])
    form = WeeklyActualsForm(obj = actuals)
    return render_template('update_actuals.html', form = form, user = user)



@app.route('/insert_actuals', methods = ['POST'])
def insert_actuals():
    actuals = SalesActual.query.get(session['user_id'])
    forecast = SalesForecasting.query.get(session['user_id'])
    avf_dollars = SalesAvFDollars.query.get(session['user_id'])
    avf_percent = SalesAvFPercent.query.get(session['user_id'])
    sales_delete = [actuals, avf_dollars, avf_percent]
    for i in sales_delete:
        db.session.delete(i)
    db.session.commit()
    form = WeeklyActualsForm()
    if form.validate_on_submit():
        new_actuals = SalesActual(
        store_id = session['user_id'],
        monday = form.monday.data,
        tuesday = form.tuesday.data,
        wednesday = form.wednesday.data,
        thursday = form.thursday.data,
        friday = form.friday.data,
        saturday = form.saturday.data,
        sunday = form.sunday.data,
        weekly_total = form.monday.data + form.tuesday.data + form.wednesday.data + form.thursday.data + form.friday.data + form.saturday.data + form.sunday.data
    )
        avf_dollars = SalesAvFDollars(
            store_id = session['user_id'],
            monday = new_actuals.monday -forecast.monday,
            tuesday = new_actuals.tuesday - forecast.tuesday,
            wednesday = new_actuals.wednesday -forecast.wednesday,
            thursday = new_actuals.thursday -forecast.thursday,
            friday = new_actuals.friday -forecast.friday,
            saturday = new_actuals.saturday -forecast.saturday,
            sunday = new_actuals.sunday -forecast.sunday,
            weekly_total = (new_actuals.monday -forecast.monday) + (new_actuals.tuesday - forecast.tuesday) + (new_actuals.wednesday -forecast.wednesday) + (new_actuals.thursday -forecast.thursday) + (new_actuals.friday -forecast.friday) + (new_actuals.saturday -forecast.saturday) + (new_actuals.sunday -forecast.sunday)
        )
        avf_percent = SalesAvFPercent(
            store_id = session['user_id'],
            monday = round((avf_dollars.monday / forecast.monday) * 100, 2),
            tuesday = round((avf_dollars.tuesday / forecast.tuesday) * 100, 2),
            wednesday = round((avf_dollars.wednesday / forecast.wednesday) * 100,2),
            thursday = round((avf_dollars.thursday / forecast.thursday) * 100, 2),
            friday = round((avf_dollars.friday / forecast.friday) * 100, 2),
            saturday = round((avf_dollars.saturday / forecast.saturday) * 100, 2),
            sunday = round((avf_dollars.sunday / forecast.sunday) * 100, 2),
            weekly_total = round((((avf_dollars.monday / forecast.monday) * 100) + ((avf_dollars.tuesday / forecast.tuesday) * 100) + ((avf_dollars.wednesday / forecast.wednesday) * 100) + ((avf_dollars.thursday / forecast.thursday) * 100) + ((avf_dollars.friday / forecast.friday) * 100) + ((avf_dollars.saturday / forecast.saturday) * 100) + ((avf_dollars.sunday / forecast.sunday) * 100)) / 7 , 2)
        )
    sales_info = [new_actuals, avf_dollars, avf_percent]
    for i in sales_info:
        db.session.add(i)
    db.session.commit()
    return redirect('/sales')

@app.route('/confirm_sales_submit')
def comfirm_sales():
    """Page for user to confirm submitting sales"""
    user = User.query.get(session['user_id'])
    return render_template('confirm_sales.html', user = user)


@app.route('/submit_sales', methods = ['POST'])
def submit_sales():
    """Submits sales to historical data table and resets currents back to zero"""

    user = User.query.get(session['user_id'])
    forecast = SalesForecasting.query.get(user.id)
    actuals = SalesActual.query.get(user.id)
    avf_dollars = SalesAvFDollars.query.get(user.id)
    avf_percent = SalesAvFPercent.query.get(user.id)
    logged_sales = HistoricalSalesInfo.query.filter(HistoricalSalesInfo.store_id == user.id).all()
    if len(logged_sales) == 0:
        week = 1
    else: 
        week = len(logged_sales) + 1
    historic_sales = HistoricalSalesInfo(
        store_id = user.id,
        date_logged = now,
        monday_forecasted = forecast.monday,
        tuesday_forecasted = forecast.tuesday,
        wednesday_forecasted = forecast.wednesday,
        thursday_forecasted = forecast.thursday,
        friday_forecasted = forecast.friday,
        saturday_forecasted = forecast.saturday,
        sunday_forecasted = forecast.sunday,
        monday_actual = actuals.monday,
        tuesday_actual = actuals.tuesday,
        wednesday_actual = actuals.wednesday,
        thursday_actual = actuals.thursday,
        friday_actual = actuals.friday,
        saturday_actual = actuals.saturday,
        sunday_actual = actuals.sunday,
        forecasted_total = forecast.weekly_total,
        actual_total = actuals.weekly_total,
        week = week
    )
    db.session.add(historic_sales)
    db.session.commit()
    weekly_data = [forecast, actuals, avf_dollars, avf_percent]
    for i in weekly_data:
        db.session.delete(i)
    db.session.commit()
    flash('Sales reset and logged into historical sales data')
    return redirect('/sales')

@app.route('/historic_sales/<int:user_id>')
def historic_sales(user_id):
    """Page that lists all users weeks of logged data for them to choose from"""
    user = User.query.get(user_id)
    h_sales = HistoricalSalesInfo.query.filter(HistoricalSalesInfo.store_id == user_id).all()
    

    return render_template('historic_sales.html', user = user, h_sales = h_sales)


@app.route('/historical/week_<int:week>')
def weekly_historic_details(week):
    """Displays a page of a specific historical weekly sales data"""
    user = User.query.get(session['user_id'])
    sales_week = HistoricalSalesInfo.query.filter((HistoricalSalesInfo.store_id == user.id) & (HistoricalSalesInfo.week == week)).first()

    return render_template('historic_week_sales_data.html', user = user, sales_week = sales_week)



# Sales section complete. Will need to style in the future. But next project is working on the products tables


# add in log in validation to all routes

# Need to add patch route to update weekly actuals

# Todo list for this app:
# create/implement all sales info
# create/implement all inventory info
# implement product calls for recipes
# make it look nice

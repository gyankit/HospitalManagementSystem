from HMS import bcrypt
from HMS.main import main
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from HMS.main.forms import LoginForm, SearchForm
from HMS.models import User, Patient


#Login Routes
@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    title = 'Namaste Hospitals | Login'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            nexturl = request.args.get('next')
            return redirect(nexturl or url_for('main.home'))
        else:
            flash('Wrong Login Credientials', 'danger')
    return render_template('main/login.html', title=title, form=form)


#Logout Routes
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


#Home Routes
@main.route('/home')
@login_required
def home():
    title = 'Namaste Hospitals | Home'
    return render_template('main/home.html')

#About Us Route
@main.route("/aboutus")
@login_required
def aboutus():
    title = 'Namaste Hospitals | About Us'
    return render_template('main/aboutus.html', title=title)


#Contact Us Route
@main.route("/contactus")
@login_required
def contactus():
    title = 'Namaste Hospitals | Contact Us'
    return render_template("main/contactus.html", title=title)


#Services Route
@main.route("/services")
@login_required
def services():
    title = 'Namaste Hospitals | Services'
    return render_template("main/services.html", title=title)


#Patient Search Routes
@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    nexturl = request.args.get('next')
    if nexturl is None:
        abort(403)
    title = 'Namaste Hospitals | Search'
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for(nexturl, pid=request.form.get('patientid')))  
    return render_template('main/search.html', title=title, form=form)
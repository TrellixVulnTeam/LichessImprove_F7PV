from flask import render_template, url_for, flash, redirect, request
from chessapp import app, db, bcrypt
from chessapp.forms import RegistrationForm, LoginForm
from chessapp.database import User, Game
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/ApiHttpError.html"), 404


@app.route('/')
def home_page():
    return render_template("index.html", current_time=datetime.utcnow())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created")
        return redirect(url_for("login"))
    return render_template("auth/register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Login Unsuccesful')
    return render_template("auth/login.html", title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/profile/<username>')
def game_page(username):
    return render_template("game.html")


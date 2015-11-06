__author__ = 'lufee'
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, \
    login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm


# @auth.before_app_request()
# def before_request():
#     if current_user.is_authenticated():
#         current_user.ping()
#         if not current_user.confirmed \
#             and request.endpoint[:5] != 'auth.'\
#             and request.endpoint != 'static':
#             return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GEt', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me)
            return redirect('/welcome')
        flash('Invalid username or password.')
    return render_template("auth/login.html",form = form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("main.index"))
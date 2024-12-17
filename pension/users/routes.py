from flask import Blueprint, abort, render_template, url_for, request, session, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from pension import db, logger
from pension.models import User
from pension.users.forms import RegistrationForm, LoginForm
from pension.main.utils import escape, check
from html import escape

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Already signed in", "info")
        return redirect(url_for("main.index"))
    form= RegistrationForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("Please fill the form correctly !", "danger")
            return render_template("register.html", title= "Register", form=form)
        
        username = escape(form.username.data)
        email = escape(form.email.data)
        password = escape(form.password.data)
        confrimp = escape(form.confirmpassword.data)
        contact= form.contact.data
        if username is None or email is None or password is None or confrimp is None or contact is None:
            flash("All Fields are required !", "danger")
            return render_template("register.html", title= "Register", form=form)
        elif password != confrimp:
            flash("Password & Confirm Password are not the same !", "danger")
            return render_template("register.html", title= "Register", form=form)
        elif not check(email):
            flash("Email not correct !", "danger")
            return render_template("register.html", title= "Register", form=form)
        else: 
            hash=generate_password_hash(password=password)
            user = User(username=username,email=email,password=hash,contact=contact)
            try: 
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                logger.error(e) 
                flash("An error occurred at database level. cannot proceed", "danger")
                return redirect(url_for('users.register'))    

            return redirect(url_for('users.login'))    
    return render_template("register.html", title= "Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in", "info")
        return redirect(url_for("main.index"))
    form= LoginForm()
    if request.method=="POST":     
        if not form.validate_on_submit():
            flash("The email or password you provided is incorrect. Please try Again !", "danger")
            return redirect(url_for('users.login'))
        user = User.query.filter_by(email=escape(form.email.data)).first()
        password = escape(form.password.data)
        if not user:
            flash("The email you provided is incorrect, Please try Again! ", "danger")
            return redirect(url_for('users.login'))
        if not check_password_hash(user.password, password=password):
            flash("The password you provided is incorrect, Please try Again! ", "danger")
            return redirect(url_for('users.login'))
        login_user(user)
        flash(f"Welcome {user.username}!", "success")
        return redirect(url_for('main.index'))
            
    return render_template("login.html", title= "Register", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "info")
    return redirect(url_for('users.login'))

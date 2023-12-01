from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_manager import DB_Manager
from datetime import date
from hashlib import sha256
from flask_login import login_user, logout_user, login_required
from server.User import User
import secrets

from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get("hashedPassword")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    DB.disconnect()

    
    user = User(email)

    if not data:
        data = ["Fail", "aa"*32]

    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
        user = User(data[2])
        login_user(user, remember=True)
        return redirect(url_for('main.profile'))

    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    joining = date.today()
    password = request.form.get("hashedPassword")
    salt = secrets.token_hex(32)
    pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(salt), bytes.fromhex(password)))).hexdigest()

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    if DB.get_login_data_by_mail(email):
        DB.disconnect()
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    else:
        DB.insert_user(("NULL", email, fname, lname, joining, pw), salt)
        DB.show_all_users()
        DB.disconnect()

    return redirect(url_for('auth.login'))




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
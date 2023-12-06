from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_manager import DB_Manager
from datetime import date
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user
from server.User import User
import secrets
import pyotp
import base64
import qrcode
from io import BytesIO


from functools import wraps
from flask import abort

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user._role != 'admin':
            abort(403)  # 403 Forbidden
        return func(*args, **kwargs)
    return decorated_view


from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get("hashedPassword")
    otp = request.form.get("otp")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)

    if not data:
        data = ["Fail", "aa"*32]
        mfa = [None]
    else:
        mfa = DB.get_mfa_by_id(data[2])
    DB.disconnect()
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if mfa[0] and not otp and user_pw == data[0]:
        return render_template("login_2fa.html", email = email, password = password)


    if user_pw == data[0]:
        if mfa[0]:
            if pyotp.TOTP(mfa[0]).verify(otp):
                user = User(data[2])
                login_user(user, remember=True)
                return redirect(url_for('main.profile'))
        else:
            user = User(data[2])
            login_user(user, remember=True)
            return redirect(url_for('main.profile'))

    
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

@auth.route("/signup/2fa/")
@login_required
def signup_2fa():
    # Generating random secret key for authentication
    secret = pyotp.random_base32()

    mail = current_user._email
    # Generate OTP URI for QR Code
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(mail, issuer_name='LB-Company')

    # Generate QR Code
    qr = qrcode.make(otp_uri)

    # Convert QR Code image to base64 format
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template("signup_2fa.html", secret=secret, qr_code=qr_base64)

@auth.route("/signup/2fa/", methods=["POST"])
@login_required
def signup_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = request.form.get("otp")
    id = current_user._id
    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        DB.show_all_users()
        DB.update_user((id, "mfa", secret))
        DB.show_all_users()
        DB.disconnect()

        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for('main.profile'))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token! Please scan the new QR-Code!", "danger")
        return redirect(url_for("auth.signup_2fa"))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Nur Administratoren haben Zugriff
    return render_template('admin_dashboard.html')

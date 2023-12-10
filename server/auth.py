from flask import Blueprint, render_template, redirect, url_for, request, flash
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
from server.validators import Validator


from functools import wraps
from flask import abort

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user._role != 'admin':
            abort(404) 
        return func(*args, **kwargs)
    return decorated_view


from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', user_authenticated = current_user.is_authenticated)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get("hashedPassword")
    if email != "admin@admin":
        if not Validator.is_email(email) or not Validator.is_sha256_hash(password):
            flash("Leider scheinen sie eine ungültige Eingabe zu tätigen")
            return redirect(url_for('auth.login'))

    otp = request.form.get("otp")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    if not data:
        data = ["Fail", "aa"*32, 0, 0]
        mfa = [None]   
    else:
        mfa = DB.get_mfa_by_id(data[2])


    DB.disconnect()

    if data[3] >=8:
        flash('Dein Account wurde wegen zu vielen fehlerhaften Loginversuchen gesperrt')
        return redirect(url_for('auth.login'))

    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if mfa[0] and not otp and user_pw == data[0]:
        return render_template("login_2fa.html", email = email, password = password, user_authenticated = current_user.is_authenticated)


    if user_pw == data[0]:
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        DB.update_user((data[2], "failed_login", 0))
        DB.disconnect()
        if mfa[0]:
            if pyotp.TOTP(mfa[0]).verify(otp):
                user = User(data[2])
                login_user(user, remember=True)
                return redirect(url_for('main.profile'))
        else:
            user = User(data[2])
            login_user(user, remember=True)
            return redirect(url_for('main.profile'))

    if data[0] != "Fail":
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        counter = data[3]+ 1
        DB.update_user((data[2], "failed_login", counter))
        DB.disconnect()
    
    if data[3] >= 4:
        if 8-data[3]-1 > 0: 
            flash(f'Dein Account wird nach {8-data[3]-1} weiteren fehlgeschlagen Loginversuchen gesperrt')
        else:
            flash('Dein Account wurde wegen zu vielen fehlerhaften Loginversuchen gesperrt')
    else:
        flash('Bitte überprüfe deine Logindaten und versuche es erneut.')
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html', user_authenticated = current_user.is_authenticated)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    password = request.form.get("hashedPassword")
    if not Validator.is_email(email) or not Validator.is_sha256_hash(password) or not Validator.is_name(fname) or not Validator.is_name(lname):
        flash("Leider scheinen sie eine ungültige Eingabe zu tätigen")
        return redirect(url_for('auth.signup'))

    joining = date.today()
    salt = secrets.token_hex(32)
    pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(salt), bytes.fromhex(password)))).hexdigest()

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    if DB.get_login_data_by_mail(email):
        DB.disconnect()
        flash('Email existiert bereits')
        return redirect(url_for('auth.signup'))
    else:
        DB.insert_user(("NULL", email, fname, lname, joining, pw), salt)
        DB.disconnect()

    return redirect(url_for('auth.login'))

@auth.route("/signup/2fa/")
@login_required
def signup_2fa():
    secret = pyotp.random_base32()
    mail = current_user._email
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(mail, issuer_name='LB-Company')
    qr = qrcode.make(otp_uri)

    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template("signup_2fa.html", secret=secret, qr_code=qr_base64, user_authenticated = current_user.is_authenticated)

@auth.route("/signup/2fa/", methods=["POST"])
@login_required
def signup_2fa_form():
    secret = request.form.get("secret")
    otp = request.form.get("otp")
    id = current_user._id
    if pyotp.TOTP(secret).verify(otp):
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        DB.update_user((id, "mfa", secret))
        DB.disconnect()

        flash("Der 2FA Token ist gültig", "success")
        return redirect(url_for('main.profile'))
    else:
        flash("Der 2FA Token ist nicht gültig! Bitte den neuen QR-Code scannen!", "danger")
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
    return render_template('admin_dashboard.html', user_authenticated = current_user.is_authenticated)

@auth.route('/reset_password')
@login_required
def reset_password():
    return render_template('reset_password.html', user_authenticated = current_user.is_authenticated)

@auth.route('/reset_password', methods=['POST'])
@login_required
def reset_password_post():
    email = current_user._email
    password = request.form.get("hashedPasswordOld")

    if not Validator.is_sha256_hash(password):
        flash("Leider scheinen sie eine ungültige Eingabe zu tätigen")
        return redirect(url_for('auth.reset_password'))

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
            password = request.form.get("hashedPasswordNew")
            if not Validator.is_sha256_hash(password):
                flash("Leider scheinen sie eine ungültige Eingabe zu tätigen")
                return redirect(url_for('auth.reset_password'))

            salt = secrets.token_hex(32)
            pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(salt), bytes.fromhex(password)))).hexdigest()
            DB = DB_Manager("database/kundendatenbank.sql", "users")
            DB.connect()
            DB.update_user((current_user._id, "password", pw))
            DB.update_user((current_user._id, "salt", salt))
            DB.disconnect()
            flash("Passwort erfolgreich geändert", 'success')
            return redirect(url_for('main.profile'))

    
    flash('Falsches Password')
    return redirect(url_for('auth.reset_password'))


@auth.route('/delete_account')
@login_required
def delete_account():
    return render_template('delete_account.html', user_authenticated = current_user.is_authenticated)

@auth.route('/delete_account', methods=['POST'])
@login_required
def delete_account_post():
    email = current_user._email
    password = request.form.get("hashedPassword")

    if not Validator.is_sha256_hash(password):
        flash("Leider scheinen sie eine ungültige Eingabe zu tätigen")
        return redirect(url_for('auth.delete_account'))

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
        if data[2] != 1:
            id = current_user._id
            logout_user()
            DB = DB_Manager("database/kundendatenbank.sql", "users")
            DB.connect()
            DB.delete_user(id)
            DB.disconnect()
            return redirect(url_for('main.index'))
        
        else:
            flash("Der Admin Account kann nicht gelöscht werden")
            return redirect(url_for('auth.delete_account'))

    flash("Falsches Passwort")
    return redirect(url_for('auth.delete_account'))


@auth.route('/delete_2fa')
@login_required
def delete_2fa():
    return render_template('delete_2fa.html', user_authenticated = current_user.is_authenticated)

@auth.route('/delete_2fa', methods=['POST'])
@login_required
def delete_2fa_post():
    email = current_user._email
    password = request.form.get("hashedPassword")

    if not Validator.is_sha256_hash(password):
        flash("Leider scheinen sie eine ungültige Eingabe zu tätigen")
        return redirect(url_for('auth.delete_2fa'))

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    role = DB.get_role_by_id(data[2])
    mfa = DB.get_mfa_by_id(data[2])
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
        if not mfa[0]:
            flash("Es ist keine 2FA aktiviert")
            return redirect(url_for('auth.delete_2fa'))

        if role[0] != "admin":
            id = current_user._id
            DB = DB_Manager("database/kundendatenbank.sql", "users")
            DB.connect()
            DB.remove_mfa(id)
            DB.disconnect()
            flash("2FA wurde entfernt")
            return redirect(url_for('main.profile'))
        
        else:
            flash("Admin Accounts benötigen 2FA")
            redirect(url_for('auth.delete_2fa'))

    flash("Falsches Passwort")
    return redirect(url_for('auth.delete_2fa'))

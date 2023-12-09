from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_manager import DB_Manager
from datetime import date
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user
from server.User import User
import secrets
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

admin= Blueprint('admin', __name__)


@admin.route('/admin/dashboard/delete_user')
@login_required
@admin_required
def delete_user():
    print("delete")
    return render_template('admin_delete_user.html', user_authenticated = current_user.is_authenticated)


@admin.route('/admin/dashboard/delete_user', methods=['POST'])
@login_required
@admin_required
def delete_user_post():
    email = request.form.get("email")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_id_by_mail(email)
    if not data:
        DB.disconnect()
        flash('Nutzer mit dieser Email existiert nicht')
        return redirect(url_for('admin.delete_user'))
    else:
        DB.delete_user(data[0])
        DB.disconnect()
        flash('Nutzer wurde erfolgreich gelöscht')
        return redirect(url_for('auth.admin_dashboard'))

@admin.route('/admin/dashboard/grant_rights')
@login_required
@admin_required
def grant_rights():
    print("delete")
    return render_template('admin_grant_rights.html', user_authenticated = current_user.is_authenticated)


@admin.route('/admin/dashboard/grant_rights', methods=['POST'])
@login_required
@admin_required
def grant_rights_post():
    email = request.form.get("email")
    role = request.form.get("role")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_id_by_mail(email)
    mfa = DB.get_mfa_by_id(data[0])

    if not data:
        DB.disconnect()
        flash('Nutzer mit dieser Email existiert nicht')
        return redirect(url_for('admin.grant_rights'))
    
    if data[0] == current_user._id or data[0] == 1:
        DB.disconnect()
        flash('Du kannst dir selbst und dem Admin Account keine Rechte zuweisen/entziehen')
        return redirect(url_for('admin.grant_rights'))
    
    if not mfa[0] and role == "admin":
        DB.disconnect()
        flash('Admin Accounts benötigen 2FA')
        return redirect(url_for('admin.grant_rights'))
    

    else:
        DB.update_user((data[0], "role", role))
        DB.disconnect()
        role = role.capitalize()
        flash(f'{role}rechte wurden erfolgreich zugewiesen')
        return redirect(url_for('auth.admin_dashboard'))

@admin.route('/admin/dashboard/unlock_account')
@login_required
@admin_required
def unlock_account():
    return render_template('admin_unlock_account.html', user_authenticated = current_user.is_authenticated)


@admin.route('/admin/dashboard/unlock_account', methods=['POST'])
@login_required
@admin_required
def unlock_account_post():
    email = request.form.get("email")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_id_by_mail(email)

    if not data:
        DB.disconnect()
        flash('Nutzer mit dieser Email existiert nicht')
        return redirect(url_for('admin.unlock_account'))
    
    else:

        DB.update_user((data[0], "failed_login", 0))
        DB.disconnect()
        flash(f'Loginversuche wurden erfolgreich zurückgesetzt')
        return redirect(url_for('auth.admin_dashboard'))


@admin.route('/admin/dashboard/remove_password')
@login_required
@admin_required
def remove_password():
    return render_template('admin_reset_password.html', user_authenticated = current_user.is_authenticated)


@admin.route('/admin/dashboard/remove_password', methods=['POST'])
@login_required
@admin_required
def remove_password_post():
    email = request.form.get("email")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_id_by_mail(email)

    if not data:
        DB.disconnect()
        flash('Nutzer mit dieser Email existiert nicht')
        return redirect(url_for('admin.remove_password'))
    
    else:
        random_hex = secrets.token_hex(5)
        hash = sha256(random_hex.encode()).hexdigest()
        salt = secrets.token_hex(32)
        pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(salt), bytes.fromhex(hash)))).hexdigest()
        DB.update_user((data[0], "password", pw))
        DB.update_user((data[0], "salt", salt))
        DB.disconnect()
        flash(f'Das neue Passwort ist {random_hex}')
        return redirect(url_for('auth.admin_dashboard'))


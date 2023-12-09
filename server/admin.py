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

admin= Blueprint('admin', __name__)


@admin.route('/admin/delete_user')
@login_required
@admin_required
def delete_user():
    print("delete")
    return render_template('admin_dashboard.html', user_authenticated = current_user.is_a)

@admin.route('/admin/reset_password')
@login_required
@admin_required
def reset_user_pw():
    print("add")
    return render_template('admin_dashboard.html', user_authenticated = current_user.is_a)

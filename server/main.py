from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required
from . import db
import requests

main = Blueprint('main', __name__)

class SmartmeterDataHandler():
    _bearer = "axsGqZTjZtwoTnxxPINHqTLWuFNnEL"

    def get_data(self, email):
        header = {'Content-type': 'application/json', 'Authorization':f'Bearer {self._bearer}'}
        url = f"https://smartmeter.mwoelke.de/api/customers/{email}"
        response = requests.get(url=url, headers=header)
        if response.status_code == 404:
            return []
        else:
            response = response.json()
            print(response)
        return response["smartmeters"]


SMARTMETER_HANDLER = SmartmeterDataHandler()

@main.route('/')
def index():
    return render_template('index.html', user_authenticated = current_user.is_authenticated)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user._name, user_authenticated = current_user.is_authenticated)

@main.route('/smartmeters')
@login_required
def view_smartmeters():
    email = current_user._email
    response = SMARTMETER_HANDLER.get_data(email)

    if not response:
        flash('Du hast leider keine Smartmeter bei uns registriert.')

    return render_template('smartmeters.html', data = response, user_authenticated = current_user.is_authenticated)
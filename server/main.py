from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from database.db_manager import DB_Manager
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

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    contract = DB.get_contract(current_user._id)
    DB.disconnect()
    if not contract:
        flash("Kein Vertrag gefunden")
        return redirect(url_for('main.profile'))

    if not response:
        flash('Du hast leider keine Smartmeter bei uns registriert.')

    if contract[0] == 2:
        multi = 0.3

    if contract[0] == 1:
        multi = 0.5

    for smartmeter in response:
        value = round(multi * smartmeter["counter"], 2)
        smartmeter["contract"] = f"{value} €"

    return render_template('smartmeters.html', data = response, user_authenticated = current_user.is_authenticated)


@main.route('/contract_details')
@login_required
def contract_details():
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    contract = DB.get_contract(current_user._id)
    DB.disconnect()
    if not contract:
        flash("Kein Vertrag gefunden")
        return redirect(url_for('main.profile'))

    print(contract)
    return render_template('contract_details.html', contract=str(contract[0]), user_authenticated = current_user.is_authenticated)

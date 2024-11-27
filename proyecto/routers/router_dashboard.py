from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory

from .router_login import session

home_dashboard = Blueprint("views_dashboard", __name__)

#ruta de dasboard
@home_dashboard.route('/dashboard/<int:id>',methods=['GET', 'POST'])
def dashboard(id):
    if 'Esta_logeado' in session:
        return render_template('dashboard.html', id = id)
    return redirect(url_for('views_login.login'))

#ruta dashboard administrador
@home_dashboard.route('/dashboard_admin')
def dashboard_admin():
    if 'Esta_logeado' in session:
        return render_template('dashboardAdmin.html')
    return redirect(url_for('views_login.login'))
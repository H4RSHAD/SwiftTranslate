from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory
from datetime import datetime

from ..controllers import SuscripcionController

home_suscripcion = Blueprint("views_suscripcion", __name__)

@home_suscripcion.route('/suscripcion_create/<int:id>', methods=['POST', 'GET'])
def suscripcion_create(id):
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            subs = {
                'id_user': request.form['id'],
                'id_plan': request.form['id_plan'],
                'start_date': datetime.now(),
                'state': request.form['state']
            }
            SuscripcionController.create(subs)
            data = SuscripcionController.getById(id)
            print(data)
            return render_template('suscripcion.html', id = id, data = data)
        return render_template("plans.html", id = id)
    return redirect(url_for('views.login'))


@home_suscripcion.route('/suscripcion/<int:id>', methods=['POST', 'GET'])
def suscripcion(id):
    if 'Esta_logeado' in session:
        data = SuscripcionController.getById(id)
        return render_template('suscripcion.html', id = id, data = data)
    return redirect(url_for('views.login'))
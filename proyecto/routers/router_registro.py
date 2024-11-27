from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory
import threading
from datetime import datetime

# importamos los controladores de Usuario
from ..controllers import UserController
# importamos los Modelos de usuario
from ..models.User import User


home_registro = Blueprint("views_registro", __name__)
# ----------------------HOME------------------------------

#ruta de registro de usuario
@home_registro.route('/register', methods=['GET', 'POST'])
def register():
    time_creacion = datetime.now()  # guardamos la fecha y hora en la que se registrará
    # si el metodo es post, es decir, si se envio el formulario
    if request.method == "POST":
        data = request.form
        print('------datos ingresados por formulario-------')
        print(data)
        usuario = User(data['name'], data['email'], data['password'], data['id_rol'], data['state'], time_creacion)
        # capturo los datos del formulario y mando al modelo User
        # los 0 son nulos porque no metemos desde formulario
        UserController.create(usuario)
        flash('Usuario registrado con exito')
        return redirect(url_for('views_login.login'))

    return render_template('register.html')
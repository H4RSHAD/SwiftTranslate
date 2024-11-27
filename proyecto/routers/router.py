from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory
import threading
from datetime import datetime


# importamos los controladores de Usuario
from ..controllers import UserController

# importamos los Modelos de usuario
from ..models.User import User, Plan
import os
import time
from werkzeug.utils import secure_filename
from proyecto.database.connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 
from werkzeug.security import generate_password_hash


home = Blueprint("views", __name__)
# ----------------------HOME------------------------------
# funciones decoradas, (para que puedan ser usadas en otro archivo)
@home.route('/', methods=['GET'])
def home_():
    """
    Cargar Usuario Admin
    """
    user = User(name="admin", email="admin@gmail.com",password = generate_password_hash("12345678"), id_rol = 1, state= "activo", create_at= datetime.now() )
    if User.query.filter_by(email=user.email).first():
        print("Usuario Admin ya esta registrado")
        flash('Usuario Admin ya esta registrado', 'danger')
        
    else:   
        sql = "INSERT INTO roles (id, rol) VALUES (%s, %s);"
        _fetch_none(sql, (1, 'Administrador'))
        _fetch_none(sql, (2, 'Usuario'))
        sql2 = "INSERT INTO plans (id, name, description, monthly_price) VALUES (%s, %s, %s, %s)"
        _fetch_none(sql2,(1,'Basico', 'Este plan es el mas basico', 70))
        _fetch_none(sql2,(2,'Intermedio', 'Este plan es el mas Intermedio', 120))
        _fetch_none(sql2,(3,'Profesional', 'Este plan es el mas Profesional', 150))
        UserController.create(user)

    return render_template("home.html")


#ruta de login
@home.route('/login', methods=['GET', 'POST'])
def login():
    # si el metodo es post, es decir, si se envio el formulario
    if request.method == 'POST':
        data = request.form  # guardo todos los datos ingresados por formulario de la vista
        print('------datos ingresados por formulario-------')
        usuario = User(0, data['email'], data['password'],0 , 0, 0)  # capturo los datos del formulario y mando al modelo User
        # los 0 son nulos porque no metemos desde formulario

        logged_user = UserController.login(usuario)
        print('datos del login')
        print(logged_user)
        # si el usuario existe
        if logged_user != None:
            if logged_user.password_hash:
                # guardamos los datos del usuario en la sesion
                session['Esta_logeado'] = True  # Variable para saber si el usuario esta logeado
                # obtenemos todo los datos del usuario
                session['usuario_id'] = logged_user.id
                session['name'] = logged_user.name
                session['email'] = logged_user.email
                session['password'] = logged_user.password_hash
                session['id_rol'] = logged_user.id_rol
                session['state'] = logged_user.state
                session['create_at'] = logged_user.create_at
                if(logged_user.id_rol == 1):
                    return redirect(url_for('views.dashboard_admin'))
                   # return render_template("dashboardAdmin.html")
                else:
                    id = UserController.id_user(usuario)[0]
                    return redirect(url_for('views.dashboard', id = id))  # redirige dashboard que corresponde//////chinin estuvo aquí
            else:
                flash("Usuario o Contraseña invalida")  # Contraseña invalida
                return render_template("login.html")
        else:
            flash("Usuario o Contraseña invalida")  # Usuario no encontrado
            return render_template("login.html")
    else:
        return render_template("login.html")
    


#ruta de registro de usuario
@home.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('views.login'))

    return render_template('register.html')

#ruta de dasboard
@home.route('/dashboard/<int:id>',methods=['GET', 'POST'])
def dashboard(id):
    if 'Esta_logeado' in session:
        return render_template('dashboard.html', id = id)
    return redirect(url_for('views.login'))

#ruta dashboard administrador
@home.route('/dashboard_admin')
def dashboard_admin():
    if 'Esta_logeado' in session:
        return render_template('dashboardAdmin.html')
    return redirect(url_for('views.login'))

#ruta a logaut 
@home.route('/logout')
def logout():
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        session.pop('Esta_logeado', None)
        session.pop('name', None)
        return redirect(url_for('views.home_'))
    return redirect(url_for('views.login'))
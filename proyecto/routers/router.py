from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory
import threading
from datetime import datetime


# importamos los controladores de Usuario
from ..controllers import UserController

# importamos los Modelos de usuario
from ..models.User import User
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
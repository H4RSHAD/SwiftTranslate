from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory

# importamos los controladores de Usuario
from ..controllers import UserController
# importamos los Modelos de usuario
from ..models.User import User


home_login = Blueprint("views_login", __name__)

#ruta de login
@home_login.route('/login', methods=['GET', 'POST'])
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
                    return redirect(url_for('views_dashboard.dashboard_admin'))
                   # return render_template("dashboardAdmin.html")
                else:
                    id = UserController.id_user(usuario)[0]
                    return redirect(url_for('views_dashboard.dashboard', id = id))  # redirige dashboard que corresponde//////chinin estuvo aquí
            else:
                flash("Usuario o Contraseña invalida")  # Contraseña invalida
                return render_template("login.html")
        else:
            flash("Usuario o Contraseña invalida")  # Usuario no encontrado
            return render_template("login.html")
    else:
        return render_template("login.html")



#ruta a logaut 
@home_login.route('/logout')
def logout():
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        session.pop('Esta_logeado', None)
        session.pop('name', None)
        return redirect(url_for('views.home_'))
    return redirect(url_for('views_login.login'))
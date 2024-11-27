from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory


from ..controllers import PlansController

home_planes = Blueprint("views_planes", __name__)

#ruta principal de planes 
@home_planes.route('/plans/<int:id>',methods=['GET', 'POST'])
def plans(id):
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        planes = PlansController.getAll()
        print(planes)  # Verificación de datos
        return render_template("plans.html", plans=planes, id =id)
    return redirect(url_for('views.login'))

#ruta de los administracion de planes
@home_planes.route('/admin_plans/')
def admin_plans():
    if 'Esta_logeado' in session:  # Si el usuario está logeado entonces realiza funcionalidades permitidas
        planes = PlansController.getAll()
        print(planes)  # Verificación de datos
        return render_template("admin_plans.html", plans=planes)
    return redirect(url_for('views.login'))

#ruta de creacion de Planes
@home_planes.route('/admin_plans/create', methods=['GET', 'POST'])
def create_plan():
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            plan_data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'monthly_price': request.form['monthly_price']
            }
            PlansController.create(plan_data)
            return redirect(url_for('views.admin_plans'))
        return render_template("create_plan.html")
    return redirect(url_for('views.login'))

#ruta de actualizacion de los planes 
@home_planes.route('/admin_plans/update/<int:id>', methods=['GET', 'POST'])
def update_plan(id):
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            plan_data = {
                'id': id,
                'name': request.form['name'],
                'description': request.form['description'],
                'monthly_price': request.form['monthly_price']
            }
            PlansController.update(plan_data)
            return redirect(url_for('views.admin_plans'))
        plan = PlansController.getById(id)
        return render_template("update_plan.html", plan=plan)
    return redirect(url_for('views.login'))

#ruta para para eliminar planes 
@home_planes.route('/admin_plans/delete/<int:id>', methods=['POST'])
def delete_plan(id):
    if 'Esta_logeado' in session:
        PlansController.delete(id)
        return redirect(url_for('views.admin_plans'))
    return redirect(url_for('views.login'))

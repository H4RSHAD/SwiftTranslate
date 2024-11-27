from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from proyecto import app
from proyecto.database.connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 

db = SQLAlchemy(app)  # Crea una instancia de SQLAlchemy

# Define la tabla Plan
class Plan(db.Model):
    __tablename__ = 'plans'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna id como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Columna name, no puede ser nula
    description = db.Column(db.Text, nullable=True)  # Columna description, puede ser nula
    monthly_price = db.Column(db.Float, nullable=False)  # Columna monthly_price, no puede ser nula
    
    # Relación inversa con la tabla Subscription
    subscriptions = db.relationship('Subscription', backref='plan', lazy=True)  # Relación uno a muchos con la tabla Subscription

    def __init__(self, name, description, monthly_price):
        self.name = name
        self.description = description
        self.monthly_price = monthly_price
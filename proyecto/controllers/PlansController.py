from ..models.User import Plan
from ..database import plans

# Obtener todos los planes
def getAll() -> list:
    raw_plans = plans.getAll()  # Llama a la función getAll del módulo plans
    # Convierte la lista de tuplas en una lista de diccionarios
    plans_list = [{'id': p[0], 'name': p[1], 'description': p[2], 'monthly_price': p[3]} for p in raw_plans]
    return plans_list

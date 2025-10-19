import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Intentar importar mongomock (no pasa nada si no existe)
try:
    import mongomock
except ImportError:
    mongomock = None

# Cargar variables del archivo .env
load_dotenv()


class CitaService:
    # Profesionales y especialidades disponibles
    ESPECIALIDADES = {
        "Medicina General": ["Carlos Mejia Lopez", "Alejandra Molina Puerta"],
        "Psicologia": ["Alejandro Gomez Bedoya"],
        "Planificacion Familiar": ["Luisa Maria Paez"],
        "Odontologia": ["Jorge Eduardo Arango"]
    }

    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI")

        # 🔹 Si no hay MONGO_URI, o si el entorno pide un mock, usar mongomock
        if (not mongo_uri or "mock" in str(mongo_uri).lower()) and mongomock:
            print("⚙️  Usando base de datos simulada con mongomock (modo test)")
            self.client = mongomock.MongoClient()
        else:
            if not mongo_uri:
                raise ValueError("❌ La variable MONGO_URI no está definida en el entorno.")
            self.client = MongoClient(mongo_uri)

        self.db = self.client["salud_vital"]
        self.citas = self.db["citas"]

    # -------------------------------------------
    # 🔹 Horas disponibles (intervalos de 20 min)
    # -------------------------------------------
    def obtener_horas_disponibles(self, fecha, profesional):
        inicio = datetime.strptime(f"{fecha} 08:00", "%Y-%m-%d %H:%M")
        fin = datetime.strptime(f"{fecha} 17:00", "%Y-%m-%d %H:%M")
        intervalo = timedelta(minutes=20)
        horas = []

        while inicio < fin:
            hora_str = inicio.strftime("%H:%M")
            if not self.citas.find_one({"fecha": fecha, "hora": hora_str, "profesional": profesional}):
                horas.append(hora_str)
            inicio += intervalo

        return horas

    # -------------------------------------------
    # 🔹 CRUD de citas
    # -------------------------------------------
    def agendar_cita(self, nombre, cedula, correo, especialidad, profesional, fecha, hora):
        cita = {
            "nombre": nombre,
            "cedula": cedula,
            "correo": correo,
            "especialidad": especialidad,
            "profesional": profesional,
            "fecha": fecha,
            "hora": hora,
            "creado_en": datetime.now()
        }
        self.citas.insert_one(cita)

    def obtener_citas(self):
        return list(self.citas.find({}, {"_id": 0}))

    def obtener_cita_por_cedula(self, cedula):
        return self.citas.find_one({"cedula": cedula}, {"_id": 0})

    def cancelar_cita(self, cedula):
        self.citas.delete_one({"cedula": cedula})

    def reprogramar_cita(self, cedula, nueva_fecha, nueva_hora, nuevo_profesional, nueva_especialidad):
        self.citas.update_one(
            {"cedula": cedula},
            {"$set": {
                "fecha": nueva_fecha,
                "hora": nueva_hora,
                "profesional": nuevo_profesional,
                "especialidad": nueva_especialidad
            }}
        )

import os
from pymongo import MongoClient
from datetime import datetime, timedelta


class CitaService:
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("❌ La variable MONGO_URI no está definida en el entorno.")

        self.client = MongoClient(mongo_uri)
        self.db = self.client["salud_vital"]
        self.citas = self.db["citas"]

    def obtener_horas_disponibles(self, fecha):
        inicio = datetime.strptime(f"{fecha} 08:00", "%Y-%m-%d %H:%M")
        fin = datetime.strptime(f"{fecha} 17:00", "%Y-%m-%d %H:%M")
        intervalo = timedelta(minutes=30)
        horas = []

        while inicio < fin:
            hora_str = inicio.strftime("%H:%M")
            if not self.citas.find_one({"fecha": fecha, "hora": hora_str}):
                horas.append(hora_str)
            inicio += intervalo

        return horas

    def agendar_cita(self, nombre, cedula, correo, fecha, hora):
        cita = {
            "nombre": nombre,
            "cedula": cedula,
            "correo": correo,
            "fecha": fecha,
            "hora": hora,
            "creado_en": datetime.now()
        }
        self.citas.insert_one(cita)

    def obtener_citas(self):
        return list(self.citas.find({}, {"_id": 0}))

    def cancelar_cita(self, cedula):
        self.citas.delete_one({"cedula": cedula})

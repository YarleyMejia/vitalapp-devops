import os
from pymongo import MongoClient
from datetime import datetime, timedelta

class CitaService:
    def __init__(self):
        # Leer la URI desde la variable de entorno
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("La variable MONGO_URI no está definida en el entorno.")
        
        # Conexión con MongoDB Atlas
        self.client = MongoClient(mongo_uri)
        self.db = self.client["salud_vital"]
        self.citas = self.db["citas"]

    def obtener_horas_disponibles(self, fecha):
        """Genera las horas disponibles cada 30 minutos de 8 AM a 5 PM"""
        inicio = datetime.strptime(f"{fecha} 08:00", "%Y-%m-%d %H:%M")
        fin = datetime.strptime(f"{fecha} 17:00", "%Y-%m-%d %H:%M")
        intervalo = timedelta(minutes=30)
        horas = []

        while inicio < fin:
            hora_str = inicio.strftime("%H:%M")
            existe = self.citas.find_one({"fecha": fecha, "hora": hora_str})
            if not existe:
                horas.append(hora_str)
            inicio += intervalo

        return horas

    def agendar_cita(self, nombre, cedula, correo, fecha, hora):
        """Registra una nueva cita en la base de datos"""
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
        """Devuelve todas las citas registradas (sin el _id)"""
        return list(self.citas.find({}, {"_id": 0}))

    def cancelar_cita(self, cedula):
        """Elimina una cita según la cédula"""
        self.citas.delete_one({"cedula": cedula})
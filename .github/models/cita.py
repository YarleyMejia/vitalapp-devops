from datetime import datetime

class Cita:
    def __init__(self, nombre, cedula, correo, fecha, hora):
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.fecha = fecha
        self.hora = hora
        self.creado_en = datetime.now()

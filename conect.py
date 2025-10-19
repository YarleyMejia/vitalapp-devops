from pymongo import MongoClient

# Reemplaza con tu cadena real de Atlas:
uri = "mongodb+srv://ycmejia:Familia.967@vital.joik75f.mongodb.net/?retryWrites=true&w=majority&appName=vital"

client = MongoClient(uri)

# Accede a la base de datos
db = client["saludvital"]

# Ejemplo: mostrar las colecciones existentes
print(db.list_collection_names())

# Insertar un ejemplo
db.usuarios.insert_one({"nombre": "Camilo", "rol": "Admin"})

print("Conexión exitosa y dato insertado")

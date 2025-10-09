from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# ===========================
# 🔗 Conexión con MongoDB
# ===========================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["vitalapp_db"]
citas_collection = db["citas"]

# ===========================
# 🏠 Página principal (formulario)
# ===========================
@app.route('/')
def index():
    # Consultar citas ya agendadas para mostrarlas
    citas = list(citas_collection.find({}, {'_id': 0}))
    return render_template('index.html', citas=citas)

# ===========================
# 🩺 Agendar nueva cita
# ===========================
@app.route('/agendar', methods=['POST'])
def agendar_cita():
    paciente = request.form.get('paciente')
    tipo_consulta = request.form.get('tipo_consulta')
    fecha_str = request.form.get('fecha_cita')

    if not paciente or not tipo_consulta or not fecha_str:
        return "⚠️ Faltan datos", 400

    # Convertir fecha string a tipo datetime
    fecha_cita = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

    # Insertar en la colección
    citas_collection.insert_one({
        "paciente": paciente,
        "tipo_consulta": tipo_consulta,
        "fecha_cita": fecha_cita
    })

    return redirect(url_for('index'))

# ===========================
# 📋 API para consultar citas (opcional)
# ===========================
@app.route('/api/citas', methods=['GET'])
def listar_citas():
    citas = list(citas_collection.find({}, {'_id': 0}))
    return {"citas": citas}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

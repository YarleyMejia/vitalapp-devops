from flask import Flask, render_template
from routes.cita_routes import cita_bp
from services.cita_service import CitaService
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "clave_super_secreta_123"

# Registrar Blueprint
app.register_blueprint(cita_bp, url_prefix="/cita")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/test-db")
def test_db():
    try:
        dbs = CitaService().client.list_database_names()
        return f"Conexión exitosa: {dbs}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
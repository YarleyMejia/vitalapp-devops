from flask import Flask, render_template
from routes.cita_routes import cita_bp
from services.cita_service import CitaService
from dotenv import load_dotenv
import os

# ✅ Cargar las variables del archivo .env
load_dotenv()
print("MONGO_URI cargado:", os.getenv("MONGO_URI"))  # 👈 línea temporal para probar

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

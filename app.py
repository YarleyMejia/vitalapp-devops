from flask import Flask, render_template
from routes.cita_routes import cita_bp
import os

app = Flask(__name__)

# ✅ Clave secreta para sesiones
app.secret_key = os.getenv("SECRET_KEY") or "clave_super_secreta_123"

# ✅ Registrar Blueprint de citas
app.register_blueprint(cita_bp, url_prefix="/cita")

@app.route("/")
def home():
    """Página principal"""
    return render_template("home.html")

# ✅ Endpoint opcional para probar conexión con MongoDB Atlas
@app.route("/test-db")
def test_db():
    try:
        from routes.cita_service import CitaService
        dbs = CitaService().client.list_database_names()
        return f"Conexión exitosa: {dbs}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

if __name__ == "__main__":
    # ✅ Render requiere host 0.0.0.0 y puerto 5000
    app.run(host="0.0.0.0", port=5000)
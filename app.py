# app.py
from flask import Flask, render_template
from routes.cita_routes import cita_bp
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_super_secreta_123")

# Registrar blueprints
app.register_blueprint(cita_bp, url_prefix="/cita")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

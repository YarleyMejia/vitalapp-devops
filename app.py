from flask import Flask, render_template
from routes.cita_routes import cita_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "clave_super_secreta_123"

# Registrar Blueprint de citas
app.register_blueprint(cita_bp, url_prefix="/citas")

@app.route("/")
def home():
    """Página principal"""
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

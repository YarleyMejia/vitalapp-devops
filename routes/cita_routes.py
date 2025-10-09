from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.cita_service import CitaService
from datetime import date

cita_bp = Blueprint("cita", __name__)
service = CitaService()

@cita_bp.route("/agendar", methods=["GET", "POST"])
def agendar():
    hoy = date.today().strftime("%Y-%m-%d")
    if request.method == "POST":
        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        correo = request.form["correo"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        service.agendar_cita(nombre, cedula, correo, fecha, hora)
        flash("✅ Cita agendada con éxito", "success")
        return redirect(url_for("cita.listar"))
    horas_disponibles = service.obtener_horas_disponibles(hoy)
    return render_template("agendar.html", horas=horas_disponibles, fecha=hoy)

@cita_bp.route("/listar")
def listar():
    citas = service.obtener_citas()
    return render_template("listar.html", citas=citas)

@cita_bp.route("/cancelar", methods=["GET", "POST"])
def cancelar():
    if request.method == "POST":
        cedula = request.form["cedula"]
        service.cancelar_cita(cedula)
        flash("❌ Cita cancelada correctamente", "info")
        return redirect(url_for("cita.listar"))
    return render_template("cancelar.html")
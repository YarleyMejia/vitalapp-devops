from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.cita_service import CitaService
from datetime import date

# Blueprint para las rutas de citas
cita_bp = Blueprint("cita", __name__)
service = CitaService()


@cita_bp.route("/agendar", methods=["GET", "POST"])
def agendar():
    hoy = date.today().strftime("%Y-%m-%d")

    if request.method == "POST":
        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        correo = request.form["correo"]
        especialidad = request.form["especialidad"]
        profesional = request.form["profesional"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        if fecha < hoy:
            flash("❌ No puedes agendar citas en fechas pasadas.", "danger")
            return redirect(url_for("cita.agendar"))

        service.agendar_cita(nombre, cedula, correo, especialidad, profesional, fecha, hora)
        flash("✅ Cita agendada con éxito", "success")
        return redirect(url_for("cita.listar"))

    return render_template(
        "agendar.html",
        especialidades=service.ESPECIALIDADES,
        fecha=hoy
    )


@cita_bp.route("/listar")
def listar():
    citas = service.obtener_citas()

    # Permitir búsqueda por cédula (opcional)
    cedula = request.args.get("cedula")
    if cedula:
        citas = [c for c in citas if c["cedula"] == cedula]

    return render_template("listar.html", citas=citas)


@cita_bp.route("/cancelar", methods=["GET", "POST"])
def cancelar():
    if request.method == "POST":
        cedula = request.form["cedula"]
        service.cancelar_cita(cedula)
        flash("❌ Cita cancelada correctamente", "info")
        return redirect(url_for("cita.listar"))
    return render_template("cancelar.html")


@cita_bp.route('/reprogramar/<cedula>', methods=['GET', 'POST'])
def reprogramar(cedula):
    cita = service.obtener_cita_por_cedula(cedula)  # Usamos el servicio, no SQLAlchemy

    if not cita:
        flash('No se encontró una cita con esa cédula.', 'danger')
        return redirect(url_for('cita.listar'))

    if request.method == 'POST':
        nueva_fecha = request.form['fecha']
        nueva_hora = request.form['hora']
        nuevo_profesional = request.form['profesional']
        nueva_especialidad = request.form['especialidad']

        service.reprogramar_cita(
            cedula,
            nueva_fecha,
            nueva_hora,
            nuevo_profesional,
            nueva_especialidad
        )

        flash('✅ Cita reprogramada exitosamente.', 'success')
        return redirect(url_for('cita.listar'))

    # Estructura que espera tu template reprogramar.html
    especialidades = {
        "Medicina General": ["Carlos Mejia Lopez", "Alejandra Molina Puerta"],
        "Psicologia": ["Alejandro Gomez Bedoya"],
        "Planificacion Familiar": ["Luisa Maria Paez"],
        "Odontologia": ["Jorge Eduardo Arango"]
    }

    return render_template(
        'reprogramar.html',
        cita=cita,
        especialidades=especialidades  # se envía como dict para JS
    )


@cita_bp.route("/horas_disponibles")
def horas_disponibles():
    fecha = request.args.get("fecha")
    profesional = request.args.get("profesional")
    horas = service.obtener_horas_disponibles(fecha, profesional)
    return jsonify({"horas": horas})

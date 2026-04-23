from flask import send_from_directory
from flask import Flask, render_template, request, send_file, abort
from flask import redirect, url_for, flash

from datetime import datetime
import tempfile
import os
import re

from lotwlo.normalizer import normalize_adif

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
app.secret_key = "supersecretkey"

def cleanup_tmp():
    for f in os.listdir("/tmp"):
        path = os.path.join("/tmp", f)
        if os.path.isfile(path) and f.startswith("normalized_"):
            try:
                os.remove(path)
                print("🧹 Eliminado:", path)
            except Exception as e:
                print("Error borrando:", path, e)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    operator = request.form.get("operator", "").strip().upper().replace(" ", "")

    if not operator:
        abort(400, "Indicativo obligatorio")

    if not re.fullmatch(r"[A-Z0-9/]+", operator):
        abort(400, "Indicativo inválido")

    file = request.files.get("adif")
    if not file:
        abort(400, "Archivo no enviado")

    if not file.filename.lower().endswith((".adi", ".adif")):
        abort(400, "Formato inválido")

    cleanup_tmp()  # LIMPIA ANTES DE PROCESAR

    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, "input.adi")
        output_path = os.path.join(tmp, "output.oneline.adi")

        file.save(input_path)

        count = normalize_adif(input_path, output_path, operator)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"{operator}-{timestamp}.normalized.adi"

        final_path = os.path.join("/tmp", output_filename)
        original_filename = file.filename

        import shutil
        shutil.move(output_path, final_path)

        print("Guardado:", final_path)

        return redirect(url_for(
            "index",
            file=output_filename,
            qsos=count,
            original=original_filename
        ))

@app.route("/download/<filename>")
def download(filename):
    path = os.path.join("/tmp", filename)

    if not os.path.exists(path):
        abort(404, "Archivo no encontrado")

    return send_from_directory("/tmp", filename, as_attachment=True)
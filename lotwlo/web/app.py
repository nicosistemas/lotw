from flask import Flask, render_template, request, send_file, abort
import tempfile
import os
import re

from lotwlo.normalizer import normalize_adif

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    operator = request.form.get("operator", "").strip().upper()

    if not operator:
        abort(400, "Indicativo obligatorio")

    if not re.fullmatch(r"[A-Z0-9/]+", operator):
        abort(400, "Indicativo inválido")

    file = request.files.get("adif")
    if not file:
        abort(400, "Archivo no enviado")

    if not file.filename.lower().endswith((".adi", ".adif")):
        abort(400, "Formato de archivo inválido")

    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, "input.adi")
        output_path = os.path.join(tmp, "output.adi")

        file.save(input_path)
        normalize_adif(input_path, output_path, operator)

        return send_file(
            output_path,
            as_attachment=True,
            download_name=f"lotw_{operator}.adi",
            mimetype="text/plain",
        )
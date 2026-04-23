import re
import os

ORDER = [
    "call",
    "qso_date",
    "time_on",
    "band",
    "freq",
    "mode",
    "rst_sent",
    "rst_rcvd",
    "gridsquare",
    "country",
    "name",
    "qth",
    "distance",
]
def normalize_adif(input_path, output_path, operator):
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()

    parts = re.split(r"(?i)<eoh>", data, maxsplit=1)
    if len(parts) > 1:
        data = parts[1]

    data = data.replace("\n", " ").replace("\r", " ")

    records = re.split(r"(?i)<eor>", data)

    clean_records = []

    for rec in records:
        rec = rec.strip()
        if not rec:
            continue

        fields = re.findall(r"<([^:>]+):(\d+)>([^<]*)", rec, re.IGNORECASE)

        d = {}
        for k, l, v in fields:
            k = k.lower()
            v = v.strip()

            if k.startswith("my_") or k.startswith("qrzcom_") or k.startswith("app_"):
                continue

            if k == "my_iota":
                continue

            if k not in d:
                d[k] = v

        # validar mínimos
        if not all(k in d for k in ["call", "qso_date", "time_on"]):
            continue

        if d.get("qso_date") == "00000000":
            continue

        # normalizar hora
        d["time_on"] = d["time_on"][:4]

        # construir salida
        out = []

        for k in ORDER:
            if k in d and d[k]:
                v = d[k]
                out.append(f"<{k}:{len(v)}>{v}")

        out.append(f"<station_callsign:{len(operator)}>{operator}")
        out.append(f"<operator:{len(operator)}>{operator}")

        clean_records.append(" ".join(out) + " <eor>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<ADIF_VER:5>3.1.1 <eoh>\n")
        for r in clean_records:
            f.write(r + "\n")

    return len(clean_records)
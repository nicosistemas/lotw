import re

def normalize_adif(input_file, output_file, operator):
    operator = operator.upper()
    op_len = len(operator)

    eor_re = re.compile(r"<eor>", re.IGNORECASE)
    drop_qsl_re = re.compile(
        r"<(lotw|eqsl)_qsl[rs]date:8>00000000",
        re.IGNORECASE
    )

    with open(input_file, "r", encoding="utf-8", errors="ignore") as fin, \
         open(output_file, "w", encoding="utf-8") as fout:

        current_qso = []

        for line in fin:
            line = line.strip()

            # líneas vacías
            if not line:
                continue

            # <MY_IOTA>
            if re.search(r"<my_iota:", line, re.IGNORECASE):
                continue

            # fechas LoTW / eQSL inválidas
            if drop_qsl_re.search(line):
                continue

            # fin de QSO
            if eor_re.search(line):
                line = eor_re.sub(
                    f"<operator:{op_len}>{operator} <eor>",
                    line
                )
                current_qso.append(line)
                fout.write(" ".join(current_qso) + "\n")
                current_qso = []
            else:
                current_qso.append(line)
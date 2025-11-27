for f in *.adi
do
  LC_ALL=C awk '
    BEGIN { ORS="" ; IGNORECASE=1 }

    # borrar my_iota
    /<my_iota:/ { next }

    # borrar lineas vacias
    /^[[:space:]]*$/ { next }

    # borrar fechas 00000000 de LoTW y eQSL
    /<(lotw|eqsl)_qsl[rs]date:8>00000000/ { next }

    {
      # insertar OPERATOR antes de <eor>
      if (index(tolower($0), "<eor>")) {
        sub(/<eor>/, "<operator:6>LU2FTI <eor>")
      }

      # imprimir registro en una sola linea
      printf "%s ", $0

      # corte final de registro
      if (index(tolower($0), "<eor>")) {
        printf "\n"
      }
    }
  ' "$f" > "${f%.adi}.normalized.adi"
done

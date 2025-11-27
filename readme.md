# Normalizador ADIF QRZ to LOTW by LU2FTI

Este script procesa archivos ADIF (`.adi`) para dejarlos en un formato compatible con Logbook of The World (LoTW).

## Qué hace

-   Convierte cada QSO en una sola línea
-   Elimina `<my_iota>`
-   Elimina líneas vacías
-   Borra fechas inválidas 00000000 de LoTW y eQSL
-   Agrega automáticamente `<operator:6>LU2FTI` antes de `<eor>`
-   Genera archivos nuevos `.oneline.adi` sin modificar los originales

## Script

``` bash
for f in *.adi
do
  LC_ALL=C awk '
    BEGIN { ORS="" ; IGNORECASE=1 }

    /<my_iota:/ { next }
    /^[[:space:]]*$/ { next }
    /<(lotw|eqsl)_qsl[rs]date:8>00000000/ { next }

    {
      if (index(tolower($0), "<eor>")) {
        sub(/<eor>/, "<operator:6>LU2FTI <eor>")
      }

      printf "%s ", $0

      if (index(tolower($0), "<eor>")) {
        printf "\n"
      }
    }
  ' "$f" > "${f%.adi}.normalized.adi"
done
```

## Uso

``` bash
chmod +x qrz-to-lotw.sh
./qrz-to-lotw.sh
```

## Salida

`archivo.adi` → `archivo.normalized.adi`

## Notas

-   No reemplaza archivos originales
-   Cambiar LU2FTI si usás otro indicativo
-   Listo para subir a tqsl / LoTW

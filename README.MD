# Normalizadif v3

## Run with Docker

### Build image

```bash
docker build -t normaliadif .
```

### Run container

```bash
docker run -p 5010:5010 normaliadif
```

### Open in browser

```text
http://localhost:5010
```

---

## Run with Docker Compose

```bash
docker compose up --build -d
```

### Open in browser

```text
http://localhost:5010
```
## Features

* Normaliza archivos ADIF exportados desde QRZ para uso en LoTW
* Convierte cada QSO a formato de una sola línea
* Elimina campos innecesarios como `<my_iota>`
* Filtra líneas vacías automáticamente
* Elimina fechas inválidas (`00000000`) de LoTW y eQSL
* Inserta automáticamente el campo `<operator>` con tu indicativo
* No modifica el archivo original
* Genera un nuevo archivo `.normalized.adi` listo para subir
* Interfaz web simple para subir, procesar y descargar
* Muestra cantidad de QSOs procesados
* Naming automático con indicativo + fecha + hora
* Limpieza automática de archivos temporales (`/tmp`)
* Ejecución en Docker
# 🛰️ IP Lookup Tool

Herramienta en Python para consultar información geográfica y técnica de direcciones IP. Permite cargar listas de IP desde archivos `.csv`, `.txt` o `.xlsx` y exportar los resultados a Excel o KML para su visualización en mapas.

---

## 🚀 Características

- CLI moderna basada en [`Typer`](https://typer.tiangolo.com/) con soporte para `--help`.
- Consulta de IPs utilizando **ip-api.com** y **fallback automático a ipinfo.io** en caso de error o límite de uso.
- Soporte para entrada desde `.csv`, `.txt` o `.xlsx`.
- Exportación de resultados a `.xlsx`.
- Generación opcional de archivo `.kml` para uso en Google Earth o herramientas GIS.
- Validación de IPs duplicadas o mal formateadas.
- Modo detallado (`--verbose`) para seguimiento por consola.
- Testeado con `pytest`.

---

## 🗂️ Estructura del Proyecto

```bash
.
├── data/                     # Archivos de entrada y salida
│   ├── input.csv
│   └── output.xlsx
├── src/
│   ├── __init__.py
│   ├── ip_lookup.py          # Lógica principal del script
│   └── utils.py              # Funciones auxiliares
├── tests/
│   └── test_ip_lookup.py     # Tests unitarios
├── setup.py                  # Instalación como CLI global
├── requirements.txt
└── README.md
```

---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MikelUrr/IP-lookup-tool.git
cd IP-lookup-tool
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Instalar como comando global

Ubicado en el directorio raíz se encuentra `setup.py`. Para instalar el CLI globalmente:

```bash
pip install .
```

Esto habilita el comando:

```bash
ip-lookup input.csv output.xlsx --kml output.kml --verbose
```

---

## 🛠️ Uso desde CLI

```bash
python src/ip_lookup.py input.csv output.xlsx [--kml output.kml] [--verbose]
```

O si lo instalaste como paquete CLI:

```bash
ip-lookup input.csv output.xlsx --kml output.kml --verbose
```

---

## 📋 Ejemplos de uso

### ✅ Leer IPs desde CSV

```bash
ip-lookup data/input.csv data/output.xlsx
```

### 📄 Leer IPs desde TXT

```bash
ip-lookup data/input.txt data/output.xlsx
```

### 📊 Leer IPs desde Excel

```bash
ip-lookup data/input.xlsx data/output.xlsx
```

### 🌍 Generar archivo KML para visualizar en mapas

```bash
ip-lookup data/input.csv data/output.xlsx --kml data/output.kml
```

### 🔍 Activar modo detallado

```bash
ip-lookup data/input.csv data/output.xlsx --verbose
```

---

## 🧪 Ejecutar pruebas

```bash
pytest tests/
```

---

## 📤 Formato de salida

El archivo Excel incluirá las siguientes columnas:

- `IP`
- `País`
- `Región`
- `Ciudad`
- `ISP`
- `Org`
- `Lat`
- `Lon`
- `Error` (si aplica)

---


---

## 🌐 APIs Utilizadas

Este proyecto utiliza dos servicios web para obtener información sobre direcciones IP:

- [ip-api.com](http://ip-api.com/docs)  
  Servicio gratuito sin clave para consultar información de geolocalización y red.  
  Límite: 45 peticiones por minuto desde la misma IP.

- [ipinfo.io](https://ipinfo.io/developers)  
  Utilizado como alternativa en caso de fallo o límite con ip-api.  
  Proporciona ubicación, ISP y más datos sobre la IP consultada.

## 📝 Licencia

MIT License

---

## ✉️ Contacto

Desarrollado por **Mikel U.**  
Este proyecto es funcional y educativo. Se aceptan contribuciones vía pull request.
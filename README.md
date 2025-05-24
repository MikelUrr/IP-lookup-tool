# 🛰️ IP Lookup Tool

Herramienta en Python que permite obtener información geográfica y técnica sobre direcciones IP, a partir de un archivo `.csv`, `.txt` o `.xlsx`.

## 🚀 Características

- Consulta a IP-API (gratuito, sin clave API).
- Soporte para archivos de entrada `.csv`, `.txt`, `.xlsx`.
- Exporta resultados a Excel.
- Pensado para ser fácilmente extensible.

## 🗂️ Estructura del Proyecto

Ver estructura de carpetas en el código fuente.

## 📦 Instalación

```bash
git clone https://github.com/MikelUrr/IP-lookup-tool.git
cd IP-lookup-tool
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
# 🛰️ IP Lookup Tool

Herramienta en Python que permite obtener información geográfica y técnica sobre direcciones IP, a partir de un archivo `.csv`, `.txt` o `.xlsx`.

---

## 🚀 Características

- Consulta gratuita a la API de [ip-api.com](http://ip-api.com).
- Soporte para archivos de entrada `.csv`, `.txt`, `.xlsx`.
- Exporta los resultados a un archivo Excel con múltiples columnas.
- Pensado para ser fácilmente extensible y mantenible.

---

## 📂 Estructura del Proyecto

```bash
ip_lookup_tool/
│
├── data/
│   ├── input.csv              # Archivo de entrada (IPs)
│   └── output.xlsx            # Archivo de salida con los resultados
│
├── src/
│   ├── __init__.py
│   ├── ip_lookup.py           # Lógica principal del script
│   └── utils.py               # Funciones auxiliares
│
├── tests/
│   └── test_ip_lookup.py      # Pruebas automáticas
│
├── requirements.txt           # Dependencias
├── README.md                  # Este archivo
└── .gitignore
```

---

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/MikelUrr/IP-lookup-tool.git
cd IP-lookup-tool
```

2. Crea un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Uso

```bash
python -m src.ip_lookup data/input.csv data/output.xlsx
```

---

## 📋 Ejemplos de uso

### 🧾 1. Leer archivo CSV

```bash
python -m src.ip_lookup data/input.csv data/output.xlsx
```

> El archivo `input.csv` debe contener una IP por línea o una columna con IPs.

---

### 📄 2. Leer archivo TXT (una IP por línea)

Puedes usar el mismo comando si el archivo `.txt` tiene el mismo formato que un `.csv` (una IP por línea).

```bash
python -m src.ip_lookup data/ips.txt data/output.xlsx
```

---

### 📊 3. Leer archivo Excel (`.xlsx`)

Modifica la función de lectura para admitir Excel (ya soportado si adaptas `pandas.read_excel()`).

```bash
python -m src.ip_lookup data/input_ips.xlsx data/output.xlsx
```

---

### 🧪 4. Ejecutar pruebas

```bash
pytest tests/
```

---

## 🧾 Formato del resultado

El archivo Excel generado tendrá columnas como:

- IP
- País
- Región
- Ciudad
- ISP
- Org
- Lat
- Lon
- Error (si aplica)

---

## 📝 Licencia

MIT License

---

## 📬 Contacto

Creado por **Mikel U.**  
Proyecto educativo y funcional. Se aceptan mejoras vía PR.
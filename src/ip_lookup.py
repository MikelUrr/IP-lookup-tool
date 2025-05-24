import pandas as pd
import requests
import os
import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from xml.etree.ElementTree import Element, SubElement, ElementTree
from src.utils import clean_ip
import typer

app = typer.Typer()
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def resolve_input_path(path_str: str) -> str:
    data_path = os.path.join("data", path_str)
    return data_path if os.path.exists(data_path) else path_str

def resolve_output_path(path_str: str) -> str:
    if os.path.isdir("data"):
        return os.path.join("data", os.path.basename(path_str))
    return path_str

def is_valid_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split("."))

def generate_kml(results, output_path):
    kml = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = SubElement(kml, "Document")

    for entry in results:
        if entry.get("Lat") is not None and entry.get("Lon") is not None:
            placemark = SubElement(doc, "Placemark")
            SubElement(placemark, "name").text = entry.get("IP")
            SubElement(placemark, "description").text = f"{entry.get('Ciudad')}, {entry.get('País')} - {entry.get('ISP')}"
            point = SubElement(placemark, "Point")
            SubElement(point, "coordinates").text = f"{entry['Lon']},{entry['Lat']},0"

    tree = ElementTree(kml)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "IP": ip,
                    "País": data.get("country"),
                    "Región": data.get("regionName"),
                    "Ciudad": data.get("city"),
                    "ISP": data.get("isp"),
                    "Org": data.get("org"),
                    "Lat": data.get("lat"),
                    "Lon": data.get("lon"),
                }

        logger.warning(f"Fallo con ip-api para {ip}, probando con ipinfo...")
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            loc = data.get("loc", "0,0").split(",")
            return {
                "IP": ip,
                "País": data.get("country"),
                "Región": data.get("region", ""),
                "Ciudad": data.get("city", ""),
                "ISP": data.get("org", ""),
                "Org": data.get("org", ""),
                "Lat": float(loc[0]),
                "Lon": float(loc[1]),
            }
        return {"IP": ip, "Error": "No se pudo obtener información de ningún proveedor."}
    except Exception as e:
        return {"IP": ip, "Error": str(e)}

def read_ips(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(filepath, header=None)
    elif ext == ".xlsx":
        df = pd.read_excel(filepath, header=None)
    elif ext == ".txt":
        df = pd.read_csv(filepath, header=None, delimiter="\n", engine="python")
    else:
        raise ValueError(f"Extensión de archivo no soportada: {ext}")
    return df[0].dropna().apply(clean_ip).tolist()

@app.command()
def main(
    input: str = typer.Argument(..., help="Ruta al archivo de entrada (.csv, .txt, .xlsx)"),
    output: str = typer.Argument(..., help="Ruta al archivo de salida .xlsx"),
    kml: Optional[str] = typer.Option(None, help="Ruta opcional para generar archivo KML"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Activar modo detallado")
):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled.")

    resolved_input = resolve_input_path(input)
    if not os.path.exists(resolved_input):
        typer.echo(f"❌ Archivo de entrada no encontrado: {resolved_input}")
        raise typer.Exit(code=1)

    logger.info(f"🔍 Leyendo IPs desde {resolved_input}...")
    ips = read_ips(resolved_input)
    logger.info(f"📡 Consultando API para {len(ips)} IPs...")

    results = []
    seen_ips = set()
    valid_ips = []
    for ip in ips:
        if not ip:
            continue
        if ip in seen_ips:
            logger.warning(f"IP duplicada ignorada: {ip}")
            results.append({"IP": ip, "Error": "Duplicated IP"})
            continue
        if not is_valid_ip(ip):
            logger.error(f"IP inválida: {ip}")
            results.append({"IP": ip, "Error": "Invalid IP format"})
            continue
        seen_ips.add(ip)
        valid_ips.append(ip)

    BATCH_SIZE = 45
    for i in range(0, len(valid_ips), BATCH_SIZE):
        batch = valid_ips[i:i + BATCH_SIZE]
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ip = {executor.submit(get_ip_info, ip): ip for ip in batch}
            for future in as_completed(future_to_ip):
                result = future.result()
                results.append(result)
        if i + BATCH_SIZE < len(valid_ips):
            logger.info("⏳ Esperando 60 segundos para cumplir el límite de la API...")
            time.sleep(60)

    resolved_output = resolve_output_path(output)
    df_result = pd.DataFrame(results)
    df_result.to_excel(resolved_output, index=False)
    logger.info(f"✅ Archivo generado: {resolved_output}")

    if kml:
        resolved_kml = resolve_output_path(kml)
        generate_kml(results, resolved_kml)
        logger.info(f"📍 Archivo KML generado: {resolved_kml}")

def main_entry():
    app()
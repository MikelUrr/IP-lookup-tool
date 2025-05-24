import pandas as pd
import requests
import argparse
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils import clean_ip
from xml.etree.ElementTree import Element, SubElement, ElementTree

API_URL = "http://ip-api.com/json/{}"

def is_valid_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split('.'))

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
        # Primero intentamos ip-api
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

        # Si ip-api falla o excede el límite, probamos con ipinfo
        print(f"🔁 Fallo con ip-api para {ip}, probando con ipinfo...")
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

def process_ips(input_file, output_file, kml_file=None):
    if not os.path.exists(input_file):
        print(f"❌ Archivo de entrada no encontrado: {input_file}")
        return

    print(f"🔍 Leyendo IPs desde {input_file}...")
    ips = read_ips(input_file)
    print(f"📡 Consultando API para {len(ips)} IPs...")

    results = []
    seen_ips = set()
    valid_ips = []
    for ip in ips:
        if not ip:
            continue
        if ip in seen_ips:
            print(f"⚠️  IP duplicada ignorada: {ip}")
            results.append({"IP": ip, "Error": "Duplicated IP"})
            continue
        if not is_valid_ip(ip):
            print(f"❌ IP inválida: {ip}")
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
            print("⏳ Esperando 60 segundos para cumplir el límite de la API...")
            time.sleep(60)

    df_result = pd.DataFrame(results)
    df_result.to_excel(output_file, index=False)
    print(f"✅ Archivo generado: {output_file}")

    if kml_file:
        generate_kml(results, kml_file)
        print(f"📍 Archivo KML generado: {kml_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta información de direcciones IP desde un archivo.")
    parser.add_argument("input", help="Ruta al archivo de entrada (.csv, .txt, .xlsx)")
    parser.add_argument("output", help="Ruta al archivo de salida .xlsx")
    parser.add_argument("--kml", help="Ruta opcional para generar archivo KML")
    args = parser.parse_args()

    process_ips(args.input, args.output, args.kml)
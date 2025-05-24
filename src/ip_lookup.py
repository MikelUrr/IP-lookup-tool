import pandas as pd
import requests
import argparse
import os
import re
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
        response = requests.get(API_URL.format(ip), timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
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
        return {"IP": ip, "Error": data.get("message", "No se pudo obtener info")}
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
        results.append(get_ip_info(ip))

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
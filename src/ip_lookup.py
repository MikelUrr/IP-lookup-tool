import pandas as pd
import requests
import argparse
import os
from src.utils import clean_ip

API_URL = "http://ip-api.com/json/{}"

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

def process_ips(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ Archivo de entrada no encontrado: {input_file}")
        return

    print(f"🔍 Leyendo IPs desde {input_file}...")
    ips = read_ips(input_file)
    print(f"📡 Consultando API para {len(ips)} IPs...")

    results = [get_ip_info(ip) for ip in ips if ip]
    df_result = pd.DataFrame(results)

    df_result.to_excel(output_file, index=False)
    print(f"✅ Archivo generado: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta información de direcciones IP desde un archivo.")
    parser.add_argument("input", help="Ruta al archivo de entrada (.csv, .txt, .xlsx)")
    parser.add_argument("output", help="Ruta al archivo de salida .xlsx")
    args = parser.parse_args()

    process_ips(args.input, args.output)

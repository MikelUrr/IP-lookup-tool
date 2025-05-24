import pandas as pd
import requests
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

def process_ips(filepath, output_path):
    ips = pd.read_csv(filepath, header=None)[0].apply(clean_ip)
    results = [get_ip_info(ip) for ip in ips if ip]
    df_result = pd.DataFrame(results)
    df_result.to_excel(output_path, index=False)

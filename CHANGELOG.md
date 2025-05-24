# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-05-24

### Added

- Initial version of IP Lookup Tool.
  - Soporte de entrada desde archivos `.csv`, `.txt` y `.xlsx`.
  - Salida en formato Excel con geolocalización IP.
  - Lectura de IPs desde archivos ubicados en `data/` o raíz.

- CLI profesional usando [Typer](https://typer.tiangolo.com/).
  - Reemplazo completo de `argparse`.
  - Soporte para `--kml` y `--verbose`.

- Logging integrado (activado con `--verbose`).

- Instalación del CLI como comando global `ip-lookup` vía `setup.py`.

- Soporte para múltiples proveedores:
  - Se usa `ip-api.com` por defecto.
  - Fallback automático a `ipinfo.io` en caso de error o límite de uso.

- Paralelización de consultas IP:
  - Uso de `ThreadPoolExecutor`.
  - Lotes de 45 IPs con espera de 60 segundos.

- Validación de IPs:
  - Ignora IPs duplicadas.
  - Detecta IPs inválidas.

- Exportación opcional de resultados a `.kml` para visualización en mapas.

- Sistema de rutas inteligente:
  - Preferencia por guardar/leer desde `data/` si existe.

- Tests automatizados:
  - Pruebas unitarias con `pytest`.
  - Mock de peticiones para validar fallback a `ipinfo.io`.

- Documentación completamente actualizada:
  - Uso detallado del CLI.
  - Ejemplos prácticos.
  - Instrucciones para instalación como paquete.
  - Referencias a las APIs utilizadas.

---

## [Unreleased]

- Mejora del manejo de errores HTTP y desconexiones.
- Soporte para visualización HTML (por ejemplo con `folium`).
- Panel web (Streamlit o similar).

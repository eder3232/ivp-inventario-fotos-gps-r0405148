import json
import math
from pyproj import Transformer

from config import CONFIG
from pathlib import Path

images_metadata_json = Path(CONFIG["METADATA"])
metadata_with_utm = Path(CONFIG["METADATA_WITH_UTM"])


def latlon_to_utm(lat, lon):
    """
    Convierte una coordenada (lat, lon) a UTM.
    Calcula el número de zona y la letra de la zona según la latitud.
    Para la transformación se utiliza pyproj.
    """
    # Cálculo del número de zona UTM
    zone_number = int((lon + 180) / 6) + 1

    # Cálculo de la letra de zona UTM usando la fórmula:
    # Las letras van de C a X (omitiendo I y O), para latitudes entre -80 y 84.
    letters = "CDEFGHJKLMNPQRSTUVWX"
    zone_letter = letters[int((lat + 80) // 8)]

    # Determinamos el código EPSG según el hemisferio
    # En el hemisferio norte se usa EPSG:326XX y en el sur EPSG:327XX, donde XX es el número de zona con dos dígitos.
    epsg_code = f"326{zone_number:02d}" if lat >= 0 else f"327{zone_number:02d}"

    # Creamos el transformador de pyproj de EPSG:4326 (lat,lon) a la proyección UTM correspondiente.
    transformer = Transformer.from_crs("epsg:4326", f"epsg:{epsg_code}", always_xy=True)
    utm_x, utm_y = transformer.transform(lon, lat)

    return utm_x, utm_y, f"{zone_number}{zone_letter}"


def procesar_json(archivo_entrada, archivo_salida):
    # Leemos el JSON de entrada
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Recorremos cada registro y agregamos la conversión a UTM
    for registro in data:
        lat = registro["gps"]["latitude"]
        lon = registro["gps"]["longitude"]
        utm_x, utm_y, zona = latlon_to_utm(lat, lon)
        registro["utm"] = {"x": utm_x, "y": utm_y, "zone": zona}

    # Escribimos el nuevo JSON con los datos agregados
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Define el nombre de tu archivo de entrada y de salida
    archivo_entrada = images_metadata_json  # Cambia este nombre según corresponda
    archivo_salida = metadata_with_utm  # Archivo generado con las coordenadas UTM
    procesar_json(archivo_entrada, archivo_salida)
    print(f"Archivo generado: {archivo_salida}")

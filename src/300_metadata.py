import os
import json
import exifread

from config import CONFIG
from pathlib import Path

images_processed_dir = Path(CONFIG["IMAGES_PROCESSED_DIR"])
images_metadata_json = Path(CONFIG["METADATA"])


def convert_to_degrees(value):
    """
    Convierte una lista de valores (grados, minutos, segundos) en grados decimales.
    """
    d = float(value[0].num) / float(value[0].den)
    m = float(value[1].num) / float(value[1].den)
    s = float(value[2].num) / float(value[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def extract_gps_data(file_path):
    """
    Extrae la información GPS de una imagen.
    Retorna un diccionario con 'latitude' y 'longitude' si están disponibles.
    """
    gps_data = {}
    try:
        with open(file_path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        if (
            "GPS GPSLatitude" in tags
            and "GPS GPSLongitude" in tags
            and "GPS GPSLatitudeRef" in tags
            and "GPS GPSLongitudeRef" in tags
        ):

            lat = tags["GPS GPSLatitude"].values
            lat_ref = tags["GPS GPSLatitudeRef"].printable
            lon = tags["GPS GPSLongitude"].values
            lon_ref = tags["GPS GPSLongitudeRef"].printable

            lat_dd = convert_to_degrees(lat)
            lon_dd = convert_to_degrees(lon)

            # Ajuste según la referencia (N/S, E/W)
            if lat_ref.upper() != "N":
                lat_dd = -lat_dd
            if lon_ref.upper() != "E":
                lon_dd = -lon_dd

            gps_data["latitude"] = lat_dd
            gps_data["longitude"] = lon_dd
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
    return gps_data


def process_images(folder_path, output_file):
    """
    Procesa todas las imágenes de una carpeta, extrayendo sus datos GPS.
    Los resultados se guardan en un archivo JSON.
    """
    results = []
    # Filtrar imágenes según su extensión
    valid_extensions = (".jpg", ".jpeg", ".png")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(folder_path, filename)
            gps = extract_gps_data(file_path)
            if gps:
                results.append({"file": filename, "gps": gps})
            else:
                print(f"No se encontraron datos GPS en: {filename}")

    # Guardar los resultados en un archivo JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Datos extraídos y guardados en {output_file}")


if __name__ == "__main__":
    folder = images_processed_dir
    output = images_metadata_json
    process_images(folder, output)

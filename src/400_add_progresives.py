import pandas as pd
import geopandas as gpd
from config import CONFIG
from pathlib import Path

kml_path = Path(CONFIG["KML"])
processed_data_pickle_path = Path(CONFIG["PROCESSED_DATA_PICKLE_PATH"])
processed_with_coordinates_pickle_path = Path(
    CONFIG["PROCESSED_WITH_COORDINATES_PICKLE_PATH"]
)

EPSG_CURRENT = "32718"

gdf = gpd.read_file(kml_path, driver="KML")
carretera_utm = gdf.to_crs("EPSG:32719")

linea_utm = carretera_utm.geometry.iloc[0]
print("linea_utm")
print(linea_utm)

df = pd.read_pickle(processed_data_pickle_path)
print("df")
print(df.head())

df_gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["x"], df["y"]), crs="EPSG:32719"
)

# 4) Calcular la progresiva usando project()
#    project() da la distancia (en metros) a lo largo de la línea desde su inicio hasta el
#    punto proyectado más cercano.

df_gdf["progresiva_m"] = df_gdf.geometry.apply(lambda point: linea_utm.project(point))

df_gdf.to_pickle(processed_with_coordinates_pickle_path)

print(f"Archivo guardado con la progresiva en {processed_with_coordinates_pickle_path}")

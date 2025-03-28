import pandas as pd
from config import CONFIG
from pathlib import Path


processed_with_coordinates_pickle_path = Path(
    CONFIG["PROCESSED_WITH_COORDINATES_PICKLE_PATH"]
)
processed_fixed_with_coordinates_pickle_path = Path(
    CONFIG["PROCESSED_FIXED_WITH_COORDINATES_PICKLE_PATH"]
)

df = pd.read_pickle(processed_with_coordinates_pickle_path)

# Tomamos el valor de 'progresiva_m' donde la descripción es "inicio"
valor_inicio = df.loc[df["descripcion"] == "inicio", "progresiva_m"].iloc[0]

# Restamos ese valor a toda la columna
df["progresiva_m"] = df["progresiva_m"] - valor_inicio


print(df.tail())
# print(df[["id", "descripcion", "progresiva_m"]].tail())

df.to_pickle(processed_fixed_with_coordinates_pickle_path)

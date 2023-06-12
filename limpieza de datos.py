import pandas as pd
import numpy as np
import json
import re

movies = pd.read_csv('movies_dataset.csv', low_memory=False)
credits = pd.read_csv('credits.csv', low_memory=False)

# es una clase para extraer el valor name de las columnas que contienen listas o diccionarios
class desanidar:
    @staticmethod
    def convertir_a_str(valor):
        if isinstance(valor, (list, dict)):
            return json.dumps(valor)
        return str(valor)
    @staticmethod
    def extraer_nombres(valor):
        pattern = r"'name': '([^']*)'"
        coincidencias = re.findall(pattern, valor)
        if len(coincidencias) > 0:
            nombre = coincidencias[0]
            return nombre
        else:
            return None
        
movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(desanidar.convertir_a_str).apply(desanidar.extraer_nombres)
movies['genres'] = movies['genres'].apply(lambda x: ', '.join([row['name'] for row in json.loads(x.replace("'", "\""))]))
movies['genres'] = movies['genres'].fillna('')
movies['production_companies'] = movies['production_companies'].apply(desanidar.convertir_a_str).apply(desanidar.extraer_nombres)
movies['production_countries'] = movies['production_countries'].apply(desanidar.convertir_a_str).apply(desanidar.extraer_nombres)
movies['spoken_languages'] = movies['spoken_languages'].apply(desanidar.convertir_a_str).apply(desanidar.extraer_nombres)
credits['cast'] = credits['cast'].apply(desanidar.convertir_a_str).apply(desanidar.extraer_nombres)
credits['crew'] = credits['crew'].apply(desanidar.convertir_a_str).apply(desanidar.extraer_nombres)

# rellenar con 0 en valores nulos de los campos revenue y budget
movies[['budget', 'revenue']] = movies[['budget', 'revenue']].fillna(0)

# los valores de budget a numerico ya que es objeto
movies['budget'] = pd.to_numeric(movies['budget'], errors='coerce', downcast='integer')
movies['budget'] = movies['budget'].fillna(0)

# pasar a enteros
movies[['budget', 'revenue']] = movies[['budget', 'revenue']].astype(np.int64)

#cambiar el formato de las fechas
movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d', errors='coerce')

# eliminar campos nulos de release_date
movies['release_date'] = movies['release_date'].fillna(np.nan)
movies = movies.dropna(subset=['release_date'])

# crear nueva columna con el año de estreno
movies['release_year'] = movies['release_date'].dt.year

# una funcion anonima para crear la columna return
movies['return'] = movies.apply(lambda row: row['revenue'] / row['budget'] if pd.notnull(row['revenue']) and pd.notnull(row['budget']) and row['budget'] != 0 else 0, axis=1)

# eliminar columnas irrelevantes
eliminar_cols = movies[['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']]
movies = movies.drop(eliminar_cols, axis=1)

movies['id'] = movies['id'].astype(np.int64)
movies_credits_dataset = pd.merge(movies, credits, on='id')
movies_credits_dataset.to_csv('movies_credits_dataset.csv', index=False)

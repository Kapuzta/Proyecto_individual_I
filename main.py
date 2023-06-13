from fastapi import FastAPI
import pandas as pd
import numpy as np
import json 
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

app = FastAPI()

movies = pd.read_csv('movies_credits_dataset.csv', parse_dates=['release_date'], low_memory=False)
movies = movies.drop_duplicates()

#diccionario para que los meses sean en español
meses_dict = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

#diccionario para que los dias sean en español
dias_dict = {
    'lunes': 0,
    'martes': 1,
    'miércoles': 2,
    'jueves': 3,
    'viernes': 4,
    'sábado': 5,
    'domingo': 6
}

# funcion 1
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    mes_minus = mes.lower()
    if mes_minus in meses_dict:
        num_mes = meses_dict[mes_minus]
        peliculas_mes = movies[movies['release_date'].dt.month == num_mes]
        cantidad = len(peliculas_mes)
        return {'mes':mes, 'cantidad':cantidad}
    else:
        return {}
    
# funcion 2
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    dia_minus = dia.lower()
    if dia_minus in dias_dict:
        num_dia = dias_dict[dia_minus]
        peliculas_dia = movies[movies['release_date'].dt.dayofweek == num_dia]
        cantidad = len(peliculas_dia)
        return {'dia':dia, 'cantidad':cantidad}
    else:
        return {}
    
# funcion 3
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    titulo = titulo.lower()
    pelicula = movies[movies['title'].str.lower() == titulo]
    if len(pelicula) > 0:
        titulo_filmacion = pelicula['title'].iloc[0]
        fecha_estreno = int(pelicula['release_year'].iloc[0])
        score = round(pelicula['popularity'].iloc[0], 2)
        return {'titulo':titulo_filmacion, 'anio':fecha_estreno, 'popularidad':score}
    else:
        return {'mensaje': 'No se encontro ninguna pelicula con ese título'}
    
# funcion 4
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    pelicula = movies[movies['title'] == titulo]
    
    if len(pelicula) > 0:
        titulo_filmacion = pelicula['title'].iloc[0]
        anio_estreno = pelicula['release_year'].iloc[0]
        total_votos = (pelicula['vote_count']).iloc[0]
        promedio_votos = str(pelicula['vote_average'].iloc[0])
        
        if total_votos >= 2000:
            return {'titulo':titulo_filmacion,
                    'anio':f'{anio_estreno}',
                    'voto_total':total_votos,
                    'voto_promedio':f'{promedio_votos}'
                    }
        else:
            return {'La película no cumple con el requisito de tener al menos 2000 valoraciones.'}
    else:
        return {'La película no se encuentra.'}
    
# funcion 5
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor):
    nombre_actor = nombre_actor.lower()
    peliculas_actor = movies[(movies['cast'].str.lower() == nombre_actor) & (movies['crew'] != nombre_actor)]
    cantidad_peliculas = len(peliculas_actor)
    exito = round(peliculas_actor['return'].sum(),2)
    promedio_retorno = round((exito / cantidad_peliculas),2)
    
    return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_peliculas, 'retorno_total':exito, 'retorno_promedio':promedio_retorno}

# funcion 6
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director):
    nombre_director = nombre_director.lower()
    peliculas_director = movies[movies['crew'].str.lower() == nombre_director]
    exito_director = round((peliculas_director['return'].sum()), 2)
    
    peliculas = []
    
    for _, pelicula in peliculas_director.iterrows():
        titulo = pelicula['title']
        anio_lanzamiento = pelicula['release_year']
        retorno_individual = round((pelicula['return']), 2)
        costo = pelicula['budget']
        ganancia = pelicula['revenue']
        
        peliculas.append({
            'titulo': titulo,
            'fecha_lanzamiento': anio_lanzamiento,
            'retorno_individual': retorno_individual,
            'costo': costo,
            'ganancia': ganancia
        })
        
    return {'director':nombre_director, 'retorno_total_director':exito_director, 'peliculas':peliculas}

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    titulo_minus = titulo.lower()
    pelicula = movies[movies['title'].str.lower() == titulo_minus]
    movies['genres'] = movies['genres'].fillna('')

    genero_pelicula = pelicula['genres'].str.lower().str.split(',').explode().unique()
    
    filtered_movies = movies[movies['genres'].str.lower().str.split(',').apply(lambda x: any(genero in x for genero in genero_pelicula))]
    filtered_movies = filtered_movies.head(5000)
    filtered_movies['genre_match'] = filtered_movies['genres'].str.lower().str.split(',').apply(lambda x: sum(genero in x for genero in genero_pelicula))
    filtered_movies = filtered_movies.sort_values('genre_match', ascending=False)
    
    filtered_movies['title_similarity'] = filtered_movies['title'].apply(lambda x: fuzz.ratio(x.lower(), titulo_minus))
    filtered_movies = filtered_movies[filtered_movies['title_similarity'] >= 35]
    
    similarity_scores = cosine_similarity(filtered_movies[['popularity', 'vote_count']].fillna(0),
                                          filtered_movies[['popularity', 'vote_count']].fillna(0),
                                          dense_output=True)
    similar_indices = similarity_scores[-1].argsort()[::-1][1:6]
    
    similar_movies = filtered_movies.iloc[similar_indices]
    
    recommended_movies = similar_movies['title'].values.tolist()
    
    return {'lista recomendada': recommended_movies}


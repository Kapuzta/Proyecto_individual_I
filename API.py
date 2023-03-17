from fastapi import FastAPI
import pandas as pd
''' Crea el FastAPI '''
app = FastAPI()

'''Carga el dataset de películas'''
peliculas = pd.read_csv('plataform_titles.csv')

'''Consulta: Pelicula con mayor duracion'''
@app.get('/peliculas/max_duration')
async def get_max_duration(year: int = None, platform: str = None, duration_type: str = None):
    '''Filtra el dataset'''
    filtered_titles = peliculas.copy()
    if year:
        filtered_titles = filtered_titles[filtered_titles['release_year'] == year]
    if platform:
        filtered_titles = filtered_titles[filtered_titles['platform'] == platform]
    if duration_type:
        filtered_titles = filtered_titles[filtered_titles['duration_type'] == duration_type]

    '''película con mayor duracion'''
    max_duration = filtered_titles.loc[filtered_titles['duration_int'].idxmax()]

    '''Retorna los datos'''
    return {'La pelicula con mayor duracion': max_duration.to_dict()}

'''Consulta: Cantidad de películas por plataforma con puntaje mayor a XX en determinado año'''
@app.get('/peliculas/score_count')
async def get_score_count(platform: str, scored: float, year: int):
    '''Filtra por puntaje y año'''
    filtered_score = peliculas[(peliculas['platform'] == platform) & (peliculas['rating'] >= scored) & (peliculas['release_year'] == year)]

    '''cantidad de películas'''
    contador_peliculas = len(filtered_score)

    return {'La cantidad de películas para el score, año y plataforma es ': contador_peliculas}

'''Consulta: Cantidad de películas por plataforma con filtro de plataforma'''
@app.get('/peliculas/count_platform')
async def get_count_platform(platform: str):
    '''plataforma'''
    filtered_titles = peliculas[peliculas['platform'] == platform]

    '''cantidad de películas'''
    contador_peliculas = len(filtered_titles)

    return {'La cantidad de películas para esta plataforma es ': contador_peliculas}

'''Consulta: Actor que más se repite segun plataforma y año'''
@app.get('/peliculas/most_common_actor')
async def get_actor(platform: str, year: int):
    '''plataforma y año'''
    filtered_titles = peliculas[(peliculas['platform'] == platform) & (peliculas['release_year'] == year)]

    '''lista de actores de todas las peliculas filtradas'''
    lista_actores = [actors.split(', ') for actors in filtered_titles['cast']]
    sublista_actores = [actor for sublist in lista_actores for actor in sublist]

    '''actor mas comun en la lista'''
    actor_mas_comun = max(set(sublista_actores), key=sublista_actores.count)

    '''actor mas comun'''
    return {'El actor que más se repite segun plataforma y año es ': actor_mas_comun}

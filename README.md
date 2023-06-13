![head](https://github.com/Kapuzta/Proyecto_individual_I/blob/280f177649bb0050b6fde830ed5429593654a0a3/titulo.png)

# Sistema de recomendación de peliculas 
En este repositorio encontraremos el dataset [movies_credits_dataset.csv](https://github.com/Kapuzta/Proyecto_individual_I/blob/d6f058193841d2d50b6a575ed97ef24e00787af1/movies_credits_dataset.csv) con el que dare una recomendacion de 5 titulos de peliculas de acuerdo a un titulo ingresado por medio de una api alojada en render

## Puedes probar la API [aquí](https://movies-xvg8.onrender.com) con los siguientes endponits:
  - [/cantidad_filmaciones_mes/"mes"](https://movies-xvg8.onrender.com/cantidad_filmaciones_mes/) >>> Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente.
  - [/cantidad_filmaciones_dia/"dia"](https://movies-xvg8.onrender.com/cantidad_filmaciones_dia/) >>> Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente.
  - [/score_titulo/"titulo"](https://movies-xvg8.onrender.com/score_titulo/) >>> Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
  - [/votos_titulo/"titulo"](https://movies-xvg8.onrender.com/votos_titulo/) >>> Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones.
  - [/get_actor/"nombre actor"](https://movies-xvg8.onrender.com/get_actor/) >>> Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno.
  - [/get_director/"nombre director"](https://movies-xvg8.onrender.com/get_director/) >>> Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno.
  - [/recomendacion/"titulo"](https://movies-xvg8.onrender.com/recomendacion/) >>> Ingresas un nombre de pelicula y te recomienda las 5 similares en una lista

## Tambien puedes ver un video probando la aplicación y mostrando el codigo
  - video

## Documento de Pandas Profiling para EDA
  - #### [Reporte](https://drive.google.com/file/d/1YfNTYqnsvff3TOyV8SReJUnGUfDD6NnV/view?usp=drive_link)

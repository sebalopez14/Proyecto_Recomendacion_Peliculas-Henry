from fastapi import FastAPI, HTTPException
import pandas as pd
from src.carga_data import carga_data
from src.recomendacion import recomendar_peliculas

app = FastAPI(
    title="FastAPI",
    description="Endpoints API optimizados",
    version="1.0.0"
)

df_num, df_info, df_prod, df_cast = carga_data()

# Función para convertir el nombre del mes de español a número
def mes_numero(mes):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    return meses.get(mes.lower(), None)

# Función para convertir el nombre del día de español a número
def dia_numero(dia):
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2,
        "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6
    }
    return dias.get(dia.lower(), None)

# Endpoint: Cantidad de filmaciones en un mes específico
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    mes_numero_value = mes_numero(mes)  # Usando mes_numero en lugar de mes_a_numero
    if mes_numero_value is None:
        raise HTTPException(status_code=400, detail="Mes inválido")
    
    df_num['release_date'] = pd.to_datetime(df_num['release_date'], errors='coerce')
    peliculas_mes = df_num[df_num['release_date'].dt.month == mes_numero_value]
    cantidad = len(peliculas_mes)
    return {f"{cantidad} películas fueron estrenadas en el mes de {mes}"}

# Endpoint: Cantidad de filmaciones en un día específico
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dia_numero_value = dia_numero(dia)  # Usando dia_numero en lugar de dia_a_numero
    if dia_numero_value is None:
        raise HTTPException(status_code=400, detail="Día inválido")
    
    df_num['release_date'] = pd.to_datetime(df_num['release_date'], errors='coerce')
    peliculas_dia = df_num[df_num['release_date'].dt.weekday == dia_numero_value]
    cantidad = len(peliculas_dia)
    return {f"{cantidad} películas fueron estrenadas en los días {dia}"}

# Endpoint para obtener el score de una película por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    pelicula = df_info[df_info['title'].str.contains(titulo, case=False, na=False)]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    pelicula_info = pelicula.iloc[0]
    id_movie = pelicula_info['id']
    movie_details = df_num[df_num['id'] == id_movie].iloc[0]
    return (f"La película {pelicula_info['title']} fue estrenada en el año {movie_details['release_year']} con un score/popularidad de {movie_details['popularity']}")

# Endpoint para obtener la cantidad de votos y promedio de votos de una película por título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    pelicula = df_info[df_info['title'].str.contains(titulo, case=False, na=False)]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    pelicula_info = pelicula.iloc[0]
    id_movie = pelicula_info['id']
    movie_details = df_num[df_num['id'] == id_movie].iloc[0]
    if movie_details['vote_count'] < 2000:
        return {"mensaje": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    
    return (f"La película {pelicula_info['title']} fue estrenada en el año {movie_details['release_year']}. "
            f"La misma cuenta con un total de {movie_details['vote_count']} valoraciones, con un promedio de {movie_details['vote_average']}.")


# Endpoint para obtener información sobre un actor por nombre
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    actor_movies = df_cast[df_cast['cast_name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_movies.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    cantidad_peliculas = len(actor_movies)
    retorno_total = df_num[df_num['id'].isin(actor_movies['id'])]['return'].sum()
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de peliculas, consiguiendo un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación"

# Endpoint para obtener información sobre un director por nombre
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    director_movies = df_prod[df_prod['director'].str.contains(nombre_director, case=False, na=False)]
    if director_movies.empty:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    
    resultado = []
    for _, row in director_movies.iterrows():
        movie_details = df_num[df_num['id'] == row['id']].iloc[0]
        pelicula_info = df_info[df_info['id'] == row['id']].iloc[0]
        
        resultado.append(f"{pelicula_info['title']}, Fecha de Lanzamiento: {movie_details['release_date']}, "
                        f"Retorno: {movie_details['return']}, Costo: {movie_details['budget']}, "
                        f"Ganancia: {movie_details['revenue']}")

    peliculas_str = "  //////////  ".join(resultado)  # Unir todas las películas en una cadena separada por saltos de línea
    
    return f"El director {nombre_director} tiene {len(resultado)} películas registradas entre ellas:          {peliculas_str}"

def combinar_datos():
    # Cargar solo las columnas necesarias de df_num
    data_num_date = df_num[['id', 'release_date']]
    
    # Unir data_info con la columna 'release_date' de data_num
    combined_data = pd.merge(df_info, data_num_date, on='id')
    
    # Convertir 'release_date' a datetime si es necesario
    combined_data['release_date'] = pd.to_datetime(combined_data['release_date'])
    
    return combined_data

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    combined_data = combinar_datos()
    recomendaciones = recomendar_peliculas(combined_data, titulo)
    return (f"Recomendaciones para {titulo}: {recomendaciones}")
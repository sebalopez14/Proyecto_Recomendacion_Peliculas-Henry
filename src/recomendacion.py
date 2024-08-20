from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def vectorizar_generos_por_fecha(combined_data, indice_pelicula, chunk_size=1000): #Se hace por "chunks" para abarcar el df por partes y reducir el uso de memoria
    vectorizer = TfidfVectorizer()
    
    # Ordenar las películas por fecha de lanzamiento
    combined_data = combined_data.sort_values(by='release_date', ascending=True)
    
    # Seleccionar un chunk de películas cercanas en fecha
    start_index = max(0, indice_pelicula - chunk_size // 2)
    end_index = min(len(combined_data), start_index + chunk_size)
    
    selected_genres = combined_data['genres_name'].iloc[start_index:end_index]
    
    # Vectorizar solo el pequeño subconjunto de géneros
    tfidf_matrix = vectorizer.fit_transform(selected_genres)
    
    # Calcular la similitud del coseno para este subconjunto
    cosine_sim = cosine_similarity(tfidf_matrix)
    
    return cosine_sim, start_index

def obtener_indice_titulo(combined_data, titulo):
    try:
        return combined_data[combined_data['title'].str.contains(titulo, case=False)].index[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Película no encontrada")

def recomendar_peliculas(combined_data, titulo, num_recomendaciones=5):
    indice_pelicula = obtener_indice_titulo(combined_data, titulo)
    
    # Calcular similitudes solo para un pequeño grupo de películas en lugar de todas
    cosine_sim, start_index = vectorizar_generos_por_fecha(combined_data, indice_pelicula)
    
    # La similitud se calcula dentro del subconjunto, ajustamos el índice para el subconjunto
    adjusted_index = indice_pelicula - start_index
    similitudes = list(enumerate(cosine_sim[adjusted_index]))
    
    # Ordenar las similitudes y obtener las más altas
    similitudes = sorted(similitudes, key=lambda x: x[1], reverse=True)
    
    # Seleccionar los títulos de las películas similares, excluyendo la propia (basado en título)
    peliculas_similares = [combined_data['title'].iloc[start_index + i[0]]
                            for i in similitudes
                            if combined_data['title'].iloc[start_index + i[0]] != titulo][:num_recomendaciones]
    
    return peliculas_similares


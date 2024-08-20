# Proyecto de Sistema de Recomendación de Películas

Este proyecto tiene como objetivo crear un sistema de recomendación de películas utilizando un proceso de ETL (Extracción, Transformación y Carga) para procesar datos de películas.
Seguido de la creación de una API para disponibilizar la información y un modelo de Machine Learning para recomendar peliculas basado en el genero y fecha de una pelicula.

## Tabla de Contenido
- [Instalación y Requisitos](#instalación-y-requisitos)
- [Metodologías, datos y fuentes](#metodología,datos-y-fuentes)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Autor](#Autor)

## Instalación y Requisitos

### Requisitos
- Python 3.10 o superior
- FastAPI
- Uvicorn
- Scikit-learn
- Pandas
- Fastparquet

### Pasos de Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/sebalopez14/proyecto_individual01-dataft24.git
   ```
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activar el entorno virtual:
   - **Windows:** 
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:** 
     ```bash
     source venv/bin/activate
     ```
4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Metodologías, datos y fuentes
Durante el Análisis Exploratorio de Datos (EDA), se realizaron varias tareas sobre los archivos dados (movies_dataset.csv y credits.csv): 
Se chequearon valores nulos y duplicados, eliminando o imputando según el caso; se revisaron los valores faltantes y los tipos de datos. Además, se llevó a cabo un análisis estadístico para entender la distribución de las variables y se exploraron correlaciones para identificar relaciones significativas entre las variables que podrían influir en el modelo de Machine Learning.


Una vez Analizado los datos, pasamos al "ETL", cargando los datos, procesandolos teniendo en cuenta los analisis realizados. En un principio se eliminaron todos las filas de peliculas anteriores al 1975 para trabajar con informacion mas ligera,actual y relevante, actualmente ese codigo esta comentado. 
Todo este proceso nos deja un Dataframe limpio y optimo el cual se dividio en 4 archivos .parquet para optimizar el uso de memoria y almacenamiento.

## Estructura del Proyecto

- **`data/`**: Contiene los archivos de datos preprocesados y utilizados en el proyecto.
- **`notebooks/`**: Incluye los notebooks utilizados para realizar los procesos de EDA y ETL.
- **`src/`**: Código fuente del proyecto, ademas de la API, y el sistema de recomendacion (ademas del archivo "carga_data" que contiene la funcion para cargar los datos) .
- **`data_default/`**: Carpeta donde van los archivos "crudos" a procesar (no subidos al repositorio para optimizar almacenamiento).
- **`README.md`**: Documentación del proyecto (este archivo).

### Autor:
Este proyecto fue realizado por Sebastián López.

import os
import pandas as pd

def carga_data():
    # Obtener la ruta del directorio raíz del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Construir la ruta al directorio 'data' desde el directorio raíz del proyecto
    data_folder = os.path.join(project_root, 'data')
    
    # Leer los archivos .parquet desde la ruta construida
    df_num = pd.read_parquet(os.path.join(data_folder, 'data_num.parquet'))
    df_info = pd.read_parquet(os.path.join(data_folder, 'data_info.parquet'))
    df_prod = pd.read_parquet(os.path.join(data_folder, 'data_prod.parquet'))
    df_cast = pd.read_parquet(os.path.join(data_folder, 'data_cast.parquet'))
    
    return df_num, df_info, df_prod, df_cast


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, silhouette_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import KNNImputer
import seaborn as sns
import numpy as np

# Leer datos
def read_data(file_name):
    data = pd.read_csv(file_name)
    return data

# Preprocesamiento de datos
def preprocess_data(df):
    # Convertir columnas de ocupación a numéricas y llenar valores faltantes con KNNImputer
    occupancy_columns = ['1', '6', '8', '13', '15', '20', '22', '27']
    df[occupancy_columns] = df[occupancy_columns].apply(pd.to_numeric, errors='coerce')
    
    # Convertir precio a valores numéricos
    df['precio'] = df['precio'].replace('[\$,]', '', regex=True).astype(float)
    
    # Convertir pax a valores numéricos
    df['pax'] = pd.to_numeric(df['pax'], errors='coerce')
    
    # Aplicar KNNImputer a las columnas numéricas
    imputer = KNNImputer(n_neighbors=5)
    df[occupancy_columns + ['precio', 'pax']] = imputer.fit_transform(df[occupancy_columns + ['precio', 'pax']])
    
    # Convertir tipo a valores numéricos usando LabelEncoder
    le = LabelEncoder()
    df['tipo'] = le.fit_transform(df['tipo'])
    
    # Imprimir el mapeo de valores
    tipo_mapeo = dict(zip(le.classes_, le.transform(le.classes_)))
    print("Mapeo de tipos de alojamiento:", tipo_mapeo)
    
    # Rellenar valores faltantes para columnas categóricas
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    for column in categorical_columns:
        df[column].fillna(df[column].mode()[0], inplace=True)
    
    return df

# Normalizar características
def scale_features(df, features):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[features])
    return df_scaled

# Clustering
def perform_clustering(df, df_scaled):
    # DBSCAN clustering
    dbscan = DBSCAN(eps=0.75, min_samples=5)
    df['DBSCAN_Cluster'] = dbscan.fit_predict(df_scaled)
    
    # KMeans clustering
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['KMeans_Cluster'] = kmeans.fit_predict(df_scaled)
    
    # Calinski-Harabasz scores
    ch_score_dbscan = calinski_harabasz_score(df_scaled, df['DBSCAN_Cluster']) if len(set(df['DBSCAN_Cluster'])) > 1 else None
    ch_score_kmeans = calinski_harabasz_score(df_scaled, df['KMeans_Cluster'])
    
    # Silhouette scores
    silhouette_score_dbscan = silhouette_score(df_scaled, df['DBSCAN_Cluster']) if len(set(df['DBSCAN_Cluster'])) > 1 else None
    silhouette_score_kmeans = silhouette_score(df_scaled, df['KMeans_Cluster'])
    
    print("DBSCAN Clustering:")
    print("Calinski-Harabasz Score:", ch_score_dbscan)
    print("Silhouette Score:", silhouette_score_dbscan)
    print()
    
    print("KMeans Clustering:")
    print("Calinski-Harabasz Score:", ch_score_kmeans)
    print("Silhouette Score:", silhouette_score_kmeans)
    
    return df

# Guardar resultados
def save_results(df, file_name):
    df.to_csv(file_name, index=False)

# Visualización
def visualize_results(df):
    # Visualización para DBSCAN
    plt.figure(figsize=(10, 6))
    plt.scatter(df['tipo'], df['pax'], c=df['DBSCAN_Cluster'], cmap='viridis')
    plt.xlabel('Tipo de Alojamiento')
    plt.ylabel('Número de Personas (Pax)')
    plt.title('DBSCAN Clustering de Reservas')
    plt.colorbar(label='Cluster ID')
    plt.show()

    # Visualización para KMeans
    plt.figure(figsize=(10, 6))
    plt.scatter(df['tipo'], df['pax'], c=df['KMeans_Cluster'], cmap='viridis')
    plt.xlabel('Tipo de Alojamiento')
    plt.ylabel('Número de Personas (Pax)')
    plt.title('KMeans Clustering de Reservas')
    plt.colorbar(label='Cluster ID')
    plt.show()

# Main
def main():
    # Leer datos
    file_name = '../resultados/all_booking.xlsx'
    df = pd.read_excel(file_name, sheet_name='graficas')
    df.columns = df.columns.astype(str) 
    
    # Preprocesar datos
    df = preprocess_data(df)
    
    # Seleccionar características y normalizar
    features = ['tipo', 'pax', 'precio'] + ['1', '6', '8', '13', '15', '20', '22', '27']
    df_scaled = scale_features(df, features)
    
    # Aplicar clustering
    df_clustered = perform_clustering(df, df_scaled) 
    
    # Guardar resultados
    save_results(df_clustered, 'reservas_clustered.csv')
    
    # Visualizar resultados
    visualize_results(df_clustered)

if __name__ == "__main__":
    main()

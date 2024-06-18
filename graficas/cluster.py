import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, dendrogram
from pandas.plotting import parallel_coordinates
import seaborn as sns

# Crear directorio para guardar las visualizaciones
output_dir = "visualizaciones"
os.makedirs(output_dir, exist_ok=True)

def norm_to_zero_one(df):
    return (df - df.min()) / (df.max() - df.min())

def read_data(file_name):
    data = pd.read_excel(file_name, sheet_name='graficas')
    data.columns = data.columns.astype(str)
    print("Columnas del DataFrame:", data.columns)
    return data

def preprocess_data(df):
    occupancy_columns = ['1', '6', '8', '13', '15', '20', '22', '27']
    df[occupancy_columns] = df[occupancy_columns].apply(pd.to_numeric, errors='coerce')
    df['precio'] = df['precio'].replace('[\$,]', '', regex=True).astype(float)
    df['pax'] = pd.to_numeric(df['pax'], errors='coerce')
    
    imputer = KNNImputer(n_neighbors=5)
    df[occupancy_columns + ['precio', 'pax']] = imputer.fit_transform(df[occupancy_columns + ['precio', 'pax']])
    
    # Codificación One-Hot para la variable 'tipo'
    df = pd.get_dummies(df, columns=['tipo'])
    
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    for column in categorical_columns:
        df[column].fillna(df[column].mode()[0], inplace=True)
    
    return df

def scale_features(df, features):
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[features])
    return df_scaled

def elbow_method(data, feature_name):
    inertia_values = []
    max_clusters = 10

    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=5, random_state=123456)
        kmeans.fit(data)
        inertia_values.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    plt.plot(range(1, max_clusters + 1), inertia_values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    plt.title(f'Método del Codo para KMeans ({feature_name})', fontsize=16)
    plt.xlabel('Número de Clusters', fontsize=14)
    plt.ylabel('Inertia (WSS)', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f"ElbowMethod_{feature_name}.png"))
    plt.close()

def perform_kmeans_clustering(df, df_scaled, feature_name):
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['KMeans_Cluster'] = kmeans.fit_predict(df_scaled)
    
    ch_score = calinski_harabasz_score(df_scaled, df['KMeans_Cluster'])
    silhouette_avg = silhouette_score(df_scaled, df['KMeans_Cluster'])
    db_score = davies_bouldin_score(df_scaled, df['KMeans_Cluster'])
    
    print(f"KMeans Clustering ({feature_name}):")
    print("Calinski-Harabasz Score:", ch_score)
    print("Silhouette Score:", silhouette_avg)
    print("Davies-Bouldin Score:", db_score)
    
    return df, kmeans, ch_score, silhouette_avg, db_score

def perform_dbscan_clustering(df, df_scaled, feature_name):
    dbscan = DBSCAN(eps=0.35, min_samples=5)
    df['DBSCAN_Cluster'] = dbscan.fit_predict(df_scaled)
    
    if len(set(df['DBSCAN_Cluster'])) > 1:
        ch_score = calinski_harabasz_score(df_scaled, df['DBSCAN_Cluster'])
        silhouette_avg = silhouette_score(df_scaled, df['DBSCAN_Cluster'])
        db_score = davies_bouldin_score(df_scaled, df['DBSCAN_Cluster'])
    else:
        ch_score = silhouette_avg = db_score = None
    
    print(f"DBSCAN Clustering ({feature_name}):")
    print("Calinski-Harabasz Score:", ch_score)
    print("Silhouette Score:", silhouette_avg)
    print("Davies-Bouldin Score:", db_score)
    
    return df, dbscan, ch_score, silhouette_avg, db_score

def visualize_scatter_matrix(df, features, cluster_col, feature_name):
    df = df.copy()
    sns.set(style="whitegrid")
    variables = features.copy()
    variables.append(cluster_col)
    sns_plot = sns.pairplot(df[variables], hue=cluster_col, palette='husl', plot_kws={"s": 25}, diag_kind="hist")
    sns_plot.fig.tight_layout()
    sns_plot.fig.subplots_adjust(wspace=.03, hspace=.03)
    sns_plot.savefig(os.path.join(output_dir, f"scatter_matrix_{feature_name}_{cluster_col}.png"))
    plt.close()

def visualize_parallel_coordinates(df, cluster_col, feature_name):
    df = df.copy()
    df[cluster_col] = df[cluster_col].astype(str)
    for col in df.columns:
        if df[col].dtype != object:
            df[col] = df[col].astype(str)
    plt.figure(figsize=(15, 10))
    parallel_coordinates(df, cluster_col, color=plt.cm.Set2.colors)
    plt.title(f'Parallel Coordinates ({feature_name})', fontsize=16)
    plt.savefig(os.path.join(output_dir, f"parallel_coordinates_{feature_name}_{cluster_col}.png"))
    plt.close()

def visualize_heatmap(df, features, feature_name):
    corr = df[features].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', annot_kws={"size": 8})
    plt.title(f'Heatmap de Correlación ({feature_name})', fontsize=16)
    plt.savefig(os.path.join(output_dir, f"heatmap_corr_{feature_name}.png"))
    plt.close()

def visualize_silhouette(df_scaled, cluster_labels, cluster_name, feature_name):
    silhouette_vals = silhouette_samples(df_scaled, cluster_labels)
    y_ticks = []
    y_lower, y_upper = 0, 0
    for i, cluster in enumerate(np.unique(cluster_labels)):
        cluster_silhouette_vals = silhouette_vals[cluster_labels == cluster]
        cluster_silhouette_vals.sort()
        y_upper += len(cluster_silhouette_vals)
        plt.barh(range(y_lower, y_upper), cluster_silhouette_vals, edgecolor='none', height=1)
        y_ticks.append((y_lower + y_upper) / 2)
        y_lower += len(cluster_silhouette_vals)
    plt.axvline(np.mean(silhouette_vals), color="red", linestyle="--")
    plt.yticks(y_ticks, np.unique(cluster_labels) + 1)
    plt.ylabel("Cluster")
    plt.xlabel("Silhouette Coefficient")
    plt.title(f"Silhouette Plot para {cluster_name} ({feature_name})", fontsize=16)
    plt.savefig(os.path.join(output_dir, f"silhouette_plot_{cluster_name}_{feature_name}.png"))
    plt.close()

def visualize_dendrogram(df_scaled, feature_name):
    linked = linkage(df_scaled, 'ward')
    plt.figure(figsize=(10, 7))
    dendrogram(linked)
    plt.title(f'Dendrograma ({feature_name})', fontsize=16)
    plt.savefig(os.path.join(output_dir, f"dendrogram_{feature_name}.png"))
    plt.close()

def visualize_kmeans_centroids(kmeans, features, feature_name):
    centers = pd.DataFrame(kmeans.cluster_centers_, columns=features)
    centers_desnormal = centers.copy()
    plt.figure(figsize=(12, 10))
    sns.heatmap(centers, cmap="YlGnBu", annot=centers_desnormal, fmt='.3f', annot_kws={"size": 8})
    plt.title(f'Heatmap de Centroides de KMeans ({feature_name})', fontsize=16)
    plt.savefig(os.path.join(output_dir, f"centroides_kmeans_{feature_name}.png"))
    plt.close()

def visualize_pca(df_scaled, cluster_labels, cluster_name, feature_name):
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(df_scaled)
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis')
    legend_labels = [f'Cluster {i}' for i in np.unique(cluster_labels)]
    legend = plt.legend(handles=scatter.legend_elements()[0], labels=legend_labels, title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.title(f"PCA para {cluster_name} ({feature_name})")
    plt.savefig(os.path.join(output_dir, f"PCA_{cluster_name}_{feature_name}.png"), bbox_inches='tight')
    plt.close()

def main():
    file_name = '../resultados/all_booking.xlsx'
    df = read_data(file_name)
    
    df = preprocess_data(df)
    
    days = ['1', '6', '8', '13', '15', '20', '22', '27']
    base_features = [col for col in df.columns if 'tipo' in col] + ['pax', 'precio']
    
    for day in days:
        feature_name = f'tipo_pax_precio_{day}'
        features = base_features + [day]
        
        # Eliminar outliers
        Q1 = df[features].quantile(0.25)
        Q3 = df[features].quantile(0.75)
        IQR = Q3 - Q1
        df_filtered = df[~((df[features] < (Q1 - 1.5 * IQR)) | (df[features] > (Q3 + 1.5 * IQR))).any(axis=1)]
        
        # Normalización
        df_scaled = scale_features(df_filtered, features)
        
        # Método del codo
        elbow_method(df_scaled, feature_name)
        
        # Aplicar KMeans clustering
        df_clustered_kmeans, kmeans, kmeans_ch_score, kmeans_silhouette_avg, kmeans_db_score = perform_kmeans_clustering(df_filtered, df_scaled, feature_name)
        
        # Aplicar DBSCAN clustering
        df_clustered_dbscan, dbscan, dbscan_ch_score, dbscan_silhouette_avg, dbscan_db_score = perform_dbscan_clustering(df_filtered, df_scaled, feature_name)
        
        # Visualizaciones para KMeans
        visualize_scatter_matrix(df_clustered_kmeans, features, 'KMeans_Cluster', feature_name)
        visualize_silhouette(df_scaled, df_clustered_kmeans['KMeans_Cluster'], 'KMeans_Cluster', feature_name)
        visualize_kmeans_centroids(kmeans, features, feature_name)
        visualize_pca(df_scaled, df_clustered_kmeans['KMeans_Cluster'], 'KMeans_Cluster', feature_name)
        
        # Visualizaciones para DBSCAN
        if dbscan_silhouette_avg is not None:  # Para evitar errores si DBSCAN no encuentra suficientes clusters
            visualize_scatter_matrix(df_clustered_dbscan, features, 'DBSCAN_Cluster', feature_name)
            visualize_silhouette(df_scaled, df_clustered_dbscan['DBSCAN_Cluster'], 'DBSCAN_Cluster', feature_name)
            visualize_pca(df_scaled, df_clustered_dbscan['DBSCAN_Cluster'], 'DBSCAN_Cluster', feature_name)
        
        # Visualizaciones comunes
        visualize_parallel_coordinates(df_clustered_kmeans, 'KMeans_Cluster', feature_name)
        visualize_heatmap(df_filtered, features, feature_name)
        visualize_dendrogram(df_scaled, feature_name)

if __name__ == "__main__":
    main()

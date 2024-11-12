# -*- coding: utf-8 -*-
"""io.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zEhsLNruzhSWRmYKqXHKHjdkqCgCVg7e
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
from numba import jit, prange
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import kurtosis, skew
from google.colab import drive

# Montar Google Drive
drive.mount('/content/drive')

# Configurações globais
DRIVE_MOUNT_PATH = "/content/drive"
GRAPHPATH = os.path.join(DRIVE_MOUNT_PATH, "MyDrive/graficos")
SUMMARYPATH = os.path.join(DRIVE_MOUNT_PATH, "MyDrive/sumarios")
PALETTE = sns.color_palette("bright")  # Paleta de cores vibrante
FIGSIZE = (10, 6)

# Função para criar diretórios se não existirem
def create_directories(directories):
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Função para carregar dados
def load_data(filepath, delimiter=',', encoding='utf-8'):
    try:
        df = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding, on_bad_lines='skip')
        return dd.from_pandas(df, npartitions=4)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado - {filepath}")
        return None
    except pd.errors.ParserError as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

# Função para salvar gráficos
def save_fig(filename, graphpath):
    plt.savefig(os.path.join(graphpath, filename), dpi=300, bbox_inches='tight')
    plt.close()

# Função para agrupar dados em quartis
def group_data(df):
    df_computed = df.compute()
    df_computed['CargaHorariaGroup'] = pd.qcut(df_computed['CargaHorariaTotal'], 4, labels=["Baixa", "Moderada", "Alta", "Muito Alta"])
    df_computed['PublicoGroup'] = pd.qcut(df_computed['PublicoDiretoEstimado'], 4, labels=["Baixo", "Moderado", "Alto", "Muito Alto"])
    return dd.from_pandas(df_computed, npartitions=4)

# Classe para geração de gráficos
class GraphGenerator:
    def __init__(self, df, graphpath):
        self.df = df
        self.graphpath = graphpath

    def _compute_df(self):
        return self.df.compute()

    def _adjust_palette(self, hue):
        unique_hue_values = self._compute_df()[hue].nunique()
        if unique_hue_values > len(PALETTE):
            return sns.color_palette("bright", unique_hue_values)
        return PALETTE

    def generate_violinplot(self, x, y, hue, title, filename, split=False):
        plt.figure(figsize=FIGSIZE, facecolor='black')
        try:
            df_computed = self._compute_df()
            if df_computed[x].dropna().empty or df_computed[y].dropna().empty:
                print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
                return
            palette = self._adjust_palette(hue)
            sns.violinplot(x=x, y=y, hue=hue, data=df_computed, split=split, palette=palette)
            plt.gca().set_facecolor('black')
            plt.title(title, color='white')
            save_fig(filename, self.graphpath)
        except ValueError as e:
            print(f"Erro ao gerar gráfico de violino: {e}")

    def generate_histplot(self, x, hue, title, filename, bins=20):
        plt.figure(figsize=FIGSIZE, facecolor='black')
        try:
            df_computed = self._compute_df()
            if df_computed[x].dropna().empty:
                print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
                return
            palette = self._adjust_palette(hue)
            sns.histplot(df_computed, x=x, hue=hue, bins=bins, palette=palette, kde=True)
            plt.gca().set_facecolor('black')
            plt.title(title, color='white')
            save_fig(filename, self.graphpath)
        except ValueError as e:
            print(f"Erro ao gerar histograma: {e}")

    def generate_boxplot(self, x, y, hue, title, filename):
        plt.figure(figsize=FIGSIZE, facecolor='black')
        try:
            df_computed = self._compute_df()
            if df_computed[x].dropna().empty or df_computed[y].dropna().empty:
                print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
                return
            palette = self._adjust_palette(hue)
            sns.boxplot(x=x, y=y, hue=hue, data=df_computed, palette=palette)
            plt.gca().set_facecolor('black')
            plt.title(title, color='white')
            save_fig(filename, self.graphpath)
        except ValueError as e:
            print(f"Erro ao gerar boxplot: {e}")

    def generate_barplot(self, x, y, hue, title, filename):
        plt.figure(figsize=FIGSIZE, facecolor='black')
        try:
            df_computed = self._compute_df()
            if df_computed[x].dropna().empty or df_computed[y].dropna().empty:
                print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
                return
            palette = self._adjust_palette(hue)
            sns.barplot(x=x, y=y, hue=hue, data=df_computed, palette=palette)
            plt.gca().set_facecolor('black')
            plt.title(title, color='white')
            save_fig(filename, self.graphpath)
        except ValueError as e:
            print(f"Erro ao gerar gráfico de barras: {e}")

    def generate_scatterplot(self, x, y, hue, title, filename):
        plt.figure(figsize=FIGSIZE, facecolor='black')
        try:
            df_computed = self._compute_df()
            if df_computed[x].dropna().empty or df_computed[y].dropna().empty:
                print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
                return
            palette = self._adjust_palette(hue)
            sns.scatterplot(x=x, y=y, hue=hue, data=df_computed, palette=palette)
            plt.gca().set_facecolor('black')
            plt.title(title, color='white')
            save_fig(filename, self.graphpath)
        except ValueError as e:
            print(f"Erro ao gerar gráfico de dispersão: {e}")

    def generate_kdeplot(self, x, hue, title, filename):
        plt.figure(figsize=FIGSIZE, facecolor='black')
        try:
            df_computed = self._compute_df()
            if df_computed[x].dropna().empty:
                print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
                return
            palette = self._adjust_palette(hue)
            sns.kdeplot(data=df_computed, x=x, hue=hue, fill=True, palette=palette)
            plt.gca().set_facecolor('black')
            plt.title(title, color='white')
            save_fig(filename, self.graphpath)
        except ValueError as e:
            print(f"Erro ao gerar gráfico KDE: {e}")

# Função para gerar automaticamente todos os gráficos
def generate_all_graphs(df, graph_generator):
    graph_specs = [
        {'type': 'violinplot', 'x': 'CargaHorariaGroup', 'y': 'PublicoDiretoEstimado', 'hue': 'LinhaDeExtensao',
         'title': 'Violin: Público Estimado por Carga Horária e Linha de Extensão', 'filename': 'violin_publico_carga_linha.png'},
        {'type': 'histplot', 'x': 'PublicoGroup', 'hue': 'ObjetivosDeDesenvolvimentoSustentavel', 'title': 'Histograma: Público Estimado por Grupo',
         'filename': 'hist_publico_grupo.png'},
        {'type': 'scatterplot', 'x': 'CargaHorariaTotal', 'y': 'PublicoDiretoEstimado', 'hue': 'CargaHorariaGroup',
         'title': 'Scatterplot: Público Estimado vs Carga Horária Total', 'filename': 'scatter_publico_carga_grupo.png'}
    ]

    for spec in graph_specs:
        plot_type = spec.pop('type')
        getattr(graph_generator, f'generate_{plot_type}')(**spec)

# Função para gerar sumário estatístico
def generate_statistical_summary(df, summarypath):
    try:
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        summary = df[numeric_columns].describe().compute().T
        summary['variance'] = df[numeric_columns].var().compute()
        summary['skewness'] = [skew(df[col].compute()) for col in numeric_columns]
        summary['kurtosis'] = [kurtosis(df[col].compute()) for col in numeric_columns]
        summary.to_csv(os.path.join(summarypath, "summary_spss.csv"))
        print(f"Sumário estatístico salvo em: {summarypath}")
    except Exception as e:
        print(f"Erro ao gerar sumário estatístico: {e}")

# Função para bootstrap
@jit(nopython=True, parallel=True)
def bootstrap_jit(data, boots=1000):
    bs_data = np.empty(boots)
    for b in prange(boots):
        total = 0
        for s in range(data.shape[0]):
            total += data[np.random.randint(0, data.shape[0])]
        bs_data[b] = total / data.shape[0]
    return bs_data

# Função para calcular intervalos de confiança com bootstrap
def bootstrap_confidence_intervals(data, boots=1000, alpha=0.05):
    boot_means = bootstrap_jit(data, boots)
    lower = np.percentile(boot_means, 100 * alpha / 2)
    upper = np.percentile(boot_means, 100 * (1 - alpha / 2))
    return lower, upper

# Função para gerar gráficos adicionais solicitados
def generate_additional_graphs(df, graph_generator):
    additional_graph_specs = [
        {'type': 'kdeplot', 'x': 'PublicoDiretoEstimado', 'hue': 'ObjetivosDeDesenvolvimentoSustentavel',
         'title': 'KDE: Estimativa de Público Direto por Objetivo de Desenvolvimento Sustentável', 'filename': 'kde_publico_ods.png'},
        {'type': 'boxplot', 'x': 'CargaHorariaGroup', 'y': 'PublicoDiretoEstimado', 'hue': 'ObjetivosDeDesenvolvimentoSustentavel',
         'title': 'Boxplot: Público Estimado por Carga Horária e ODS', 'filename': 'box_publico_carga_ods.png'},
        {'type': 'violinplot', 'x': 'ObjetivosDeDesenvolvimentoSustentavel', 'y': 'CargaHorariaTotal', 'hue': 'PublicoGroup', 'split': True,
         'title': 'Violin: Carga Horária Total por ODS e Grupo de Público', 'filename': 'violin_carga_ods_publico.png'},
        {'type': 'violinplot', 'x': 'ObjetivosDeDesenvolvimentoSustentavel', 'y': 'PublicoDiretoEstimado', 'hue': 'CargaHorariaGroup', 'split': False,
         'title': 'Violin: Público Estimado por ODS e Carga Horária', 'filename': 'violin_publico_ods_carga.png'},
        {'type': 'polynomial_regression_plot', 'x': 'CargaHorariaTotal', 'y': 'PublicoDiretoEstimado',
         'title': 'Regressão Polinomial (Grau 3): Público Estimado vs Carga Horária', 'filename': 'poly_regression_publico_carga.png'}
    ]

    for spec in additional_graph_specs:
        plot_type = spec.pop('type')
        if plot_type == 'polynomial_regression_plot':
            generate_polynomial_regression_plot(df.compute(), **spec)
        else:
            getattr(graph_generator, f'generate_{plot_type}')(**spec)

# Função para gerar gráfico de regressão polinomial de grau 3
def generate_polynomial_regression_plot(df, x, y, title, filename, degree=3):
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression

    plt.figure(figsize=FIGSIZE, facecolor='black')
    try:
        if df[x].dropna().empty or df[y].dropna().empty:
            print(f"Erro ao gerar gráfico {filename}: dados insuficientes.")
            return

        # Preparar os dados
        X = df[[x]].dropna()
        y_data = df[y].dropna()

        if X.shape[0] != y_data.shape[0]:
            X, y_data = X.align(y_data, join='inner', axis=0)

        # Ajustar o modelo de regressão polinomial
        poly = PolynomialFeatures(degree)
        X_poly = poly.fit_transform(X)
        model = LinearRegression().fit(X_poly, y_data)
        y_pred = model.predict(X_poly)

        # Gerar gráfico de dispersão e linha de regressão
        sns.scatterplot(x=df[x], y=df[y], color='blue')
        plt.plot(X, y_pred, color='red', label=f'Regressão Polinomial (Grau {degree})')
        plt.gca().set_facecolor('black')
        plt.title(title, color='white')
        plt.legend()
        save_fig(filename, GRAPHPATH)
    except Exception as e:
        print(f"Erro ao gerar gráfico de regressão polinomial: {e}")

# Execução principal
create_directories([GRAPHPATH, SUMMARYPATH])

CSV_FILEPATH = "https://docs.google.com/spreadsheets/d/1FA_j6pAdUXh0q-2WUOiS-JeVU2rAhxaQExroDvnQPoM/export?format=csv&gid=511983049"
df = load_data(CSV_FILEPATH)

if df is not None:
    df = group_data(df)
    graph_generator = GraphGenerator(df, GRAPHPATH)

    if all(col in df.columns for col in ['ObjetivosDeDesenvolvimentoSustentavel', 'PublicoDiretoEstimado', 'CargaHorariaTotal']):
        generate_all_graphs(df, graph_generator)
        generate_statistical_summary(df, SUMMARYPATH)
        generate_additional_graphs(df, graph_generator)

        # Exemplo de uso de bootstrap
        data = np.random.normal(0, 1, size=100)
        lower, upper = bootstrap_confidence_intervals(data, boots=1000)
        print(f"Intervalo de confiança via bootstrap: {lower:.4f}, {upper:.4f}")
    else:
        print("Colunas necessárias ('ObjetivosDeDesenvolvimentoSustentavel', 'PublicoDiretoEstimado', 'CargaHorariaTotal') não estão presentes no dataframe.")
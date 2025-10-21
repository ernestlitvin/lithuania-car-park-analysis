# # =============================================================================
# # === 1. LIBRARY IMPORTS ===
# # =============================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# =============================================================================
# === 2. DATA LOADING & PREPARATION ===
# =============================================================================
# Load the dataset
# 1.1. Columns to use
cols_to_use = [
    'MARKE',
    'KOMERCINIS_PAV',
    'DEGALAI',
    'GAMYBOS_METAI',
    'PIRM_REG_DATA',
    'SPALVA',
    'GALIA',
    'SAVIVALDYBE'
]
# 1.2. Dictionary for optimization of data types. Using "category" to save memory, since the main file is over 900 MB
data_types = {
    'MARKE': 'category',
    'KOMERCINIS_PAV': 'category',
    'DEGALAI': 'category',
    'SPALVA': 'category',
    'SAVIVALDYBE': 'category'
}
file_path = "Atviri_TP_parko_duomenys.csv"
df_cars = pd.read_csv(
    file_path,
    usecols = cols_to_use,
    dtype=data_types
)
# --- Data Cleaning & Transformation ---
# Renaming columns to EN language ---

lt_cols = {
    'MARKE': 'mark',
    'KOMERCINIS_PAV': 'model',
    'DEGALAI': 'fuel_type',
    'GAMYBOS_METAI': 'production_year',
    'PIRM_REG_DATA': 'first_reg_date',
    'SPALVA': 'color',
    'GALIA': 'power',
    'SAVIVALDYBE': 'municipality'
}
df_cars = df_cars.rename(columns=lt_cols)

# Converting column "date" to datetime-format
df_cars["first_reg_date"] = pd.to_datetime(df_cars["first_reg_date"])

df_cars.info()














# H1: The Lithuanian car market is dominated by German brands, with Volkswagen being the single most popular make.
# H2: The share of electric and hybrid vehicles among newly registered cars has been growing significantly in the last 5 years.
# H3: The average age of cars in Vilnius is significantly lower than in other municipalities.
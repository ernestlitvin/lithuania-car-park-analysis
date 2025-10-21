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
# df_cars.info()

# Checking duplicates
# print(f"Rows before duplicates: {len(df_cars)}")
# df_cars.drop_duplicates(inplace=True)
# print(f"Rows after duplicates were removed: {len(df_cars)}")

# Checking "mark" counts and deleting unnecessary ("noisy") rows
# print(df_cars["mark"].value_counts().nsmallest(50))

mark_counts = df_cars["mark"].value_counts()
threshold = 100
rare_marks = mark_counts[mark_counts <= threshold].index.tolist()

# print(f"Rows before filtering of rare marks: {len(df_cars)}")
df_cars = df_cars[~df_cars["mark"].isin(rare_marks)]
# print(f"Rows after filtering of rare marks: {len(df_cars)}")
df_cars["mark"] = df_cars["mark"].cat.remove_unused_categories()

# Applying same logic, but for "model" column.
# print(df_cars['model'].value_counts())
print(df_cars["model"].value_counts().nlargest(50))
garbage_models = ["Nuasmeninta", "-", "---"]
df_cars = df_cars[~df_cars["model"].isin(garbage_models)]

# print(df_cars['model'].value_counts())
model_counts = df_cars["model"].value_counts()
# print(model_counts)
threshold = 100
rare_models = model_counts[model_counts <= threshold].index.tolist()

# print(f"Rows before filtering of rare marks: {len(df_cars)}")
df_cars = df_cars[~df_cars["model"].isin(rare_models)]
# print(f"Rows after filtering of rare marks: {len(df_cars)}")
df_cars["model"] = df_cars["model"].cat.remove_unused_categories()
# print(df_cars['model'].value_counts())






# Filtering data by production year

# print(df_cars["production_year"].describe())

# print(f"Rows before year filter: {len(df_cars)}")
df_cars = df_cars[
    (df_cars["production_year"] >= 1990) | (df_cars["production_year"].isnull())
]
# print(f"Rows after year filter: {len(df_cars)}")














# H1: The Lithuanian car market is dominated by German brands, with Volkswagen being the single most popular make.
# H2: The share of electric and hybrid vehicles among newly registered cars has been growing significantly in the last 5 years.
# H3: The average age of cars in Vilnius is significantly lower than in other municipalities.
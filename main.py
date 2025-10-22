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
    'KATEGORIJA_KLASE',
    'SPALVA',
    'GALIA',
    'SAVIVALDYBE'
]
# 1.2. Dictionary for optimization of data types. Using "category" to save memory, since the main file is over 900 MB
data_types = {
    'MARKE': 'category',
    'KOMERCINIS_PAV': 'category',
    'KATEGORIJA_KLASE': 'category',
    'DEGALAI': 'category',
    'SPALVA': 'category',
    'SAVIVALDYBE': 'category'
}
file_path = 'Atviri_TP_parko_duomenys.csv'
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
    'KATEGORIJA_KLASE': "car_cat",
    'SPALVA': 'color',
    'GALIA': 'power',
    'SAVIVALDYBE': 'municipality'
}
df_cars = df_cars.rename(columns=lt_cols)

# Converting column "date" to datetime-format
df_cars['first_reg_date'] = pd.to_datetime(df_cars['first_reg_date'])
# df_cars.info()

# Filtering only M1 car categories
df_cars = df_cars[df_cars['car_cat'] == "M1"]

# Normalization of register
df_cars['mark'] = df_cars['mark'].str.upper()
df_cars['model'] = df_cars['model'].str.upper()

# Checking duplicates
# print(f"Rows before duplicates: {len(df_cars)}")
df_cars.drop_duplicates(inplace=True)
# print(f"Rows after duplicates were removed: {len(df_cars)}")

# Deleting unused columns(0)
categorical_cols = df_cars.select_dtypes(include=['category']).columns
for col in categorical_cols:
    df_cars[col] = df_cars[col].cat.remove_unused_categories()

# Filtering TOP50 list of 'marks' and updating dictionary

corrections = {
    'VW': 'VOLKSWAGEN',
    'VOLKSWAGEN. VW': 'VOLKSWAGEN',
    'VOLKSWAGEN-VW': 'VOLKSWAGEN',
    'VOLKSWAGEN-VW VOLKSWAGEN. VW': 'VOLKSWAGEN',
    'MERCEDES-BENZ': 'MERCEDES',
    'MERCEDES BENZ': 'MERCEDES',
    'BAYER.MOT.WERKE-BMW': 'BMW',
    'BMW AG': 'BMW',
    'BMW I': 'BMW',
    'DAIMLERCHRYSLER (D)': 'CHRYSLER',
    'FORD (D)': 'FORD',
    'ROVER': 'LAND ROVER',
    'TOYOTA MEM (B)': 'TOYOTA',
    'SKODA (CZ)': 'SKODA',
    'SEAT (E)': 'SEAT',
    'RENAULT/CARPOL': 'RENAULT',
    'RENAULT (F)': 'RENAULT',
    'VOLVO (S)': 'VOLVO',
    'PEUGEOT (F)': 'PEUGEOT',
    'AUDI AUDI': 'AUDI',
    'FUJI HEAVY IND.(J)': 'SUBARU',
    'NISSAN EUROPE (F)': 'NISSAN',
    'MITSUBISHI (J)': 'MITSUBISHI',
    'FORD (D) FORD': 'FORD',
    'KIA MOTOR (ROK)': 'KIA',
    'VOLVO (S) VOLVO': 'VOLVO',
    'TESLA MOTORS': 'TESLA',
    'ADAM OPEL GMBH': 'OPEL',
    'SKODA (CZ) SKODA': 'SKODA',
    'HYUNDAI MOTOR (ROK)': 'HYUNDAI',
    'JAGUAR LAND ROVER LIMITED': 'LAND ROVER',
    'OPEL OPEL': 'OPEL',
    'BAYER.MOT.WERKE-BMW BMW': 'BMW',
    'CITROEN (F)': 'CITROEN',
    'B.M.W.': 'BMW',
    'MAZDA (J)': 'MAZDA',
    'FIAT (I)': 'FIAT',
    'DAIMLERCHRYSLER (USA)': 'CHRYSLER',
    'HONDA MOTOR (J)': 'HONDA',
    'DAIMLERCHRYSLER AG': 'CHRYSLER',
    'FORD W GMBH': 'FORD',
    'MERCEDES-AMG': 'MERCEDES',
    'HONDA (GB)': 'HONDA',
    'LANDROVER': 'LAND ROVER',
    'DAIMLER AG': 'MERCEDES',
    'TOYOTA EUROPE (B)': 'TOYOTA',
    'FUJI HEAVY IND. (J)': 'SUBARU',
    'ALFA': 'ALFA ROMEO',
    'DS': 'CITROEN',
    'SSANGYONG': 'SSANG YONG'
}

# Replacing 'mark' values in a category column, because of the warning
df_cars['mark'] = df_cars['mark'].astype('object')
df_cars['mark'] = df_cars['mark'].replace(corrections)
df_cars['mark'] = df_cars['mark'].astype('category')

# Adding filter to remove values, which are less than 100 counts (removing 'noisy' values)
mark_counts = df_cars['mark'].value_counts()
threshold = 100
rare_marks = mark_counts[mark_counts <= threshold].index.tolist()

# print(f'Rows before filtering of rare marks: {len(df_cars)}')
df_cars = df_cars[~df_cars['mark'].isin(rare_marks)]
# print(f'Rows after filtering of rare marks: {len(df_cars)}')
df_cars['mark'] = df_cars['mark'].cat.remove_unused_categories()

# Removing "garbage" data
garbage_mark = ['NUASMENINTA']
df_cars = df_cars[~df_cars['mark'].isin(garbage_mark)]
df_cars['mark'] = df_cars['mark'].cat.remove_unused_categories()


# TOP50 CARS
# top_50 = df_cars['mark'].value_counts()
# print(top_50)

# # ==================================================================================
# # === 3.0. EXPLORATORY DATA ANALYSIS (EDA) ===
# # ==================================================================================
# # --- Providing basic statistics

# Most popular cars 'marks' in Lithuania. Filtering TOP9 and Others

marks_top9 = df_cars['mark'].value_counts()[:9]
other_marks_count = df_cars['mark'].value_counts()[9:].sum()
other_counts = {'Other': other_marks_count }
other_marks = pd.Series(other_counts)
top10_cars = pd.concat([marks_top9, other_marks])

# Visualization of results TOP10 'pie chart'
# fig = plt.figure(figsize=(8, 8))
# plt.pie(top10_cars, labels = top10_cars.index, autopct='%1.1f%%')
# plt.title('TOP10 car marks in Lithuania')
# plt.show()

# Visualization of TOP20 'bar chart'
marks_top20 = df_cars['mark'].value_counts()[:20]
print(marks_top20)


















# top3 'marks' in top3 'models'
# car 'marks' by ages
# amount of cars in municipalities
# what are the most popular colors of cars in LT ?

first_rows = df_cars.columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# print(first_rows)












#
#
#
#
#
#
# # Checking "mark" counts and deleting unnecessary ("noisy") rows
#
# mark_counts = df_cars["mark"].value_counts()
# threshold = 10
# rare_marks = mark_counts[mark_counts <= threshold].index.tolist()
#
# # print(f"Rows before filtering of rare marks: {len(df_cars)}")
# df_cars = df_cars[~df_cars["mark"].isin(rare_marks)]
# # print(f"Rows after filtering of rare marks: {len(df_cars)}")
# df_cars["mark"] = df_cars["mark"].cat.remove_unused_categories()
#
# # print(df_cars["mark"].value_counts().nsmallest(50))
#
#
# # print(df_cars["mark"].value_counts().nlargest(50))
# garbage_models = ["Nuasmeninta", "SAVOS GAMYBOS", "SAVOS" ]
# df_cars = df_cars[~df_cars["mark"].isin(garbage_models)]
#
# # Applying same logic, but for "model" column.
# # print(df_cars['model'].value_counts())
# # print(df_cars["model"].value_counts().nlargest(50))
# garbage_models = ["Nuasmeninta", "-", "---"]
# df_cars = df_cars[~df_cars["model"].isin(garbage_models)]
#
# # print(df_cars['model'].value_counts())
# model_counts = df_cars["model"].value_counts()
# # print(model_counts)
# threshold = 100
# rare_models = model_counts[model_counts <= threshold].index.tolist()
#
# # print(f"Rows before filtering of rare marks: {len(df_cars)}")
# df_cars = df_cars[~df_cars["model"].isin(rare_models)]
# # print(f"Rows after filtering of rare marks: {len(df_cars)}")
# # df_cars["model"] = df_cars["model"].cat.remove_unused_categories()
# # print(df_cars['model'].value_counts())






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
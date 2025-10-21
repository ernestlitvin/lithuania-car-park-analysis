import pandas as pd

# 1. Cols to use
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

# 2. Dictionary for optimization of data types. We use 'category' to save memory.
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

# print("Data successfully loaded!")
# df_cars.info()



# H1: The Lithuanian car market is dominated by German brands, with Volkswagen being the single most popular make.
# H2: The share of electric and hybrid vehicles among newly registered cars has been growing significantly in the last 5 years.
# H3: The average age of cars in Vilnius is significantly lower than in other municipalities.
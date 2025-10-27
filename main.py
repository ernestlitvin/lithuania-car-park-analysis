# # =============================================================================
# # === 1. LIBRARY IMPORTS ===
# # =============================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from constants import corrections, corrections_models, colors_update

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

# Removing "garbage" data in 'mark' column
garbage_mark = ['NUASMENINTA']
df_cars = df_cars[~df_cars['mark'].isin(garbage_mark)]
df_cars['mark'] = df_cars['mark'].cat.remove_unused_categories()

# Corrections values in 'model' column
df_cars['model'] = df_cars['model'].astype('object')
df_cars['model'] = df_cars['model'].replace(corrections_models)
df_cars['model'] = df_cars['model'].astype('category')

# Removing "garbage" data in 'model' column
garbage_model = ['NUASMENINTA', '-', ]
df_cars = df_cars[~df_cars['model'].isin(garbage_model)]
df_cars['model'] = df_cars['model'].cat.remove_unused_categories()

# Removing "garbage" data in 'municipality' column
df_cars['municipality'] = df_cars['municipality'].str.strip()
garbage_municipality = ['ČEKIJA.', 'LATVIJA.', 'BALTARUSIJA.', 'JUNGTINĖ KARALYSTĖ.', 'KANADA.']
df_cars = df_cars[~df_cars['municipality'].isin(garbage_municipality)]
df_cars['municipality'] = df_cars['municipality'].astype('category')
df_cars['municipality'] = df_cars['municipality'].cat.remove_unused_categories()

# Updating 'Color' section dictionary
df_cars['color'] = df_cars['color'].astype('object')
df_cars['color'] = df_cars['color'].replace(colors_update)
df_cars['color'] = df_cars['color'].astype('category')


# # ==================================================================================
# # === 3.0. EXPLORATORY DATA ANALYSIS (EDA) ===
# # ==================================================================================
# # --- Providing basic statistics

# Most popular cars 'marks' in Lithuania. Filtering TOP9 and 'Others'
marks_top9 = df_cars['mark'].value_counts()[:9]
other_marks_count = df_cars['mark'].value_counts()[9:].sum()
other_counts = {'Others': other_marks_count }
other_marks = pd.Series(other_counts)
top10_cars = pd.concat([marks_top9, other_marks])

# Visualization of results TOP10 in 'pie chart'
colors = ['#B0B0B0', '#36454F', '#6495ED', '#F5F5F5', '#F08080', '#98FB98', '#D2B48C', '#FFD700', '#9370DB', '#20B2AA']
fig = plt.figure(figsize=(8, 8))
plt.pie(top10_cars, labels = top10_cars.index, autopct='%1.1f%%', colors = colors)
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Top 10 Car Marks in Lithuania')
plt.show()

# Visualization of TOP20 'bar chart'
marks_top20 = df_cars['mark'].value_counts().head(20)
total_cars = len(df_cars)
percentages = [f'{100 * v / total_cars:.1f}%' for v in marks_top20.values]
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=marks_top20.values, y=marks_top20.index.astype(str), palette = "viridis", hue = marks_top20.index.astype(str), legend=False)
plt.xlabel("Registered Cars in LT")
plt.ylabel("Mark")
plt.title("Top 20 Cars Marks in Lithuania")
for i, container in enumerate(ax.containers):
    ax.bar_label(container, labels=[percentages[i]], fontsize=9, label_type='edge', padding=5)
plt.tight_layout()
plt.show()

# TOP3 'Models' in each TOP3 'Marks'
# Looking for TOP3 Models:
marks_top3 = df_cars['mark'].value_counts().head(3)
top_3_name = marks_top3.index
df_cars_top3_model = df_cars[df_cars['mark'].isin(top_3_name)]

df_marks_grouped = df_cars_top3_model.groupby('mark', observed=True)['model'].value_counts()
df_models_top3 = df_marks_grouped.groupby('mark', observed=True).head(3)

# Visualization of TOP3 'Models' in each 'Mark'

df_models_top3 = df_models_top3.reset_index()
top_3_brands = df_models_top3['mark'].unique().tolist()

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
fig.suptitle('Top 3 Models of Top 3 Marks in Lithuania', fontsize=20)

for i, brand in enumerate(top_3_brands):
    ax = axes[i]

    brand_data = df_models_top3[df_models_top3['mark'] == brand].copy()
    brand_data['model'] = brand_data['model'].cat.remove_unused_categories()

    sns.barplot(
        data=brand_data,
        x='model',
        y='count',
        ax=ax,
        palette='viridis',
        hue='model',
        legend=False
    )

    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=10, padding=3)


    ax.set_title(brand, fontsize=16)
    ax.set_xlabel('Model', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

axes[0].set_ylabel('Number of Registered Cars', fontsize=12)
plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])
plt.show()

# Average 'age' of cars by 'marks'

# Extract year of registration, since 'production year' is almost empty
df_cars['reg_year'] = pd.DatetimeIndex(df_cars["first_reg_date"]).year
# Get a real 'age' of car
current_year = pd.Timestamp.now().year
df_cars['car_year'] = current_year - df_cars['reg_year']

car_year = df_cars['car_year'].value_counts().nlargest(50)
# print(car_year)

# Grouping 'marks' by years.
df_grouped_marks_year = df_cars.groupby('mark', observed = True)['car_year'].mean()
df_grouped_marks_year = df_grouped_marks_year.round(1).reset_index().sort_values(ascending=False, by = ['car_year'])

# Visualization of 'TOP15 of the oldest cars'

marks_year_top15 = df_grouped_marks_year.head(15).copy()
marks_year_top15['mark'] = marks_year_top15['mark'].cat.remove_unused_categories()
plot_order = marks_year_top15['mark'].tolist()

plt.figure(figsize=(12, 7))
ax = sns.barplot(x = 'car_year', y = 'mark', data = marks_year_top15, hue = 'car_year', palette = "coolwarm", legend = False, order = plot_order)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f years')

plt.xlabel("Average Age of Car")
plt.ylabel("Car Marks")
plt.title("Top 15 Oldest Cars in Lithuania")
plt.tight_layout()
sns.despine()
plt.show()

# ## Visualization of 'TOP15 of the newest cars'

marks_year_top15 = df_grouped_marks_year.tail(15).copy()
marks_year_top15['mark'] = marks_year_top15['mark'].cat.remove_unused_categories()
plot_order = marks_year_top15['mark'].tolist()

plt.figure(figsize=(12, 7))
ax = sns.barplot(x = 'car_year', y = 'mark', data = marks_year_top15, hue = 'car_year', palette = "coolwarm", legend = False, order = plot_order)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f years')

plt.xlabel("Average Age of Car")
plt.ylabel("Car Marks")
plt.title("Top 15 Newest Cars in Lithuania")
plt.tight_layout()
sns.despine()
plt.show()

# Creating labels for cars conditions:
# Very New (0-5y) / New (5-10y) / Middle (10-15y) / Old (15-20y) / Old (>20y)

bins = [0,5,10,15,20,float('inf')]
lab = ['Very New (0-5y]',
       'New (5-10y]',
       'Middle (10-15y]',
       'Old (15-20y]',
       'Very Old (>20y)']

df_cars['car_condition'] = pd.cut(df_cars['car_year'], bins=bins, labels=lab, include_lowest=True, right = True)

## Drop NaN
# print(f"Number of cars with unknown age: {df_cars['car_condition'].isnull().sum()}")
df_for_plot = df_cars.dropna(subset=['car_condition'])
# print(f"Number of cars without unknown age: {df_for_plot['car_condition'].isnull().sum()}")

# Visualization Count of Cars Conditions
count_conditions = df_for_plot['car_condition'].value_counts().reset_index()

plt.figure(figsize=(10, 4))
bx = sns.barplot(data = count_conditions, x = 'car_condition', y = 'count', hue = 'car_condition', legend = False, palette = 'icefire')

for container in bx.containers:
    bx.bar_label(container)

plt.title("Amount of Cars in Lithuania by Condition")
plt.xlabel("Condition")
plt.ylabel("Count")
plt.show()

# The amount of cars in municipalities and visualzation

cars_per_mun = df_cars['municipality'].value_counts().reset_index()
cars_per_mun_top10 = cars_per_mun.head(10)

plot_data = cars_per_mun_top10.sort_values(by='count', ascending=True)
plot_data['municipality'] = plot_data['municipality'].cat.remove_unused_categories()

#TOP10 cars per municipality
plt.figure(figsize=(12, 6))
cx = sns.barplot(data=plot_data, x='municipality', y='count', palette='magma', hue = 'municipality', legend = False)
for container in cx.containers:
    cx.bar_label(container)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Municipality")
plt.ylabel("Number of Cars")
plt.title("Top 10 Municipalities by Number of Registered Cars")
plt.tight_layout()
plt.show()

# The most popular colors of cars in LT
car_colors = df_cars['color'].value_counts().reset_index()
top7_car_colors = car_colors.head(7)

car_colors = df_cars['color'].value_counts()
top7_car_colors = car_colors.head(7).reset_index()

# Creating percentages of car colors
total_cars = len(df_cars)
custom_labels = []
for index, row in top7_car_colors.iterrows():
    color_name = row['color']
    count = row['count']

    percentage = 100 * count / total_cars
    label_text = f"{color_name}\n({percentage:.1f}%)"
    custom_labels.append(label_text)
#
# Visualization

labels = top7_car_colors['color']
color_map = {
    'Grey': '#B0B0B0',
    'Black': '#36454F',
    'Blue': '#6495ED',
    'White': '#F5F5F5',
    'Red': '#F08080',
    'Green': '#98FB98',
    'Brown': '#D2B48C'
}

plot_labels = top7_car_colors['color']
plot_colors = [color_map.get(label, '#808080') for label in plot_labels]

explode = [0.1] + [0] * 6

plt.figure(figsize=(10, 8))
wedges, texts = plt.pie(
    top7_car_colors['count'],
    labels=custom_labels,
    colors=plot_colors,
    explode=explode,
    startangle=90,
    wedgeprops={'edgecolor': 'white'})

centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Top 7 Colors of Cars in Lithuania (84.2% of All Auto Park)")
plt.show()


# # ==================================================================================
# # === 4. CHECKING THE HYPOTHESIS ===
# # ==================================================================================

# H1: The Lithuanian car market is dominated by German brands, with Volkswagen being the single most popular make.

german_marks = ['VOLKSWAGEN', 'AUDI', 'BMW', 'OPEL', 'MERCEDES', 'SMART', 'PORSCHE']
df_cars['is_german'] = df_cars['mark'].isin(german_marks)
german_brands = df_cars['is_german'].value_counts(normalize = True)

plot_labels = ['Other Brands', 'German Brands']
my_explode = [0.1, 0]
my_color = ['#98FB98', '#6495ED']
plt.pie(german_brands, labels = plot_labels , explode = my_explode, shadow = True, colors = my_color, startangle = 90, autopct='%1.1f%%')
plt.legend(title = 'Is Car German ?')
plt.title('Share of German Cars in the Lithuanian Auto Park')
plt.show()
# The most popular car on LT auto-park is VW, but the german brand cars are not 'dominating'. It is almost half of all cars in LT

# H2: The average age of cars in Vilnius is significantly lower than in other municipalities.

# Filtering cars from Vilnius and Others
is_vilnius = ['VILNIAUS M. SAV.', 'VILNIAUS R. SAV.']
df_cars['car_from_vilnius'] = df_cars['municipality'].isin(is_vilnius)
df_cars['Region'] = df_cars['car_from_vilnius'].map({True: 'Vilnius', False: 'Other Regions'})
age_by_mun = df_cars.groupby('car_from_vilnius')['car_year'].mean()

# Visualization and checking
x_ticks = np.arange(0, 100, 5)
g = sns.displot(data = df_cars, x = 'car_year', hue = 'Region', kind = 'kde', common_norm=False)
g.ax.set_xticks(x_ticks)
g.ax.grid(True)
g.ax.set_title('Density of Car Age: Vilnius vs. Other Regions')
plt.show()

y_ticks = np.arange(0, 100, 5)
ax = sns.boxplot(data=df_cars, x='Region', y='car_year')
ax.set_yticks(y_ticks)
ax.set_ylim(0, 45)
ax.set_xlabel("Region")
ax.set_ylabel("Car Year")
ax.set_title("Age distribution of cars: Vilnius vs. Other Regions")
plt.grid(True)
plt.show()

# Finding: Hypothesis 2 (H2) is Confirmed
# Average (Mean): The average age of cars in Vilnius is ~14.0 years, which is significantly lower than in other regions (~17.5 years).
#
# Density Plot (KDE) Analysis: The plot clearly shows a structural difference:
# Vilnius shows a pronounced peak in the newer car segment (0-10 years), which is almost absent in other regions.
# Conversely, "Other Regions" show a dominant peak in the older car segment (15-25 years), where they are proportionally more concentrated than in the capital.
#
# Boxplot Analysis: The boxplot confirms this difference is structural:
# The median (50th percentile) age for Vilnius is at ~13 years, while the median for "Other Regions" is at ~17 years.
# Key Finding: The median for Vilnius (~13 years) aligns with the lower quartile (25th percentile) for "Other Regions".
# This proves that 50% of cars in Vilnius are newer than 75% of cars in the rest of the country, confirming a significant difference in the auto park's structure.
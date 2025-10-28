import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- 3.0 EXPLORATORY DATA ANALYSIS (EDA) ---

def plot_top10_marks(df):
    """Visualizing Top-10 'marks' (Donut chart)"""
    print("Plotting: Top 10 Marks")
    marks_top9 = df['mark'].value_counts()[:9]
    other_marks_count = df['mark'].value_counts()[9:].sum()
    other_counts = {'Others': other_marks_count}
    other_marks = pd.Series(other_counts)
    top10_cars = pd.concat([marks_top9, other_marks])

    colors = ['#B0B0B0', '#36454F', '#6495ED', '#F5F5F5', '#F08080', '#98FB98', '#D2B48C', '#FFD700', '#9370DB',
              '#20B2AA']
    explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0.04)
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top10_cars, labels=top10_cars.index, autopct='%1.1f%%', colors=colors, explode=explode)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Top 10 Car Marks in Lithuania')
    plt.show()


def plot_top20_marks_barchart(df):
    """Visualization of Top-20 'marks' (Bar chart)"""
    print("Plotting: Top 20 Marks")
    marks_top20 = df['mark'].value_counts().head(20)
    total_cars = len(df)
    percentages = [f'{100 * v / total_cars:.1f}%' for v in marks_top20.values]
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x=marks_top20.values, y=marks_top20.index.astype(str), palette="viridis",
                     hue=marks_top20.index.astype(str), legend=False)
    plt.xlabel("Registered Cars in LT")
    plt.ylabel("Mark")
    plt.title("Top 20 Cars Marks in Lithuania")
    for i, container in enumerate(ax.containers):
        ax.bar_label(container, labels=[percentages[i]], fontsize=9, label_type='edge', padding=5)
    plt.tight_layout()
    plt.show()


def plot_top3_models_subplots(df):
    """Visualization of Top 3 'models' of Top 3 'marks' (Subplots)"""
    print("Plotting: Top 3 Models")
    marks_top3 = df['mark'].value_counts().head(3)
    top_3_name = marks_top3.index
    df_cars_top3_model = df[df['mark'].isin(top_3_name)]

    df_marks_grouped = df_cars_top3_model.groupby('mark', observed=True)['model'].value_counts()
    df_models_top3 = df_marks_grouped.groupby('mark', observed=True).head(3)

    df_models_top3 = df_models_top3.reset_index()
    top_3_brands = df_models_top3['mark'].unique().tolist()

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle('Top 3 Models of Top 3 Marks in Lithuania', fontsize=20)

    for i, brand in enumerate(top_3_brands):
        ax = axes[i]
        brand_data = df_models_top3[df_models_top3['mark'] == brand].copy()
        brand_data['model'] = brand_data['model'].cat.remove_unused_categories()

        sns.barplot(
            data=brand_data, x='model', y='count', ax=ax,
            palette='viridis', hue='model', legend=False
        )
        for container in ax.containers:
            ax.bar_label(container, label_type='edge', fontsize=10, padding=3)
        ax.set_title(brand, fontsize=16)
        ax.set_xlabel('Model', fontsize=12)
        ax.tick_params(axis='x', rotation=45)

    axes[0].set_ylabel('Number of Registered Cars', fontsize=12)
    plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])
    plt.show()


def plot_avg_age_barcharts(df):
    """Visualization of the Top 15 oldest and newest 'marks'"""
    print("Plotting: Average Age Charts")
    df_grouped_marks_year = df.groupby('mark', observed=True)['car_year'].mean()
    df_grouped_marks_year = df_grouped_marks_year.round(1).reset_index().sort_values(ascending=False, by=['car_year'])

    # --- Top 15 Oldest ---
    marks_year_top15_old = df_grouped_marks_year.head(15).copy()
    marks_year_top15_old['mark'] = marks_year_top15_old['mark'].cat.remove_unused_categories()
    plot_order_old = marks_year_top15_old['mark'].tolist()
    plt.figure(figsize=(12, 7))
    ax_old = sns.barplot(x='car_year', y='mark', data=marks_year_top15_old, hue='car_year', palette="coolwarm",
                         legend=False, order=plot_order_old)
    for container in ax_old.containers:
        ax_old.bar_label(container, fmt='%.1f years')
    plt.xlabel("Average Age of Car")
    plt.ylabel("Car Marks")
    plt.title("Top 15 Oldest Cars in Lithuania")
    plt.tight_layout()
    sns.despine()
    plt.show()

    # --- Top 15 Newest ---
    marks_year_top15_new = df_grouped_marks_year.tail(15).copy()
    marks_year_top15_new['mark'] = marks_year_top15_new['mark'].cat.remove_unused_categories()
    plot_order_new = marks_year_top15_new['mark'].tolist()
    plt.figure(figsize=(12, 7))
    ax_new = sns.barplot(x='car_year', y='mark', data=marks_year_top15_new, hue='car_year', palette="coolwarm_r", # R - обратная палитра
                         legend=False, order=plot_order_new)
    for container in ax_new.containers:
        ax_new.bar_label(container, fmt='%.1f years')
    plt.xlabel("Average Age of Car")
    plt.ylabel("Car Marks")
    plt.title("Top 15 Newest Cars in Lithuania")
    plt.tight_layout()
    sns.despine()
    plt.show()

def plot_condition_barchart(df):
    """Visualization by age categories (Very New, New, Middle, Old, Very Old)"""
    print("Plotting: Car Conditions")
    df_for_plot = df.dropna(subset=['car_condition'])
    count_conditions = df_for_plot['car_condition'].value_counts().reset_index()

    plt.figure(figsize=(10, 4))
    bx = sns.barplot(data=count_conditions, x='car_condition', y='count', hue='car_condition', legend=False,
                     palette='icefire')
    for container in bx.containers:
        bx.bar_label(container)
    plt.title("Amount of Cars in Lithuania by Condition")
    plt.xlabel("Condition")
    plt.ylabel("Count")
    plt.show()

def plot_municipality_barchart(df):
    """Visualization of the Top 10 municipalities"""
    print("Plotting: Top 10 Municipalities")
    cars_per_mun = df['municipality'].value_counts().reset_index()
    cars_per_mun_top10 = cars_per_mun.head(10)
    plot_data = cars_per_mun_top10.sort_values(by='count', ascending=True)
    plot_data['municipality'] = plot_data['municipality'].cat.remove_unused_categories()

    plt.figure(figsize=(12, 6))
    cx = sns.barplot(data=plot_data, x='municipality', y='count', palette='magma', hue='municipality', legend=False)
    for container in cx.containers:
        cx.bar_label(container)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Municipality")
    plt.ylabel("Number of Cars")
    plt.title("Top 10 Municipalities by Number of Registered Cars")
    plt.tight_layout()
    plt.show()

def plot_color_donut_chart(df):
    """Visualization of Top-7 colors (Donut chart)"""
    print("Plotting: Top 7 Colors")
    car_colors = df['color'].value_counts()
    top7_car_colors = car_colors.head(7).reset_index()
    total_cars = len(df)
    custom_labels = []
    for index, row in top7_car_colors.iterrows():
        color_name = row['color']
        count = row['count']
        percentage = 100 * count / total_cars
        label_text = f"{color_name}\n({percentage:.1f}%)"
        custom_labels.append(label_text)

    color_map = {'Grey': '#B0B0B0', 'Black': '#36454F', 'Blue': '#6495ED', 'White': '#F5F5F5', 'Red': '#F08080',
                 'Green': '#98FB98', 'Brown': '#D2B48C'}
    plot_labels = top7_car_colors['color']
    plot_colors = [color_map.get(label, '#808080') for label in plot_labels]
    explode = [0.1] + [0] * 6

    plt.figure(figsize=(10, 8))
    wedges, texts = plt.pie(
        top7_car_colors['count'], labels=custom_labels, colors=plot_colors,
        explode=explode, startangle=90, wedgeprops={'edgecolor': 'white'}
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Top 7 Colors of Cars in Lithuania (84.2% of All Auto Park)")
    plt.show()


# --- 4. CHECKING THE HYPOTHESIS ---

def plot_hypothesis_1(df):
    """Visualization H1 (Share of German cars)"""
    print("Plotting: Hypothesis 1")
    german_brands = df['is_german'].value_counts(normalize=True)

    plot_labels = ['Other Brands', 'German Brands']
    my_explode = [0.1, 0]
    my_color = ['#98FB98', '#6495ED']
    plt.pie(german_brands, labels=plot_labels, explode=my_explode, shadow=True, colors=my_color, startangle=90,
            autopct='%1.1f%%')
    plt.legend(title='Is Car German ?')
    plt.title('Share of German Cars in the Lithuanian Auto Park')
    plt.show()


def plot_hypothesis_2(df):
    """Visualization H2 (Age of Vilnius vs. Others)"""
    print("Plotting: Hypothesis 2")

    # --- Displot ---
    x_ticks = np.arange(0, 100, 5)
    g = sns.displot(data=df, x='car_year', hue='Region', kind='kde', common_norm=False)
    g.ax.set_xticks(x_ticks)
    g.ax.grid(True)
    g.ax.set_title('Density of Car Age: Vilnius vs. Other Regions')
    plt.show()

    # --- Boxplot ---
    y_ticks = np.arange(0, 100, 5)
    ax = sns.boxplot(data=df, x='Region', y='car_year')
    ax.set_yticks(y_ticks)
    ax.set_ylim(0, 45)
    ax.set_xlabel("Region")
    ax.set_ylabel("Car Year")
    ax.set_title("Age distribution of cars: Vilnius vs. Other Regions")
    plt.grid(True)
    plt.show()
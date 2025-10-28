import pandas as pd
from constants import (
    COLS_TO_USE, DATA_TYPES, LT_COLS, CORRECTIONS, CORRECTIONS_MODELS,
    COLORS_UPDATE, GARBAGE_MARK, GARBAGE_MODEL, GARBAGE_MUNICIPALITY,
    GERMAN_MARKS, IS_VILNIUS_LIST
)

def load_data(file_path):
    """
    Downloads data from CSV using pre-configured
    columns and data types for optimization.
    """
    print("Loading data...")
    df = pd.read_csv(
        file_path,
        usecols=COLS_TO_USE,
        dtype=DATA_TYPES
    )
    return df

def clean_data(df):
    """
    Performs all major data cleanup:
    - Renaming
    - Filtration 'M1'
    - Normalization and duplicates
    - 'Dictionaries' updating
    - Removal of "garbage"
    - Clearing unused categories
    """
    print("Cleaning data...")
    # Create copy to avoid error SettingWithCopyWarning
    df_clean = df.copy()

    # --- Renaming columns to EN language ---
    df_clean = df_clean.rename(columns=LT_COLS)

    # --- Filtering only M1 car categories (passenger car) ---
    df_clean = df_clean[df_clean['car_cat'] == "M1"]

    # --- Normalization of register ---
    df_clean['mark'] = df_clean['mark'].str.upper()
    df_clean['model'] = df_clean['model'].str.upper()

    # --- Deleting duplicates ---
    df_clean.drop_duplicates(inplace=True)

    # --- Replacing 'mark' values ---
    df_clean['mark'] = df_clean['mark'].astype('object')
    df_clean['mark'] = df_clean['mark'].replace(CORRECTIONS)
    df_clean['mark'] = df_clean['mark'].astype('category')

    # --- Adding filter to remove 'noisy' values ---
    mark_counts = df_clean['mark'].value_counts()
    threshold = 100
    rare_marks = mark_counts[mark_counts <= threshold].index.tolist()
    df_clean = df_clean[~df_clean['mark'].isin(rare_marks)]

    # --- Removing "garbage" data in 'mark' column ---
    df_clean = df_clean[~df_clean['mark'].isin(GARBAGE_MARK)]

    # --- Corrections values in 'model' column ---
    df_clean['model'] = df_clean['model'].astype('object')
    df_clean['model'] = df_clean['model'].replace(CORRECTIONS_MODELS)
    df_clean['model'] = df_clean['model'].astype('category')

    # --- Removing "garbage" data in 'model' column ---
    df_clean = df_clean[~df_clean['model'].isin(GARBAGE_MODEL)]

    # --- Removing "garbage" data in 'municipality' column ---
    df_clean['municipality'] = df_clean['municipality'].str.strip()
    df_clean = df_clean[~df_clean['municipality'].isin(GARBAGE_MUNICIPALITY)]
    df_clean['municipality'] = df_clean['municipality'].astype('category')

    # --- Updating 'Color' section dictionary ---
    df_clean['color'] = df_clean['color'].astype('object')
    df_clean['color'] = df_clean['color'].replace(COLORS_UPDATE)
    df_clean['color'] = df_clean['color'].astype('category')

    # --- Deleting unused categories (FINAL STEP) ---
    categorical_cols = df_clean.select_dtypes(include=['category']).columns
    for col in categorical_cols:
        df_clean[col] = df_clean[col].cat.remove_unused_categories()

    print("Cleaning complete.")
    return df_clean


def feature_engineering(df):
    """
    Creates new columns for analysis.
    - car_year (age)
    - car_condition (age category)
    - is_german (for H1)
    - Region (for H2)
    """
    print("Creating features...")
    df_feat = df.copy()

    # --- Average 'age' of cars ---
    df_feat['reg_year'] = pd.DatetimeIndex(df_feat["first_reg_date"]).year
    current_year = pd.Timestamp.now().year
    df_feat['car_year'] = current_year - df_feat['reg_year']

    # --- Car conditions labels ---
    bins = [0, 5, 10, 15, 20, float('inf')]
    lab = ['Very New (0-5y]',
           'New (5-10y]',
           'Middle (10-15y]',
           'Old (15-20y]',
           'Very Old (>20y)']
    df_feat['car_condition'] = pd.cut(df_feat['car_year'], bins=bins, labels=lab, include_lowest=True, right=True)

    # --- H1: German brands ---
    df_feat['is_german'] = df_feat['mark'].isin(GERMAN_MARKS)

    # --- H2: Vilnius vs. Others ---
    df_feat['car_from_vilnius'] = df_feat['municipality'].isin(IS_VILNIUS_LIST)
    df_feat['Region'] = df_feat['car_from_vilnius'].map({True: 'Vilnius', False: 'Other Regions'})

    print("Features engineering complete.")
    return df_feat
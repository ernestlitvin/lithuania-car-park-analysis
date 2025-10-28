import data_processing
import plotting

from constants import FILE_PATH


def main():
    """
    The main pipeline of the project:
    1. Loading data
    2. Data cleanup
    3. Feature creation (Feature Engineering)
    4. Building EDA plots
    5. Building plots for Hypotheses
    """

    # === Step 1: Load ===
    # Call load_data function from our data_processing file

    df_raw = data_processing.load_data(FILE_PATH)

    # === Step 2: Clean up ===

    df_clean = data_processing.clean_data(df_raw)

    # === Step 3: Creating features ===

    df_final = data_processing.feature_engineering(df_clean)

    # === Step 4: EDA & Visualization ===
    # Call functions from our plotting file

    plotting.plot_top10_marks(df_final)
    plotting.plot_top20_marks_barchart(df_final)
    plotting.plot_top3_models_subplots(df_final)
    plotting.plot_avg_age_barcharts(df_final)
    plotting.plot_condition_barchart(df_final)
    plotting.plot_municipality_barchart(df_final)
    plotting.plot_color_donut_chart(df_final)

    # === Step 5: Check the hypothesis ===

    plotting.plot_hypothesis_1(df_final)
    plotting.plot_hypothesis_2(df_final)

    print("\n--- Analysis complete. ---")

if __name__ == "__main__":
    main()
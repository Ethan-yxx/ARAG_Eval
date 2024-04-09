import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def json_to_long_format(json_str, trail_num, test_num):
    """
    Converts a JSON string into a long format DataFrame.
    
    Parameters:
    - json_str: The JSON string to convert.
    - trail_num: The trial number.
    - test_num: The test number.
    
    Returns:
    - A pandas DataFrame in long format.
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Parsing Error: {e} - When processing the following string: {json_str}")
        return pd.DataFrame()  # Return an empty DataFrame on error

    # Initialize a dictionary for the long format data
    long_data = {"Answer Type": [], "Dimension": [], "Trail Number": [], "Test Number": [], "Value": []}
    
    # Populate the dictionary
    for answer_key, metrics in data.items():
        answer_type = answer_key.split()[-1]
        for dimension, value in metrics.items():
            long_data["Answer Type"].append(answer_type)
            long_data["Dimension"].append(dimension)
            long_data["Trail Number"].append(trail_num)
            long_data["Test Number"].append(test_num)
            long_data["Value"].append(value)
            
    return pd.DataFrame(long_data)

def process_data_and_plot(input_excel, output_csv, fig_path):
    """
    Processes evaluation data from Excel, performs analysis, and plots results.
    
    Parameters:
    - input_excel: Path to the input Excel file.
    - output_csv: Path to save the aggregated results CSV.
    - fig_path: Base path to save figures.
    """
    # Load data, dropping any rows with missing data
    df = pd.read_excel(input_excel).dropna()
    final_df = pd.DataFrame()

    # Iterate through each evaluation result column
    for i in range(1, 11):  # Assuming 10 evaluations
        column_name = f"Evaluation Results_{i}"
        for j, json_str in enumerate(df[column_name]):
            if pd.notna(json_str):
                temp_df = json_to_long_format(json_str, j+1, i)
                final_df = pd.concat([final_df, temp_df], ignore_index=True)
    
    # Convert 'Value' to integer
    final_df['Value'] = final_df['Value'].astype('int')
    
    # Calculate and save average scores
    average_scores = final_df.groupby(['Answer Type', 'Dimension'])['Value'].mean().reset_index()
    average_scores.to_csv(output_csv, index=False)
    
    # Plotting
    plot_results(final_df, fig_path)

def plot_results(df, base_fig_path):
    """
    Generates and saves plots for the evaluation results.
    
    Parameters:
    - df: The DataFrame containing the evaluation results.
    - base_fig_path: Base path for saving figures.
    """
    plt.style.use('classic')
    
    # Define custom color palettes
    #palette_general = ['#504fa5', '#F7A19E', '#FFCBA4']
    palette_general = {'C': '#504fa5', 'A': '#F7A19E', 'B': '#FFCBA4'}

    palette_specific = {'C': '#504fa5', 'D': '#6f9de3', 'E': '#92dbed'}

    # Plot for Answer Types A, B, C
    plot_evaluation_scores(df[df['Answer Type'].isin(['A', 'B', 'C'])], palette_general, base_fig_path, "fig4.png", ['C', 'A', 'B'], ['ARAG', 'Copilot', 'Perplexity'])

    # Plot for Answer Types C, D, E
    plot_evaluation_scores(df[df['Answer Type'].isin(['C', 'D', 'E'])], palette_specific, base_fig_path, "fig5.png", ['C', 'D', 'E'], ['ARAG', 'w/o RAG', 'w/o A'])

def plot_evaluation_scores(filtered_df, palette, base_fig_path, fig_name, categories, legend_labels):
    """
    Plots evaluation scores for specified categories.
    
    Parameters:
    - filtered_df: The DataFrame filtered for specific answer types.
    - palette: The color palette for the plot.
    - base_fig_path: Base path for saving figures.
    - fig_name: Name of the figure file to save.
    - categories: Categories to plot.
    - legend_labels: Labels for the legend.
    """
    # Update the order of categories
    filtered_df['Answer Type'] = pd.Categorical(filtered_df['Answer Type'], categories)

    # Create and configure the plot
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Dimension', y='Value', hue='Answer Type', data=filtered_df, palette=palette, edgecolor='none', ci=None)
    plt.xlabel('Dimension', fontsize=16)
    plt.ylabel('Mean Score (0-5)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(labels=legend_labels, frameon=False, fontsize=14)

    sns.despine()  # Remove plot spines
    plt.tight_layout()  # Adjust layout to not cut off labels
    plt.savefig(f"{base_fig_path}/{fig_name}")
    plt.close()  # Close plot to free up memory

if __name__ == '__main__':
    input_excel = './results/arag_results.xlsx'
    output_csv = './results/average_scores.csv'
    fig_path = './figs'
    process_data_and_plot(input_excel, output_csv, fig_path)

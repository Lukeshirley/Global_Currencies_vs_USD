import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.colors import LinearSegmentedColormap

def format_for_heatmap(value):
    try:
        return float(value.replace('%', ''))
    except:
        return 0

def visualize_performance():
    df = pd.read_csv('currency_performance.csv')

    # List of top 14 countries (and EU) by GDP and their currencies
    major_currencies = {
        'USD': 'United States',
        'CNY': 'China',
        'JPY': 'Japan',
        'EUR': 'EU',
        'INR': 'India',
        'GBP': 'United Kingdom',
        'BRL': 'Brazil',
        'CAD': 'Canada',
        'RUB': 'Russia',
        'KRW': 'South Korea',
        'AUD': 'Australia',
        'MXN': 'Mexico',
        'IDR': 'Indonesia',
        'TRY': 'Turkey'
    }

    # Ensure the DataFrame is using the correct index
    df.set_index('currency', inplace=True)
    
    # Filter only those currencies that are available in the dataset
    available_major_currencies = {k: v for k, v in major_currencies.items() if k in df.columns}

    # Filter the DataFrame to include only the major currencies
    df_filtered = df[available_major_currencies.keys()]

    # Rename the columns to include country names
    df_filtered.columns = [f"{country} ({currency})" for currency, country in available_major_currencies.items()]

    # Transpose the DataFrame for proper visualization
    df_filtered = df_filtered.T

    # Convert the percentage values for heatmap visualization
    df_filtered_values = df_filtered.applymap(format_for_heatmap)

    # Custom colormap with clearer distinction
    colors = [(0, 'darkgreen'), (0.5, 'white'), (1, 'darkred')]
    cmap = LinearSegmentedColormap.from_list('custom_red_green', colors, N=256)

    # Get today's date in the desired format
    today_date = datetime.today().strftime('%B %d, %Y')

    # Create the title string with the current date
    title = f'Global Currencies vs USD as of {today_date} (2017 Baseline)'



    plt.figure(figsize=(20, 12))
    sns.heatmap(df_filtered_values, annot=df_filtered, cmap=cmap, fmt="", linewidths=.5, cbar=True, annot_kws={"size": 12}, center=0, vmin=-15, vmax=50)
    plt.title(title, fontsize=24, pad=20)
    plt.xlabel('Year', fontsize=15, labelpad=20)
    plt.ylabel('Currency', fontsize=15, labelpad=20)
    plt.xticks(ticks=[i + 0.5 for i in range(len(df_filtered.columns))], labels=[d[:4] for d in df_filtered.columns], rotation=0, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout(pad=3.0)
    plt.savefig('major_currency_performance_matrix.png', dpi=300)
    plt.show()

def main():
    visualize_performance()

if __name__ == "__main__":
    main()

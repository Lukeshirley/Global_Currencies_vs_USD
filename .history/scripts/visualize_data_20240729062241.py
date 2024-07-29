import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_for_heatmap(value):
    try:
        return float(value.replace('%', ''))
    except:
        return 0

def load_data(csv_path):
    logger.info(f"Loading data from {csv_path}")
    df = pd.read_csv(csv_path)
    logger.info(f"Data columns: {df.columns.tolist()}")
    logger.info(f"Data head:\n{df.head()}")
    return df

def visualize_performance(df):
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
    if 'currency' in df.columns:
        df.set_index('currency', inplace=True)
    else:
        logger.error("'currency' column is not in the DataFrame")
        return

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

    plt.figure(figsize=(20, 12))
    sns.heatmap(df_filtered_values, annot=df_filtered, cmap=cmap, fmt="", linewidths=.5, cbar=True, annot_kws={"size": 12}, center=0, vmin=-15, vmax=50)
    plt.title('Major Currency Performance Relative to USD (2017 baseline)', fontsize=24, pad=20)
    plt.xlabel('Year', fontsize=15, labelpad=20)
    plt.ylabel('Currency', fontsize=15, labelpad=20)
    plt.xticks(ticks=[i + 0.5 for i in range(len(df_filtered.columns))], labels=[d[:4] for d in df_filtered.columns], rotation=0, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout(pad=3.0)
    plt.savefig('major_currency_performance_matrix.png', dpi=300)
    plt.show()

    # Visualize cryptocurrency data
    cryptos = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    df_cryptos = df[cryptos]

    # Convert the percentage values for heatmap visualization
    df_cryptos_values = df_cryptos.applymap(format_for_heatmap)

    plt.figure(figsize=(20, 4))
    sns.heatmap(df_cryptos_values, annot=df_cryptos, cmap=cmap, fmt="", linewidths=.5, cbar=True, annot_kws={"size": 12}, center=0, vmin=-50, vmax=200)
    plt.title('Cryptocurrency Performance Relative to USD', fontsize=24, pad=20)
    plt.xlabel('Year', fontsize=15, labelpad=20)
    plt.ylabel('Cryptocurrency', fontsize=15, labelpad=20)
    plt.xticks(ticks=[i + 0.5 for i in range(len(df_cryptos.columns))], labels=[d[:4] for d in df_cryptos.columns], rotation=0, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout(pad=3.0)
    plt.savefig('crypto_performance_matrix.png', dpi=300)
    plt.show()

def main():
    csv_path = 'data/combined_performance.csv'
    df = load_data(csv_path)
    visualize_performance(df)

if __name__ == "__main__":
    main()


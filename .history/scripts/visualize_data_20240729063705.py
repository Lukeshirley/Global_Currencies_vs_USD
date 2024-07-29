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
        return float('nan')

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

    # Cryptocurrencies
    cryptocurrencies = ['BTC-USD', 'ETH-USD', 'SOL-USD']

    # Filter only those currencies that are available in the dataset
    available_major_currencies = {k: v for k, v in major_currencies.items() if k in df.columns}

    # Filter the DataFrame to include only the major currencies
    df_filtered = df[['date'] + list(available_major_currencies.keys()) + cryptocurrencies]

    # Rename the columns to include country names
    df_filtered.columns = ['date'] + [f"{country} ({currency})" for currency, country in available_major_currencies.items()] + cryptocurrencies

    # Transpose the DataFrame for proper visualization
    df_filtered.set_index('date', inplace=True)
    df_filtered = df_filtered.T

    # Convert the percentage values for heatmap visualization
    df_filtered_values = df_filtered.applymap(format_for_heatmap)

    # Custom colormap with clearer distinction
    colors = [(0, 'darkgreen'), (0.5, 'white'), (1, 'darkred')]
    cmap = LinearSegmentedColormap.from_list('custom_red_green', colors, N=256)

    # Separate fiat currencies and cryptocurrencies for visualization
    df_currencies = df_filtered_values.loc[[f"{country} ({currency})" for currency, country in available_major_currencies.items()]]
    df_cryptos = df_filtered_values.loc[cryptocurrencies]

    # Create an empty DataFrame to separate the two
    empty_row = pd.DataFrame([[''] * df_currencies.shape[1]], columns=df_currencies.columns, index=[''])

    # Concatenate the dataframes
    df_combined = pd.concat([df_currencies, empty_row, df_cryptos])

    plt.figure(figsize=(20, 12))
    sns.heatmap(df_combined.astype(float), annot=df_combined, cmap=cmap, fmt="", linewidths=.5, cbar=True, annot_kws={"size": 12}, center=0, vmin=-50, vmax=200)
    plt.title('Currency and Cryptocurrency Performance Relative to USD', fontsize=24, pad=20)
    plt.xlabel('Year', fontsize=15, labelpad=20)
    plt.ylabel('Currency/Cryptocurrency', fontsize=15, labelpad=20)
    plt.xticks(ticks=[i + 0.5 for i in range(len(df_combined.columns))], labels=[d[:4] for d in df_combined.columns], rotation=0, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout(pad=3.0)
    plt.savefig('currency_crypto_performance_matrix.png', dpi=300)
    plt.show()

def main():
    csv_path = 'data/combined_performance.csv'
    df = load_data(csv_path)
    visualize_performance(df)

if __name__ == "__main__":
    main()



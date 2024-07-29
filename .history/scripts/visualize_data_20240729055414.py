import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def format_for_heatmap(val):
    return f"{val:.2f} %"

def visualize_performance():
    df = pd.read_csv('data/currency_performance.csv')
    
    # List of top countries by GDP and their currencies, now including cryptocurrencies
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

    cryptocurrencies = {
        'BTC': 'Bitcoin',
        'ETH': 'Ethereum',
        'SOL': 'Solana'
    }

    # Ensure the DataFrame is using the correct index
    df.set_index('currency', inplace=True)
    
    # Filter only those currencies that are available in the dataset
    available_major_currencies = {k: v for k, v in major_currencies.items() if k in df.index}
    available_cryptocurrencies = {k: v for k, v in cryptocurrencies.items() if k in df.index}
    print("Available major currencies:")
    print(available_major_currencies)
    print("Available cryptocurrencies:")
    print(available_cryptocurrencies)

    if not available_major_currencies and not available_cryptocurrencies:
        print("None of the specified major currencies or cryptocurrencies are available in the dataset.")
        print("Available currencies:", df.index.tolist())
        return

    # Filter the DataFrame to include only the major currencies and cryptocurrencies
    df_filtered_currencies = df.loc[available_major_currencies.keys()]
    df_filtered_cryptocurrencies = df.loc[available_cryptocurrencies.keys()]

    # Combine the data with a space in between
    df_filtered_combined = pd.concat([df_filtered_currencies, pd.DataFrame([[''] * len(df.columns)], columns=df.columns), df_filtered_cryptocurrencies])
    print("Filtered data for major currencies and cryptocurrencies:")
    print(df_filtered_combined.head())  # Debugging: Check the filtered data

    # Rename the index to include country names
    df_filtered_combined.index = [f"{country} ({currency})" for currency, country in available_major_currencies.items()] + [''] + [f"{crypto} ({symbol})" for symbol, crypto in available_cryptocurrencies.items()]

    # Transpose the DataFrame for proper visualization
    df_filtered_combined = df_filtered_combined.T

    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(150, 10, as_cmap=True)  # Green and Red
    sns.heatmap(df_filtered_combined, annot=True, cmap=cmap, fmt=".2f", linewidths=.5, cbar=True, annot_kws={"size": 12}, center=0, vmin=-15, vmax=50)
    plt.title('Major Currency and Cryptocurrency Performance Relative to USD', fontsize=20, pad=20)
    plt.xlabel('Currency', fontsize=15)
    plt.ylabel('Year', fontsize=15)
    plt.xticks(ticks=range(len(df_filtered_combined.columns)), labels=[d[:4] for d in df_filtered_combined.columns], rotation=45, fontsize=12, ha='center')
    plt.yticks(fontsize=12)
    plt.tight_layout(pad=2)
    plt.savefig('output/major_currency_performance_matrix.png', dpi=300)
    plt.show()

def main():
    visualize_performance()

if __name__ == "__main__":
    main()

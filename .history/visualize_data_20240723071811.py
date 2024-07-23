import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_performance():
    # Load the CSV file
    df = pd.read_csv('currency_performance.csv')
    print("Loaded data:")
    print(df.head())  # Debugging: Check the loaded data

    # List of top 15 countries by GDP and their currencies
    major_currencies = {
        'USD': 'United States',
        'CNY': 'China',
        'JPY': 'Japan',
        'EUR': 'Germany',
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

    # Filter only those currencies that are available in the dataset
    available_major_currencies = {k: v for k, v in major_currencies.items() if k in df['currency'].values}
    print("Available major currencies:")
    print(available_major_currencies)

    if not available_major_currencies:
        print("None of the specified major currencies are available in the dataset.")
        print("Available currencies:", df['currency'].tolist())
        return

    # Filter the DataFrame to include only the major currencies
    df.set_index('currency', inplace=True)
    df = df.loc[available_major_currencies.keys()]
    print("Filtered data for major currencies:")
    print(df.head())  # Debugging: Check the filtered data

    # Rename the index to include country names
    df.index = [f"{country} ({currency})" for currency, country in available_major_currencies.items()]

    # Transpose the DataFrame for proper visualization
    df = df.T

    # Plot the data
    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(150, 10, as_cmap=True)  # Green and Red
    sns.heatmap(df, annot=True, cmap=cmap, fmt=".2f", linewidths=.5, cbar=True, annot_kws={"size": 12})
    plt.title('Major Currency Performance Relative to USD', fontsize=20)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Currency', fontsize=15)
    plt.xticks(ticks=range(len(df.columns)), labels=[d[:4] for d in df.columns], rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('major_currency_performance_matrix.png', dpi=300)
    plt.show()

def main():
    visualize_performance()

if __name__ == "__main__":
    main()

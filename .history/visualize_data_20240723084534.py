import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def format_for_heatmap(value):
    try:
        return float(value.replace('%', ''))
    except:
        return 0

def visualize_performance():
    df = pd.read_csv('currency_performance.csv')

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

    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(150, 10, s=80, l=55, n=9, as_cmap=True)  # Green and Red
    sns.heatmap(df_filtered_values, annot=df_filtered, cmap=cmap, fmt="", linewidths=.5, cbar=True, annot_kws={"size": 12}, center=0)
    plt.title('Major Currency Performance Relative to USD (2017 baseline)', fontsize=20)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Currency', fontsize=15)
    plt.xticks(ticks=range(len(df_filtered.columns)), labels=[d[:4] for d in df_filtered.columns], rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('major_currency_performance_matrix.png', dpi=300)
    plt.show()

def main():
    visualize_performance()

if __name__ == "__main__":
    main()

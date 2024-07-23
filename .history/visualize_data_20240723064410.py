# visualize_data.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_performance():
    df = pd.read_csv('currency_performance.csv', index_col=0).T

    # List of top 15 countries by GDP and their currencies
    major_currencies = ['USD', 'CNY', 'JPY', 'EUR', 'INR', 'GBP', 'BRL', 'CAD', 'RUB', 'KRW', 'AUD', 'MXN', 'IDR', 'TRY']

    # Get available currencies
    available_currencies = df.columns.tolist()

    # Filter only those currencies that are available in the dataset
    available_major_currencies = [currency for currency in major_currencies if currency in available_currencies]

    if not available_major_currencies:
        print("None of the specified major currencies are available in the dataset.")
        print("Available currencies:", available_currencies)
        return

    df = df[available_major_currencies]

    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(240, 10, n=9, as_cmap=True)
    sns.heatmap(df, annot=True, cmap=cmap, fmt=".2f", linewidths=.5, cbar=True, annot_kws={"size": 12})
    plt.title('Major Currency Performance Relative to USD', fontsize=20)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Currency', fontsize=15)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('major_currency_performance_matrix.png', dpi=300)
    plt.show()

def main():
    visualize_performance()

if __name__ == "__main__":
    main()






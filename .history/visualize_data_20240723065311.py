# visualize_data.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_performance():
    df = pd.read_csv('currency_performance.csv', index_col=0).T

    # Top 15 countries by GDP and their currencies
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
    available_major_currencies = {k: v for k, v in major_currencies.items() if k in df.columns}

    if not available_major_currencies:
        print("None of the specified major currencies are available in the dataset.")
        print("Available currencies:", df.columns.tolist())
        return

    df = df[list(available_major_currencies.keys())].T

    # Rename the index to include country names
    df.index = [f"{country} ({currency})" for currency, country in available_major_currencies.items()]

    # Remove the base year column
    df.drop('2017-12-31', axis=1, inplace=True)

    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(150, 10, as_cmap=True)  # Green and Red
    sns.heatmap(df, annot=True, cmap=cmap, fmt=".2f", linewidths=.5, cbar=True, annot_kws={"size": 12})
    plt.title('Major Currency








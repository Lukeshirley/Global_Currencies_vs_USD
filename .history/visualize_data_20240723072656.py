import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_performance():
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

    # Ensure the DataFrame is using the correct index
    df.set_index('currency', inplace=True)
    
    # Filter only those currencies that are available in the dataset
    available_major_currencies = {k: v for k, v in major_currencies.items() if k in df.index}
    print("Available major currencies:")
    print(available_major_currencies)

    if not available_major_currencies:
        print("None of the specified major currencies are available in the dataset.")
        print("Available currencies:", df.index.tolist())
        return

    # Filter the DataFrame to include only the major currencies
    df_filtered = df.loc[available_major_currencies.keys()]
    print("Filtered data for major currencies:")
    print(df_filtered.head())  # Debugging: Check the filtered data

    # Rename the index to include country names
    df_filtered.index = [f"{country} ({currency})" for currency, country in available_major_currencies.items()]

    # Transpose the DataFrame for proper visualization
    df_filtered = df_filtered.T

    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(150, 10, as_cmap=True)  # Green and Red
    sns.heatmap(df_filtered, annot=True, cmap=cmap, fmt=".2f", linewidths




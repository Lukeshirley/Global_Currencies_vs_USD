# visualize_data.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_performance():
    df = pd.read_csv('currency_performance.csv', index_col=0)
    plt.figure(figsize=(15, 10))
    sns.heatmap(df, annot=True, cmap=['red', 'green'], fmt=".2f", linewidths=.5, cbar=False)
    plt.title('Currency Performance Relative to USD')
    plt.xlabel('Currency')
    plt.ylabel('Year')
    plt.savefig('currency_performance_matrix.png')
    plt.show()

if __name__ == "__main__":
    visualize_performance()

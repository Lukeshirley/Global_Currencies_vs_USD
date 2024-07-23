# visualize_data.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_performance():
    df = pd.read_csv('currency_performance.csv', index_col=0)
    plt.figure(figsize=(20, 12))
    cmap = sns.diverging_palette(240, 10, n=9, as_cmap=True)
    sns.heatmap(df, annot=True, cmap=cmap, fmt=".2f", linewidths=.5, cbar=True, annot_kws={"size": 10})
    plt.title('Currency Performance Relative to USD', fontsize=20)
    plt.xlabel('Currency', fontsize=15)
    plt.ylabel('Year', fontsize=15)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig('currency_performance_matrix.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    visualize_performance()



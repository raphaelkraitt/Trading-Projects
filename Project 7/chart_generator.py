import matplotlib.pyplot as plt
import os
import config

def plot_portfolio_allocation(weights, save=True):
    labels = list(weights.keys())
    sizes = list(weights.values())
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Portfolio Allocation')
    plt.axis('equal')
    if save:
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"portfolio_allocation.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    else:
        plt.show()
        return ""

if __name__ == "__main__":
    weights = {'AAPL': 0.2, 'MSFT': 0.2, 'GOOGL': 0.2, 'AMZN': 0.2, 'TSLA': 0.2}
    print(plot_portfolio_allocation(weights, save=False)) 
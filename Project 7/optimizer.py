import numpy as np
import pandas as pd
from scipy.optimize import minimize
import config

def get_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    return price_df.pct_change().dropna()

def mean_variance_optimization(price_dfs, risk_free_rate=0.01):
    symbols = list(price_dfs.keys())
    returns = pd.concat([get_returns(df['Close']) for df in price_dfs.values()], axis=1)
    returns.columns = symbols
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(symbols)
    def portfolio_performance(weights):
        port_return = np.dot(weights, mean_returns)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = (port_return - risk_free_rate) / port_vol if port_vol > 0 else 0
        return -sharpe  # Negative for minimization
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    result = minimize(portfolio_performance, num_assets * [1. / num_assets], bounds=bounds, constraints=constraints)
    return dict(zip(symbols, result.x)), result

if __name__ == "__main__":
    # Example usage
    import mt5_portfolio
    portfolio = mt5_portfolio.MT5Portfolio()
    price_dfs = {s: portfolio.fetch_ohlcv(s) for s in config.PORTFOLIO_SYMBOLS}
    portfolio.shutdown()
    weights, result = mean_variance_optimization(price_dfs)
    print("Optimal weights:", weights) 
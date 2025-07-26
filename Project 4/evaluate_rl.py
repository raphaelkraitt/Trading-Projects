import data_fetcher
from env_trading import CryptoTradingEnv
import config
from stable_baselines3 import PPO
import matplotlib.pyplot as plt
import numpy as np
import os

if __name__ == "__main__":
    # Load data
    df = data_fetcher.load_ohlcv()
    # Load model
    model = PPO.load(config.MODEL_PATH)
    # Evaluate
    episode_profits = []
    for ep in range(config.EVAL_EPISODES):
        env = CryptoTradingEnv(df)
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, _ = env.step(action)
        equity_curve = env.get_equity_curve()
        profit = equity_curve['equity'].iloc[-1] - config.INITIAL_BALANCE
        episode_profits.append(profit)
        print(f"Episode {ep+1}: Profit = ${profit:.2f}")
    # Plot cumulative profit
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(1, config.EVAL_EPISODES+1), np.cumsum(episode_profits), marker='o')
    plt.title('RL Bot Cumulative Profit over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Cumulative Profit ($)')
    plt.grid(True, alpha=0.3)
    if not os.path.exists(config.CHART_SAVE_PATH):
        os.makedirs(config.CHART_SAVE_PATH)
    filename = f"rl_cumulative_profit_{config.SYMBOL.replace('/', '')}.{config.CHART_FORMAT}"
    filepath = os.path.join(config.CHART_SAVE_PATH, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved cumulative profit chart: {filepath}") 
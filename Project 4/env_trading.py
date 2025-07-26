import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
import config

class CryptoTradingEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.window_size = config.WINDOW_SIZE
        self.initial_balance = config.INITIAL_BALANCE
        self.transaction_fee = config.TRANSACTION_FEE
        self.max_position = config.MAX_POSITION
        self.action_space = spaces.Discrete(3)  # 0: Hold, 1: Buy, 2: Sell
        # Observation: window of OHLCV + position + balance
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(self.window_size, 5), dtype=np.float32
        )
        self._reset_env()

    def _reset_env(self):
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.position = 0  # -1: short, 0: flat, 1: long
        self.entry_price = 0
        self.done = False
        self.total_profit = 0
        self.trades = []
        self.equity_curve = []

    def reset(self, seed=None, options=None):
        self._reset_env()
        return self._get_observation(), {}

    def _get_observation(self):
        obs = self.df.iloc[self.current_step - self.window_size:self.current_step][['open', 'high', 'low', 'close', 'volume']].values
        return obs.astype(np.float32)

    def step(self, action):
        if self.done:
            return self._get_observation(), 0, True, False, {}
        price = self.df.iloc[self.current_step]['close']
        reward = 0
        info = {}
        # Action: 0 = Hold, 1 = Buy, 2 = Sell
        if action == 1:  # Buy
            if self.position == 0:
                self.position = 1
                self.entry_price = price
                self.balance -= price * self.max_position * (1 + self.transaction_fee)
                self.trades.append((self.current_step, 'buy', price))
            elif self.position == -1:
                # Close short, open long
                profit = (self.entry_price - price) * self.max_position
                self.balance += profit - price * self.max_position * self.transaction_fee
                self.total_profit += profit
                self.position = 1
                self.entry_price = price
                self.trades.append((self.current_step, 'cover+buy', price))
        elif action == 2:  # Sell
            if self.position == 0:
                self.position = -1
                self.entry_price = price
                self.balance += price * self.max_position * (1 - self.transaction_fee)
                self.trades.append((self.current_step, 'sell', price))
            elif self.position == 1:
                # Close long, open short
                profit = (price - self.entry_price) * self.max_position
                self.balance += profit - price * self.max_position * self.transaction_fee
                self.total_profit += profit
                self.position = -1
                self.entry_price = price
                self.trades.append((self.current_step, 'sell+short', price))
        # Hold: do nothing
        # Calculate reward as change in equity
        equity = self.balance
        if self.position == 1:
            equity += (price - self.entry_price) * self.max_position
        elif self.position == -1:
            equity += (self.entry_price - price) * self.max_position
        reward = equity - (self.equity_curve[-1][1] if self.equity_curve else self.initial_balance)
        self.equity_curve.append((self.current_step, equity))
        # Advance step
        self.current_step += 1
        if self.current_step >= len(self.df):
            self.done = True
        return self._get_observation(), reward, self.done, False, info

    def render(self):
        print(f"Step: {self.current_step}, Balance: {self.balance:.2f}, Position: {self.position}, Equity: {self.equity_curve[-1][1] if self.equity_curve else self.balance:.2f}")

    def get_equity_curve(self):
        return pd.DataFrame(self.equity_curve, columns=['step', 'equity'])

    def get_trades(self):
        return self.trades

if __name__ == "__main__":
    import data_fetcher
    df = data_fetcher.load_ohlcv()
    env = CryptoTradingEnv(df)
    obs, _ = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        obs, reward, done, _, _ = env.step(action)
    print(env.get_equity_curve().tail()) 
import data_fetcher
from env_trading import CryptoTradingEnv
import config
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import os

if __name__ == "__main__":
    # Load data
    df = data_fetcher.load_ohlcv()
    # Create environment
    env = DummyVecEnv([lambda: CryptoTradingEnv(df)])
    # Create RL agent
    model = PPO('MlpPolicy', env, verbose=1)
    # Train
    print(f"Training RL agent for {config.TOTAL_TIMESTEPS} timesteps...")
    model.learn(total_timesteps=config.TOTAL_TIMESTEPS)
    # Save model
    model.save(config.MODEL_PATH)
    print(f"Model saved to {config.MODEL_PATH}") 
# Reinforcement Learning Crypto Bot (ETH/USDT)

A Python bot that uses Stable-Baselines3 to train a reinforcement learning agent to trade ETH/USDT on Binance using historical OHLCV data. The bot maximizes cumulative reward and provides code for training, evaluation, and plotting cumulative profit over episodes.

## 🚀 Features
- Fetches historical ETH/USDT OHLCV data from Binance (via ccxt)
- Custom Gymnasium environment for trading simulation
- Uses Stable-Baselines3 (PPO) for RL agent training
- Simulates trading with transaction fees and position limits
- Plots cumulative profit over evaluation episodes
- All charts saved in the `charts/` directory

## 📋 Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## 🛠️ Installation
1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration
Edit `config.py` to change:
- Trading symbol, exchange, timeframe
- RL environment and training settings
- Chart output directory

## 🎯 Usage
### 1. Fetch Data
```bash
python data_fetcher.py
```

### 2. Train RL Agent
```bash
python train_rl.py
```

### 3. Evaluate RL Agent & Plot Cumulative Profit
```bash
python evaluate_rl.py
```

## 📊 Output
- **Cumulative Profit Chart**: Shows cumulative profit over evaluation episodes
- All charts are saved in the `charts/` directory

## 📝 Example Output
```
Training RL agent for 100000 timesteps...
Model saved to rl_trading_model.zip
Episode 1: Profit = $120.50
Episode 2: Profit = $-45.20
...
Saved cumulative profit chart: charts/rl_cumulative_profit_ETHUSDT.png
```

## 📁 Project Structure
```
Project 4/
├── config.py           # Configuration
├── data_fetcher.py     # Fetches and caches OHLCV data
├── env_trading.py      # Custom RL trading environment
├── train_rl.py         # RL agent training script
├── evaluate_rl.py      # Evaluation and plotting script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── charts/             # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- The RL environment is simplified for demonstration. You can expand it with more features.
- The agent uses PPO by default, but you can try other algorithms from Stable-Baselines3.

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 
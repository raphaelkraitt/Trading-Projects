# AI-Powered Price Prediction Bot (BTC/USDT LSTM)

A Python script using LSTM neural networks to predict the next hour’s closing price of BTC/USDT using historical OHLCV data fetched from Binance. Plots actual vs. predicted prices with error metrics and saves the graph.

## 🚀 Features
- Fetches historical BTC/USDT OHLCV data from Binance (via ccxt)
- Prepares data for LSTM sequence modeling
- Trains a PyTorch LSTM to predict the next hour’s close
- Evaluates and plots actual vs. predicted prices
- Shows error metrics (MSE, MAE, R2)
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
- LSTM model and training settings
- Chart output directory

## 🎯 Usage
### 1. Fetch Data
```bash
python data_fetcher.py
```

### 2. Train LSTM Model
```bash
python train_lstm.py
```

### 3. Evaluate & Plot Predictions
```bash
python evaluate_lstm.py
```

## 📊 Output
- **Prediction Chart**: Actual vs. predicted BTC/USDT prices
- **Error Metrics**: MSE, MAE, R2
- All charts are saved in the `charts/` directory

## 📝 Example Output
```
Training LSTM for 30 epochs...
Epoch 1/30, Loss: 0.002345
...
Model saved to lstm_price_model.pt
Scaler saved to lstm_price_model_scaler.pkl
Test MSE: 120.45
Test MAE: 7.23
Test R2: 0.89
Saved prediction chart: charts/lstm_btcusdt_pred_vs_actual.png
```

## 📁 Project Structure
```
Project 5/
├── config.py           # Configuration
├── data_fetcher.py     # Fetches and caches OHLCV data
├── lstm_model.py       # PyTorch LSTM model
├── train_lstm.py       # LSTM training script
├── evaluate_lstm.py    # Evaluation and plotting script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── charts/             # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- The LSTM model is simple and can be improved with more features or hyperparameter tuning.

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 
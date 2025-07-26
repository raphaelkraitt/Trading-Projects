import data_fetcher
import config
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lstm_model import LSTMPricePredictor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

if __name__ == "__main__":
    # Load data
    df = data_fetcher.load_ohlcv()
    features = ['open', 'high', 'low', 'close', 'volume']
    data = df[features].values
    scaler = joblib.load(config.MODEL_PATH.replace('.pt', '_scaler.pkl'))
    data_scaled = scaler.transform(data)
    # Create sequences
    def create_sequences(data, seq_len):
        xs, ys = [], []
        for i in range(len(data) - seq_len):
            x = data[i:i+seq_len]
            y = data[i+seq_len, 3]  # Predict next close
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)
    X, y = create_sequences(data_scaled, config.SEQ_LEN)
    # Only use test set
    split = int(len(X) * config.TRAIN_TEST_SPLIT)
    X_test, y_test = X[split:], y[split:]
    X_test = torch.tensor(X_test, dtype=torch.float32)
    # Load model
    model = LSTMPricePredictor(
        input_size=len(features),
        hidden_size=config.HIDDEN_SIZE,
        num_layers=config.NUM_LAYERS
    )
    model.load_state_dict(torch.load(config.MODEL_PATH))
    model.eval()
    # Predict
    with torch.no_grad():
        y_pred = model(X_test).squeeze().numpy()
    # Inverse scale
    y_test_full = np.zeros((len(y_test), len(features)))
    y_pred_full = np.zeros((len(y_pred), len(features)))
    y_test_full[:, 3] = y_test
    y_pred_full[:, 3] = y_pred
    y_test_inv = scaler.inverse_transform(y_test_full)[:, 3]
    y_pred_inv = scaler.inverse_transform(y_pred_full)[:, 3]
    # Metrics
    mse = mean_squared_error(y_test_inv, y_pred_inv)
    mae = mean_absolute_error(y_test_inv, y_pred_inv)
    r2 = r2_score(y_test_inv, y_pred_inv)
    print(f"Test MSE: {mse:.4f}")
    print(f"Test MAE: {mae:.4f}")
    print(f"Test R2: {r2:.4f}")
    # Plot
    plt.figure(figsize=(14, 7))
    plt.plot(y_test_inv, label='Actual', color='black')
    plt.plot(y_pred_inv, label='Predicted', color='blue', alpha=0.7)
    plt.title('BTC/USDT Price Prediction (LSTM)')
    plt.xlabel('Test Sample')
    plt.ylabel('Price (USDT)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    if not os.path.exists(config.CHART_SAVE_PATH):
        os.makedirs(config.CHART_SAVE_PATH)
    filename = f"lstm_btcusdt_pred_vs_actual.{config.CHART_FORMAT}"
    filepath = os.path.join(config.CHART_SAVE_PATH, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved prediction chart: {filepath}") 
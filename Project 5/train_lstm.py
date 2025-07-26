import data_fetcher
import config
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from lstm_model import LSTMPricePredictor
import os

def create_sequences(data, seq_len):
    xs, ys = [], []
    for i in range(len(data) - seq_len):
        x = data[i:i+seq_len]
        y = data[i+seq_len, 3]  # Predict next close
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

if __name__ == "__main__":
    # Load data
    df = data_fetcher.load_ohlcv()
    features = ['open', 'high', 'low', 'close', 'volume']
    data = df[features].values
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    # Create sequences
    X, y = create_sequences(data_scaled, config.SEQ_LEN)
    # Train/test split
    split = int(len(X) * config.TRAIN_TEST_SPLIT)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    # Convert to tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)
    # Model
    model = LSTMPricePredictor(
        input_size=len(features),
        hidden_size=config.HIDDEN_SIZE,
        num_layers=config.NUM_LAYERS
    )
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    # Training loop
    print(f"Training LSTM for {config.EPOCHS} epochs...")
    for epoch in range(config.EPOCHS):
        model.train()
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        if (epoch+1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch+1}/{config.EPOCHS}, Loss: {loss.item():.6f}")
    # Save model
    torch.save(model.state_dict(), config.MODEL_PATH)
    print(f"Model saved to {config.MODEL_PATH}")
    # Save scaler
    scaler_path = config.MODEL_PATH.replace('.pt', '_scaler.pkl')
    import joblib
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}") 
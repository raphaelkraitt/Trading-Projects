import torch
import torch.nn as nn

class LSTMPricePredictor(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # Take last output
        out = self.fc(out)
        return out

if __name__ == "__main__":
    model = LSTMPricePredictor(input_size=5, hidden_size=64, num_layers=2)
    x = torch.randn(8, 48, 5)
    y = model(x)
    print(y.shape) 
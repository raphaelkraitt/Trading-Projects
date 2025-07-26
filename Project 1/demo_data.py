import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_demo_data():
    """
    Generate demo OHLCV data for testing purposes
    
    Returns:
        dict: Dictionary with demo data for different exchanges
    """
    print("📊 Generating demo data...")
    
    # Base price and parameters
    base_price = 45000  # Starting BTC price
    volatility = 0.02   # 2% daily volatility
    trend = 0.001       # Slight upward trend
    
    # Generate timestamps (last 500 hours)
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=500)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='1H')
    
    demo_data = {}
    
    # Generate data for each exchange with slight variations
    exchanges = ['binance', 'mexc']
    
    for exchange in exchanges:
        # Add some randomness to make exchanges slightly different
        exchange_volatility = volatility * (1 + random.uniform(-0.1, 0.1))
        exchange_trend = trend * (1 + random.uniform(-0.2, 0.2))
        
        # Generate price series
        prices = []
        current_price = base_price * (1 + random.uniform(-0.05, 0.05))
        
        for i in range(len(timestamps)):
            # Add trend and random walk
            price_change = (exchange_trend + 
                          random.normalvariate(0, exchange_volatility / 24))
            current_price *= (1 + price_change)
            
            # Generate OHLCV data
            high = current_price * (1 + abs(random.normalvariate(0, 0.005)))
            low = current_price * (1 - abs(random.normalvariate(0, 0.005)))
            open_price = current_price * (1 + random.normalvariate(0, 0.002))
            close_price = current_price * (1 + random.normalvariate(0, 0.002))
            volume = random.uniform(100, 1000) * current_price / 1000
            
            prices.append({
                'open': max(open_price, low),
                'high': max(high, open_price, close_price),
                'low': min(low, open_price, close_price),
                'close': close_price,
                'volume': volume
            })
        
        # Create DataFrame
        df = pd.DataFrame(prices, index=timestamps)
        demo_data[exchange] = df
        
        print(f"✓ Generated {len(df)} demo candles for {exchange}")
    
    return demo_data

def generate_realistic_btc_data():
    """
    Generate more realistic BTC price data based on historical patterns
    
    Returns:
        dict: Dictionary with realistic demo data
    """
    print("📊 Generating realistic BTC demo data...")
    
    # Historical BTC price patterns (simplified)
    base_price = 45000
    timestamps = pd.date_range(
        start=datetime.now() - timedelta(hours=500),
        end=datetime.now(),
        freq='1H'
    )
    
    demo_data = {}
    exchanges = ['binance', 'mexc']
    
    for exchange in exchanges:
        # Generate realistic price movement
        np.random.seed(hash(exchange) % 1000)  # Different seed for each exchange
        
        # Create price series with realistic patterns
        returns = np.random.normal(0.0001, 0.015, len(timestamps))  # 1.5% hourly volatility
        
        # Add some trend and mean reversion
        for i in range(1, len(returns)):
            # Add slight mean reversion
            if i > 20:
                mean_return = np.mean(returns[i-20:i])
                returns[i] += (0 - mean_return) * 0.1
            
            # Add occasional larger moves
            if random.random() < 0.05:  # 5% chance of larger move
                returns[i] *= random.uniform(1.5, 2.5)
        
        # Convert returns to prices
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Generate OHLCV data
        ohlcv_data = []
        for i, price in enumerate(prices):
            # Create realistic OHLCV from price
            base = price
            high = base * (1 + abs(random.normalvariate(0, 0.008)))
            low = base * (1 - abs(random.normalvariate(0, 0.008)))
            open_price = base * (1 + random.normalvariate(0, 0.003))
            close_price = base * (1 + random.normalvariate(0, 0.003))
            
            # Ensure OHLC relationship
            high = max(high, open_price, close_price)
            low = min(low, open_price, close_price)
            
            # Volume based on price movement
            price_change = abs(close_price - open_price) / open_price
            volume = random.uniform(50, 200) * (1 + price_change * 10)
            
            ohlcv_data.append({
                'open': open_price,
                'high': high,
                'low': low,
                'close': close_price,
                'volume': volume
            })
        
        df = pd.DataFrame(ohlcv_data, index=timestamps)
        demo_data[exchange] = df
        
        print(f"✓ Generated {len(df)} realistic candles for {exchange}")
    
    return demo_data

if __name__ == "__main__":
    # Test the demo data generation
    data = generate_realistic_btc_data()
    
    for exchange, df in data.items():
        print(f"\n{exchange.upper()} Data Summary:")
        print(f"  Shape: {df.shape}")
        print(f"  Date Range: {df.index[0]} to {df.index[-1]}")
        print(f"  Price Range: ${df['low'].min():.2f} - ${df['high'].max():.2f}")
        print(f"  Current Price: ${df['close'].iloc[-1]:.2f}") 
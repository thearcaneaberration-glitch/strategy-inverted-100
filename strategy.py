import numpy as np
import pandas as pd
import os
from cpz.clients.sync import CPZClient

# Define the SYMBOLS list at module level
SYMBOLS = ['SPY', 'QQQ', 'AAPL']

# Helper function to initialize the CPZ client
def initialize_client():
    # Retrieve the strategy ID from environment variables
    strategy_id = os.environ["CPZ_AI_API_STRATEGY_ID"]
    # Initialize the CPZ client
    client = CPZClient()
    # Use the Alpaca broker in paper environment
    client.execution.use_broker("alpaca", environment="paper")
    return client, strategy_id

# Helper function to calculate mean reversion signals
def calculate_mean_reversion_signals(data):
    signals = {}
    for symbol, df in data.items():
        # Calculate the 20-day moving average
        df['20_day_ma'] = df['close'].rolling(window=20).mean()
        # Calculate the z-score
        df['z_score'] = (df['close'] - df['20_day_ma']) / df['close'].rolling(window=20).std()
        # Generate signals: short when z-score > 1.5, cover when z-score < 0.5
        signals[symbol] = np.where(df['z_score'] > 1.5, -1, np.where(df['z_score'] < 0.5, 0, np.nan))
    return signals

# Main function to generate signals
def generate_signals(current_data, state, **kwargs):
    # Calculate signals using the helper function
    signals = calculate_mean_reversion_signals(current_data)
    weights = {}
    for symbol in SYMBOLS:
        if symbol in signals:
            # Assign weights based on signals
            weights[symbol] = signals[symbol][-1] if not np.isnan(signals[symbol][-1]) else 0
    return weights

# Function to run the strategy for live execution
def run_strategy():
    # Initialize the client and strategy ID
    client, strategy_id = initialize_client()
    # Retrieve current market data
    current_data = {symbol: client.market_data.get_bars(symbol, timeframe="1Day", limit=20) for symbol in SYMBOLS}
    # Generate signals
    weights = generate_signals(current_data, state={})
    # Place orders based on generated signals
    for symbol, weight in weights.items():
        if weight != 0:
            side = "sell" if weight < 0 else "buy"
            qty = abs(weight) * 100  # Example quantity calculation
            try:
                # Place the order using CPZ client
                order = client.execution.order(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    order_type="market",
                    time_in_force="day",
                    strategy_id=strategy_id
                )
                print(order.model_dump_json())
            except Exception as e:
                print("Error placing order for %s: %s" % (symbol, str(e)))

# Ensure the module can be imported without executing any code
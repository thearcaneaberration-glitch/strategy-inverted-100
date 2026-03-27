<p align="left">
  <a href="https://ai.cpz-lab.com/">
    <img src="https://drive.google.com/uc?id=1JY-PoPj9GHmpq3bZLC7WyJLbGuT1L3hN" alt="CPZ Lab" width="150">
  </a>
</p>

# Inverted 100 - Strategy Methodology

> *Generated with [CPZAI](https://ai.cpz-lab.com/)*

## Mean_reversion Trading Strategy

| Attribute | Value |
|-----------|-------|
| **Strategy Type** | Mean_reversion |
| **Universe** | SPY, QQQ, AAPL |
| **Implementation Date** | 3/27/2026 |
| **Status** | Development |

---

## Strategy Overview

The same as 100, except for short selling instead of buying

### Instruments Traded

- **SPY**
- **QQQ**
- **AAPL**

### Technical Indicators Used

- Relative Strength Index (RSI)
- Mean Reversion

---


## Research Hypothesis

**Primary Hypothesis (H₁)**: Asset prices that deviate significantly from their long-term equilibrium values will exhibit predictable reversion patterns, driven by market inefficiencies and behavioral overreaction.

---


## Theoretical Framework

### Efficient Market Hypothesis Violations
The mean reversion anomaly represents a systematic violation of the weak-form efficient market hypothesis.

---


## Research Methodology

### Phase I: Equilibrium Definition & Calculation
**Statistical Mean Anchors**: Simple Moving Average, EWMA, Bollinger Bands

---

## Implementation Details

### Signal Generation Implementation

The core signal generation logic from `strategy.py`:

```python
def generate_signals(current_data, state, **kwargs):
    # Calculate signals using the helper function
    signals = calculate_mean_reversion_signals(current_data)
    weights = {}
    for symbol in SYMBOLS:
        if symbol in signals:
            # Assign weights based on signals
            weights[symbol] = signals[symbol][-1] if not np.isnan(signals[symbol][-1]) else 0
    return weights

```

### Execution Architecture

Orders are executed via CPZAI Platform with the following flow:

```
strategy.py                    backtest.py
    │                              │
    ├── generate_signals()  ◄──────┤ imports from strategy
    ├── initialize_client()        │
    └── run_strategy()             └── StrategyWrapper (Backtrader)
         │
         ▼
    CPZAI Platform
         │
         ▼
    Broker (Alpaca, etc.)
```

### Order Execution

```python
from cpz.clients.sync import CPZClient

def initialize_client():
    client = CPZClient()
    client.execution.use_broker("alpaca", environment="paper")
    return client

def execute_order(symbol, qty, side):
    client = initialize_client()
    order = client.execution.order(
        symbol=symbol,
        qty=qty,
        side=side,
        order_type="market",
        time_in_force="day",
        strategy_id=os.environ["CPZ_AI_API_STRATEGY_ID"]
    )
    return order
```

---

## Backtesting Framework

### Validation Process

- **Historical Analysis**: Multiple years of market data for SPY, QQQ, AAPL
- **Walk-Forward Testing**: Rolling optimization with out-of-sample validation
- **Transaction Costs**: Realistic slippage (5 bps) and commission (3 bps) modeling
- **Benchmark Comparison**: Performance vs SPY buy-and-hold

### Key Metrics Tracked

| Metric | Description |
|--------|-------------|
| Total Return | Cumulative strategy return |
| Annualized Return | CAGR |
| Sharpe Ratio | Risk-adjusted return |
| Maximum Drawdown | Largest peak-to-trough decline |
| Win Rate | Percentage of profitable trades |
| Alpha | Excess return vs benchmark |

---


## Risk Assessment & Critical Limitations

### **TRENDING MARKET RISK** 🔴
Strategy exhibits poor performance during sustained directional markets

---


## Performance Monitoring Framework

| **Metric** | **Target Range** | **Calculation** |
|------------|------------------|----------------|
| **Mean Reversion Speed** | 5-20 days | Half-life calculation |

---


## Data Infrastructure Requirements

| **Data Category** | **Frequency** | **Provider Options** |
|-------------------|---------------|---------------------|
| **High-Frequency Prices** | Minute/Tick | Bloomberg, Refinitiv |

---

## Risk Management

### Risk Controls

- Position size limits per instrument
- Maximum portfolio concentration limits
- Stop-loss mechanisms
- Volatility targeting
- Drawdown limits
- Sector concentration limits

### Performance Monitoring

- Real-time P&L tracking
- Risk metric calculations
- Performance attribution
- Automated alerts for limit breaches

---

## Academic References

*Add relevant academic papers and research that support your strategy's methodology:*

1. *[Author(s), Year. "Paper Title." Journal Name, Volume(Issue), Pages.]*
2. *[Author(s), Year. "Paper Title." Journal Name, Volume(Issue), Pages.]*
3. *[Author(s), Year. "Paper Title." Journal Name, Volume(Issue), Pages.]*

---

## Legal Disclaimer

**IMPORTANT**: This software is for educational and research purposes only. Past performance does not guarantee future results. Trading involves substantial risk of loss and is not suitable for all investors.

### Risk Warnings

- You may lose some or all of your invested capital
- Quantitative models may fail during market stress
- Execution timing and slippage may impact returns
- Regulatory requirements may affect implementation
- No guarantee of profitability or risk control

---

*Last Updated: 3/27/2026 | Version: 1.0.0*

---

*Built with [CPZAI Platform](https://ai.cpz-lab.com/)*
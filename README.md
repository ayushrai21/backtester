# Quantitative Research & Backtesting Platform

A modular Python-based platform for researching, backtesting, optimizing, and comparing algorithmic trading strategies on historical stock market data.

## Overview

This project was developed to simulate and evaluate trading strategies using historical market data. The platform supports multiple technical indicators, strategy benchmarking, parameter optimization, portfolio performance analysis, and interactive visualization through a Streamlit dashboard.

The architecture is designed to be modular, allowing new indicators and strategies to be added with minimal code changes.

---

## Features

### Data Management

* Historical market data retrieval using Yahoo Finance
* Local data caching for faster analysis
* Multi-ticker support

### Technical Indicators

* Simple Moving Average (SMA)
* Exponential Moving Average (EMA)
* Relative Strength Index (RSI)
* MACD
* Bollinger Bands

### Trading Strategies

* SMA Crossover Strategy
* EMA Crossover Strategy
* RSI Strategy
* MACD Strategy
* Bollinger Band Strategy
* Price Above SMA Strategy

### Backtesting Engine

* Signal generation and trade execution
* Cash and position tracking
* Portfolio equity curve generation
* Trade logging

### Performance Analytics

* Total Return
* Win Rate
* Profit Factor
* Sharpe Ratio
* Maximum Drawdown

### Research Tools

* Strategy comparison framework
* Multi-ticker analysis
* Parameter optimization for strategy tuning
* Buy-and-hold benchmark comparison

### Visualization

* Portfolio performance charts
* Strategy comparison plots
* Optimization result visualizations
* Interactive Streamlit dashboard

---

## Project Structure

```text
BackTester/
│
├── src/
│   ├── backtester.py
│   ├── benchmark.py
│   ├── data_loader.py
│   ├── indicators.py
│   ├── metrics.py
│   ├── reporting.py
│   ├── strategies.py
│   └── visualization.py
│
├── app.py
├── main.py
├── compare_strategies.py
├── multi_ticker_test.py
├── parameter_optimization.py
│
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone <repository-url>
cd BackTester

pip install -r requirements.txt
```

---

## Usage

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

Run a backtest:

```bash
python main.py
```

Compare strategies:

```bash
python compare_strategies.py
```

Run multi-ticker analysis:

```bash
python multi_ticker_test.py
```

Optimize strategy parameters:

```bash
python parameter_optimization.py
```

---

## Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Streamlit
* Yahoo Finance API (yfinance)

---

## Author

Ayush Rai
B.Tech Electrical Engineering, IIT Madras

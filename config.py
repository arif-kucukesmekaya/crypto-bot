import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Exchange settings
EXCHANGE = "binance"
SYMBOL = "BTC/USDT"  # Default symbol, will be updated from UI
TIMEFRAME = "1h"     # Default timeframe, will be updated from UI

# API credentials (to be set in .env file)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Technical Analysis Parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Telegram settings (to be set in .env file)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Trading parameters
TRADE_AMOUNT = 100  # USDT
STOP_LOSS_PERCENTAGE = 2
TAKE_PROFIT_PERCENTAGE = 4

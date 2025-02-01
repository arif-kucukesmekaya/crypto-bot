import ccxt
import pandas as pd
from config import API_KEY, API_SECRET, EXCHANGE, TIMEFRAME

class DataFetcher:
    def __init__(self):
        self.exchange = getattr(ccxt, EXCHANGE)({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'enableRateLimit': True,
            'timeout': 30000,  # Increase timeout to 30 seconds
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        })
        
        # Common name mappings for popular cryptocurrencies
        self.common_names = {
            'BTC': 'Bitcoin',
            'ETH': 'Ethereum',
            'BNB': 'Binance Coin',
            'XRP': 'Ripple',
            'SOL': 'Solana',
            'ADA': 'Cardano',
            'DOGE': 'Dogecoin',
            'DOT': 'Polkadot',
            'MATIC': 'Polygon',
            'LINK': 'Chainlink',
            'AVAX': 'Avalanche',
            'UNI': 'Uniswap',
            'ATOM': 'Cosmos',
            'LTC': 'Litecoin',
            'OP': 'Optimism',
            'ARB': 'Arbitrum'
        }

    def get_all_trading_pairs(self):
        """Get all available trading pairs from Binance"""
        try:
            markets = self.exchange.load_markets()
            # Filter for USDT pairs and sort them
            usdt_pairs = [
                symbol for symbol, market in markets.items()
                if symbol.endswith('/USDT') and market.get('active', False)
            ]
            return sorted(usdt_pairs)
        except Exception as e:
            print(f"Error fetching trading pairs: {e}")
            return ["BTC/USDT", "ETH/USDT", "BNB/USDT"]  # Default pairs if error

    def fetch_ohlcv(self, symbol="BTC/USDT", limit=100):
        """Fetch OHLCV (Open, High, Low, Close, Volume) data"""
        try:
            # Fetch with retry
            for _ in range(3):  # Try up to 3 times
                try:
                    ohlcv = self.exchange.fetch_ohlcv(symbol, TIMEFRAME, limit=limit)
                    if ohlcv and len(ohlcv) > 0:
                        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                        df.set_index('timestamp', inplace=True)
                        return df
                except Exception as e:
                    print(f"Retry after error: {e}")
                    continue
            return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def get_current_price(self, symbol="BTC/USDT"):
        """Get current price of the trading pair"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"Error fetching current price: {e}")
            return None

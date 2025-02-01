import asyncio
import time
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from strategy import TradingStrategy
from notifier import Notifier

async def main():
    # Initialize components
    data_fetcher = DataFetcher()
    notifier = Notifier()
    
    print("Crypto Trading Bot Started!")
    print("Monitoring market and sending signals via Telegram...")
    
    while True:
        try:
            # Fetch latest market data
            df = data_fetcher.fetch_ohlcv()
            if df is not None:
                # Add technical indicators
                df = TechnicalIndicators.add_indicators(df)
                
                # Generate trading signals
                signal_data = TradingStrategy.generate_signals(df)
                
                # Send signal notification
                if signal_data['signal'] != "NEUTRAL":
                    await notifier.send_signal(signal_data)
            
            # Wait for 5 minutes before next analysis
            await asyncio.sleep(300)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

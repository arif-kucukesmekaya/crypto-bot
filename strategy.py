from config import RSI_OVERBOUGHT, RSI_OVERSOLD

class TradingStrategy:
    @staticmethod
    def generate_signals(df):
        """Generate trading signals based on technical indicators"""
        signals = []
        
        # Get the latest data point
        latest = df.iloc[-1]
        
        # Initialize signal strength and reasons
        signal_strength = 0
        reasons = []
        
        # RSI Analysis
        if latest['rsi'] < RSI_OVERSOLD:
            signal_strength += 1
            reasons.append(f"RSI oversold ({latest['rsi']:.2f})")
        elif latest['rsi'] > RSI_OVERBOUGHT:
            signal_strength -= 1
            reasons.append(f"RSI overbought ({latest['rsi']:.2f})")
        
        # MACD Analysis
        if latest['macd'] > latest['macd_signal']:
            signal_strength += 1
            reasons.append("MACD crossed above signal line")
        elif latest['macd'] < latest['macd_signal']:
            signal_strength -= 1
            reasons.append("MACD crossed below signal line")
        
        # Moving Average Analysis
        if latest['close'] > latest['sma_50'] > latest['sma_200']:
            signal_strength += 1
            reasons.append("Price above both MAs, bullish trend")
        elif latest['close'] < latest['sma_50'] < latest['sma_200']:
            signal_strength -= 1
            reasons.append("Price below both MAs, bearish trend")
        
        # Bollinger Bands Analysis
        if latest['close'] < latest['bb_lower']:
            signal_strength += 1
            reasons.append("Price below lower Bollinger Band, potential bounce")
        elif latest['close'] > latest['bb_upper']:
            signal_strength -= 1
            reasons.append("Price above upper Bollinger Band, potential reversal")
        
        # Generate final signal
        if signal_strength >= 2:
            signal = "STRONG BUY"
        elif signal_strength == 1:
            signal = "BUY"
        elif signal_strength == 0:
            signal = "NEUTRAL"
        elif signal_strength == -1:
            signal = "SELL"
        else:
            signal = "STRONG SELL"
        
        return {
            'signal': signal,
            'strength': signal_strength,
            'reasons': reasons,
            'price': latest['close']
        }

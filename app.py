import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from strategy import TradingStrategy
from config import SYMBOL

# Page config
st.set_page_config(page_title="Crypto Trading Bot", layout="wide")

# Initialize components
@st.cache_resource
def get_data_fetcher():
    return DataFetcher()

data_fetcher = get_data_fetcher()

# Get all trading pairs
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_trading_pairs():
    return data_fetcher.get_all_trading_pairs()

trading_pairs = get_trading_pairs()

st.title("🤖 Crypto Trading Bot")

# Sidebar controls
st.sidebar.header("Settings")

# Create a dictionary of symbols and their descriptions
symbol_descriptions = {}
formatted_options = []
for pair in trading_pairs:
    symbol = pair.split('/')[0]
    if symbol in data_fetcher.common_names:
        desc = f"{symbol} ({data_fetcher.common_names[symbol]})"
        symbol_descriptions[pair] = desc
        formatted_options.append(desc)
    else:
        symbol_descriptions[pair] = symbol
        formatted_options.append(symbol)

# Search box for quick search
st.sidebar.subheader("Quick Search")
search_container = st.sidebar.container()
search_term = search_container.text_input("Search Trading Pair", "").upper()

# Show all pairs in a selectbox
st.sidebar.subheader("All Trading Pairs")
selected_option = st.sidebar.selectbox(
    "Select from all pairs",
    formatted_options,
    index=formatted_options.index("BTC (Bitcoin)") if "BTC (Bitcoin)" in formatted_options else 0
)

# Process search results if there's a search term
if search_term:
    filtered_pairs = []
    suggestions = []
    
    for pair in trading_pairs:
        symbol = pair.split('/')[0]
        if symbol.startswith(search_term):
            filtered_pairs.append(pair)
            if symbol in data_fetcher.common_names:
                suggestions.append(f"{symbol} ({data_fetcher.common_names[symbol]})")
            else:
                suggestions.append(symbol)
    
    # Show suggestions in a radio group
    if suggestions:
        st.sidebar.markdown("**Search Results:**")
        selected_suggestion = search_container.radio(
            "Suggestions",
            suggestions,
            label_visibility="collapsed"
        )
        # Extract symbol from selection
        selected_symbol = selected_suggestion.split(' (')[0]
        # Find the corresponding pair
        coin_pair = next(pair for pair in filtered_pairs if pair.startswith(selected_symbol))
    else:
        # If no search results, use the selected option from dropdown
        selected_symbol = selected_option.split(' (')[0]
        coin_pair = next(pair for pair in trading_pairs if pair.startswith(selected_symbol))
else:
    # Use the selected option from dropdown
    selected_symbol = selected_option.split(' (')[0]
    coin_pair = next(pair for pair in trading_pairs if pair.startswith(selected_symbol))

# Show timeframe selection
timeframe = st.sidebar.selectbox("Timeframe", ["1h", "4h", "1d"], index=0)

# Display total number of pairs
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Trading Pairs:** {len(trading_pairs)}")
if search_term and suggestions:
    st.sidebar.markdown(f"**Found Pairs:** {len(suggestions)}")

# Main content
st.header(f"📊 {coin_pair} Analysis")

# Add refresh button
col1, col2 = st.columns([2, 1])
with col1:
    refresh = st.button("🔄 Refresh Data")

def create_candlestick_chart(df):
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="OHLC"
    ))
    
    # Add RSI
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['rsi'],
        name="RSI",
        yaxis="y2"
    ))
    
    # Add MACD
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['macd'],
        name="MACD",
        yaxis="y3"
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['macd_signal'],
        name="Signal",
        yaxis="y3"
    ))
    
    # Update layout with title including coin pair
    fig.update_layout(
        title=f"{coin_pair} - OHLCV Chart",
        yaxis2=dict(
            title="RSI",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        yaxis3=dict(
            title="MACD",
            overlaying="y",
            side="right",
            anchor="free",
            position=0.95
        ),
        height=600
    )
    
    return fig

def format_signal_message(signal_data):
    color = {
        "STRONG BUY": "🟢",
        "BUY": "🟩",
        "NEUTRAL": "⬜",
        "SELL": "🟨",
        "STRONG SELL": "🔴"
    }
    
    message = f"**Trading Pair:** {coin_pair}  \n\n"
    message += f"{color[signal_data['signal']]} **Signal:** {signal_data['signal']}  \n"
    message += f"**Price:** ${signal_data['price']:.2f}  \n"
    message += f"**Signal Strength:** {signal_data['strength']}  \n\n"
    message += "**Analysis:**  \n"
    for reason in signal_data['reasons']:
        message += f"- {reason}  \n"
    
    return message

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Price Chart & Indicators")
    chart_placeholder = st.empty()

with col2:
    st.subheader("Trading Signals")
    signal_placeholder = st.empty()

# Time display
time_placeholder = st.empty()

# Fetch and display data
try:
    df = data_fetcher.fetch_ohlcv(symbol=coin_pair)
    if df is not None:
        # Add indicators
        df = TechnicalIndicators.add_indicators(df)
        
        # Generate trading signals
        signal_data = TradingStrategy.generate_signals(df)
        
        # Update chart
        fig = create_candlestick_chart(df)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Update signal
        signal_placeholder.markdown(format_signal_message(signal_data))
        
        # Update time
        time_placeholder.text(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.error("Unable to fetch data. Please try again.")
        
except Exception as e:
    st.error(f"Error: {str(e)}")
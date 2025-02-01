import telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SYMBOL

class Notifier:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID

    async def send_signal(self, signal_data):
        """Send trading signal via Telegram"""
        message = self._format_signal_message(signal_data)
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Error sending telegram message: {e}")

    def _format_signal_message(self, signal_data):
        """Format the signal message"""
        message = f"🚨 *Trading Signal Alert* 🚨\n\n"
        message += f"*Symbol:* {SYMBOL}\n"
        message += f"*Signal:* {signal_data['signal']}\n"
        message += f"*Current Price:* ${signal_data['price']:.2f}\n\n"
        
        message += "*Analysis:*\n"
        for reason in signal_data['reasons']:
            message += f"• {reason}\n"
        
        message += f"\n*Signal Strength:* {signal_data['strength']}"
        
        return message

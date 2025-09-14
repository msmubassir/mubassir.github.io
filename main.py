from flask import Flask, render_template, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

class TelegramBot:
    def __init__(self, token):
        self.url = f"https://api.telegram.org/bot{token}"
        self.chats = {
            '8363437161': 'First Panel',
            '7302607235': 'Second Panel',
            '7931424304': 'Third Panel',
            '6294979663': 'Panel Controller'
        }

    def send_message(self, chat_id, msg):
        try:
            r = requests.post(f"{self.url}/sendMessage",
                              data={'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'})
            return r.json().get('ok', False)
        except:
            return False

    def send_all(self, msg):
        results = {}
        for chat_id, fname in self.chats.items():
            success = self.send_message(chat_id, msg)
            results[chat_id] = {
                'name': fname,
                'status': '✅ Success' if success else '❌ Failed'
            }
        return results

# Initialize bot
bot = TelegramBot("7991180155:AAGAZrXIm-EFKm7EQd4DaA2uQfDI_9H5Pro")

@app.route('/')
def index():
    return render_template('index.html', chats=bot.chats)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    selected_chats = data.get('chats', [])
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    if not selected_chats:
        return jsonify({'error': 'No chats selected'}), 400
    
    results = {}
    
    if 'all' in selected_chats:
        # Send to all chats
        results = bot.send_all(message)
    else:
        # Send to selected chats only
        for chat_id in selected_chats:
            if chat_id in bot.chats:
                success = bot.send_message(chat_id, message)
                results[chat_id] = {
                    'name': bot.chats[chat_id],
                    'status': '✅ Success' if success else '❌ Failed'
                }
    
    return jsonify({'results': results})

def start_bot():
    """Background task for bot maintenance (if needed)"""
    print("Bot started in background...")
    # You can add periodic tasks here if needed

if __name__ == '__main__':
    PORT = 5000
    # Start bot in background thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    app.run(host='0.0.0.0', port=PORT, debug=True)

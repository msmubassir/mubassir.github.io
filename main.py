
import requests
import os
import subprocess
import json
from pathlib import Path

class WebDeployer:
    def __init__(self, telegram_bot_token=None, telegram_chat_id=None):
        self.telegram_bot_token = telegram_bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = telegram_chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
    def build_web_app(self, base_url="/mubassir.github.io"):
        """Build the Flet web application"""
        try:
            print("Building web application...")
            result = subprocess.run([
                'flet', 'build', 'web',
                '--base-url', base_url,
                '--route-url-strategy', 'hash'
            ], capture_output=True, text=True, check=True)
            
            print("Build completed successfully!")
            print(result.stdout)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")
            print(f"Error output: {e.stderr}")
            self.send_telegram_message(f"❌ Build failed: {e.stderr}")
            return False
    
    def deploy_to_github_pages(self):
        """Deploy to GitHub Pages (this would typically be handled by GitHub Actions)"""
        print("Deployment to GitHub Pages should be handled by GitHub Actions workflow.")
        print("Make sure your repository has GitHub Pages enabled in settings.")
        
    def send_telegram_message(self, message):
        """Send message via Telegram bot"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            print("Telegram bot token or chat ID not configured")
            return False
        
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Telegram message sent successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Telegram message: {e}")
            return False
    
    def run_deployment_pipeline(self):
        """Run complete deployment pipeline"""
        # Send start notification
        self.send_telegram_message("🚀 Starting deployment process...")
        
        # Build the application
        if self.build_web_app():
            # Send success notification
            self.send_telegram_message("✅ Build completed successfully!\n\n"
                                     "📦 Deployment to GitHub Pages will be handled automatically "
                                     "by GitHub Actions workflow.\n\n"
                                     "🌐 Site URL: https://msmubassir.github.io/")
            
            print("Deployment process completed!")
            print("Site will be available at: https://msmubassir.github.io/")
        else:
            # Send failure notification
            self.send_telegram_message("❌ Deployment failed! Check GitHub Actions logs for details.")

def main():
    # Initialize deployer (you can pass Telegram credentials here or set as environment variables)
    deployer = WebDeployer()
    
    # Run deployment pipeline
    deployer.run_deployment_pipeline()

if __name__ == "__main__":
    main()

"""
host.py - Flask wrapper for your existing telegram bot
Keep this in the same directory as your bot.py
Uptime Robot will ping /health every 5 minutes
"""

from flask import Flask, jsonify, request
import threading
import time
import subprocess
import os
import sys
import signal
import logging
import atexit

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
bot_process = None
bot_thread = None
bot_restart_count = 0
MAX_RESTARTS = 10
BOT_FILE = "bot.py"  # Your existing bot file
PORT = 5000

class BotManager:
    """Manages the bot process"""
    
    def __init__(self):
        self.process = None
        self.is_running = False
        self.last_restart = time.time()
        
    def start_bot(self):
        """Start the bot.py process"""
        global bot_restart_count
        
        if self.process and self.process.poll() is None:
            logger.info("Bot is already running")
            return True
            
        try:
            logger.info(f"Starting bot from {BOT_FILE}...")
            
            # Start bot process
            self.process = subprocess.Popen(
                [sys.executable, BOT_FILE],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.is_running = True
            bot_restart_count += 1
            
            # Start output reader thread
            threading.Thread(target=self.read_output, daemon=True).start()
            
            # Start monitor thread
            threading.Thread(target=self.monitor_bot, daemon=True).start()
            
            logger.info(f"Bot started successfully (PID: {self.process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            self.is_running = False
            return False
    
    def read_output(self):
        """Read and log bot output"""
        if self.process:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    logger.info(f"BOT: {line.strip()}")
    
    def monitor_bot(self):
        """Monitor bot process and restart if needed"""
        while self.is_running:
            time.sleep(10)  # Check every 10 seconds
            
            if self.process and self.process.poll() is not None:
                logger.warning("Bot process died! Attempting restart...")
                self.restart_bot()
    
    def restart_bot(self):
        """Restart the bot process"""
        global bot_restart_count
        
        if bot_restart_count >= MAX_RESTARTS:
            logger.error(f"Max restart attempts ({MAX_RESTARTS}) reached!")
            return False
        
        self.stop_bot()
        time.sleep(2)  # Wait before restart
        return self.start_bot()
    
    def stop_bot(self):
        """Stop the bot process"""
        if self.process:
            logger.info(f"Stopping bot process (PID: {self.process.pid})...")
            
            try:
                # Try graceful termination
                if os.name == 'nt':  # Windows
                    self.process.terminate()
                else:  # Unix/Linux/Mac
                    os.kill(self.process.pid, signal.SIGTERM)
                
                # Wait for termination
                self.process.wait(timeout=10)
                logger.info("Bot stopped gracefully")
                
            except subprocess.TimeoutExpired:
                logger.warning("Force killing bot process...")
                self.process.kill()
                self.process.wait()
                
            except Exception as e:
                logger.error(f"Error stopping bot: {e}")
            
            self.process = None
            self.is_running = False
    
    def get_status(self):
        """Get bot status"""
        status = {
            "running": self.is_running,
            "pid": self.process.pid if self.process else None,
            "exit_code": self.process.poll() if self.process else None,
            "restart_count": bot_restart_count,
            "uptime": time.time() - self.last_restart if self.last_restart else 0
        }
        return status

# Initialize bot manager
bot_manager = BotManager()

# Flask Routes
@app.route('/')
def home():
    """Home page - shows bot status"""
    status = bot_manager.get_status()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Host</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .status {{ padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .running {{ background-color: #d4edda; color: #155724; }}
            .stopped {{ background-color: #f8d7da; color: #721c24; }}
            button {{ padding: 10px 20px; margin: 5px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Bot Host</h1>
        <div class="status {'running' if status['running'] else 'stopped'}">
            <h2>Status: {'🟢 RUNNING' if status['running'] else '🔴 STOPPED'}</h2>
            <p>PID: {status['pid'] or 'N/A'}</p>
            <p>Restart Count: {status['restart_count']}</p>
            <p>Uptime: {int(status['uptime'])} seconds</p>
        </div>
        
        <div>
            <a href="/start"><button>Start Bot</button></a>
            <a href="/stop"><button>Stop Bot</button></a>
            <a href="/restart"><button>Restart Bot</button></a>
            <a href="/health"><button>Health Check</button></a>
            <a href="/logs"><button>View Logs</button></a>
        </div>
        
        <p style="margin-top: 30px;">
            <strong>Uptime Robot URL:</strong> https://{request.host}/health<br>
            <strong>Ping every 5 minutes to keep alive</strong>
        </p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint for Uptime Robot"""
    status = bot_manager.get_status()
    
    # If bot is not running, try to start it
    if not status['running']:
        bot_manager.start_bot()
        status = bot_manager.get_status()  # Get updated status
    
    response = {
        "status": "healthy" if status['running'] else "unhealthy",
        "bot_running": status['running'],
        "timestamp": time.time(),
        "restart_count": status['restart_count'],
        "uptime": status['uptime']
    }
    
    status_code = 200 if status['running'] else 503
    return jsonify(response), status_code

@app.route('/start')
def start_bot():
    """Start the bot manually"""
    success = bot_manager.start_bot()
    if success:
        return jsonify({"message": "Bot started successfully", "success": True}), 200
    else:
        return jsonify({"message": "Failed to start bot", "success": False}), 500

@app.route('/stop')
def stop_bot():
    """Stop the bot manually"""
    bot_manager.stop_bot()
    return jsonify({"message": "Bot stopped", "success": True}), 200

@app.route('/restart')
def restart_bot():
    """Restart the bot"""
    success = bot_manager.restart_bot()
    if success:
        return jsonify({"message": "Bot restarted successfully", "success": True}), 200
    else:
        return jsonify({"message": "Failed to restart bot", "success": False}), 500

@app.route('/status')
def status():
    """Get detailed bot status"""
    status = bot_manager.get_status()
    return jsonify(status), 200

@app.route('/logs')
def view_logs():
    """View recent logs"""
    try:
        # Try to read last 100 lines from bot output
        logs = []
        if bot_manager.process:
            # This is a simplified view - in production, you'd want to store logs properly
            logs = ["Logs are being streamed to console..."]
        
        return jsonify({"logs": logs[-100:]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return "pong", 200

@app.route('/keepalive')
def keepalive():
    """Keep-alive endpoint for external services"""
    return "Alive and kicking! 🚀", 200

def cleanup():
    """Cleanup function to stop bot on exit"""
    logger.info("Shutting down... Stopping bot")
    bot_manager.stop_bot()

# Register cleanup
atexit.register(cleanup)

# Start bot when host.py starts
if __name__ == '__main__':
    # Start bot automatically
    logger.info("=== Starting Telegram Bot Host ===")
    logger.info(f"Bot file: {BOT_FILE}")
    logger.info(f"Port: {PORT}")
    
    # Start bot in background
    bot_started = bot_manager.start_bot()
    
    if bot_started:
        logger.info("Bot started successfully")
    else:
        logger.error("Failed to start bot initially")
    
    # Start Flask server
    logger.info(f"Starting Flask server on port {PORT}...")
    logger.info(f"Health check URL: http://localhost:{PORT}/health")
    logger.info("Uptime Robot should ping: /health every 5 minutes")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        threaded=True
                  )

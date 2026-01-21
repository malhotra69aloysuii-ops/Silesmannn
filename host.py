"""
host.py - Flask wrapper for Telegram bot on Replit
Automatically runs bot.py and provides web interface
Uptime Robot pings /health to keep alive
"""

from flask import Flask, jsonify, render_template_string
import threading
import subprocess
import os
import sys
import time
import atexit
import logging

# Configure logging for Replit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global variables
bot_process = None
is_bot_running = False
restart_count = 0
MAX_RESTARTS = 50
BOT_FILE = "bot.py"
PORT = 8080  # Replit uses 8080 by default

# HTML Template for Web Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Telegram Bot Host</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        .status-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 20px;
        }
        .status-running { background: #10B981; color: white; }
        .status-stopped { background: #EF4444; color: white; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        .stat-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .stat-label {
            opacity: 0.8;
            font-size: 0.9em;
        }
        .controls {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
            margin: 30px 0;
        }
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .btn-start { background: #10B981; color: white; }
        .btn-stop { background: #EF4444; color: white; }
        .btn-restart { background: #3B82F6; color: white; }
        .btn-health { background: #8B5CF6; color: white; }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); }
        .info-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            margin-top: 30px;
        }
        .url-display {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            word-break: break-all;
            margin: 15px 0;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            opacity: 0.8;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 Telegram Bot Host</h1>
            <p>Running your bot 24/7 on Replit</p>
        </header>
        
        <div class="status-card">
            <div class="status-badge {{ 'status-running' if status.running else 'status-stopped' }}">
                {{ '🟢 BOT RUNNING' if status.running else '🔴 BOT STOPPED' }}
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">Restarts</div>
                    <div class="stat-value">{{ status.restart_count }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Uptime</div>
                    <div class="stat-value">{{ status.uptime_str }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">PID</div>
                    <div class="stat-value">{{ status.pid or 'N/A' }}</div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <a href="/start" class="btn btn-start">▶️ Start Bot</a>
            <a href="/stop" class="btn btn-stop">⏹️ Stop Bot</a>
            <a href="/restart" class="btn btn-restart">🔄 Restart Bot</a>
            <a href="/health" class="btn btn-health">❤️ Health Check</a>
        </div>
        
        <div class="info-box">
            <h3>📡 Uptime Robot Setup</h3>
            <p>Add this URL to Uptime Robot (ping every 5 minutes):</p>
            <div class="url-display">https://{{ request.host }}/health</div>
            <p>Alternative endpoints you can ping:</p>
            <div class="url-display">https://{{ request.host }}/ping<br>
            https://{{ request.host }}/keepalive</div>
        </div>
        
        <footer>
            <p>Bot will stay awake as long as Uptime Robot pings every 5 minutes</p>
            <p>Bot file: {{ status.bot_file }} | Port: {{ status.port }}</p>
        </footer>
    </div>
</body>
</html>
"""

def format_uptime(seconds):
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}m"
    elif seconds < 86400:
        return f"{int(seconds/3600)}h"
    else:
        return f"{int(seconds/86400)}d"

class BotManager:
    def __init__(self):
        self.process = None
        self.start_time = None
        
    def start_bot(self):
        """Start the Telegram bot"""
        global is_bot_running, restart_count
        
        if self.process and self.process.poll() is None:
            logger.info("Bot is already running")
            return True
        
        try:
            logger.info("🚀 Starting Telegram bot...")
            
            # Set environment variable for bot
            env = os.environ.copy()
            
            # Start bot process
            self.process = subprocess.Popen(
                [sys.executable, BOT_FILE],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            is_bot_running = True
            self.start_time = time.time()
            restart_count += 1
            
            # Start output reader in background
            threading.Thread(target=self.read_output, daemon=True).start()
            
            # Start monitor thread
            threading.Thread(target=self.monitor_process, daemon=True).start()
            
            logger.info(f"✅ Bot started (PID: {self.process.pid})")
            logger.info(f"📁 Running: {BOT_FILE}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            is_bot_running = False
            return False
    
    def read_output(self):
        """Read bot output and log it"""
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line.strip():
                    logger.info(f"🤖 {line.strip()}")
        except:
            pass
    
    def monitor_process(self):
        """Monitor bot process and restart if needed"""
        while is_bot_running:
            time.sleep(5)
            
            if self.process and self.process.poll() is not None:
                logger.warning("Bot process stopped! Restarting...")
                time.sleep(2)
                self.start_bot()
                break
    
    def stop_bot(self):
        """Stop the bot process"""
        global is_bot_running
        
        if self.process:
            logger.info("🛑 Stopping bot...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass
            
            self.process = None
            is_bot_running = False
            logger.info("Bot stopped")
    
    def restart_bot(self):
        """Restart the bot"""
        self.stop_bot()
        time.sleep(2)
        return self.start_bot()
    
    def get_status(self):
        """Get current bot status"""
        status = {
            "running": is_bot_running,
            "pid": self.process.pid if self.process else None,
            "bot_file": BOT_FILE,
            "port": PORT,
            "restart_count": restart_count,
            "start_time": self.start_time,
            "uptime": time.time() - self.start_time if self.start_time else 0,
            "uptime_str": format_uptime(time.time() - self.start_time) if self.start_time else "0s"
        }
        return status

# Initialize bot manager
bot_manager = BotManager()

# Flask Routes
@app.route('/')
def home():
    """Main dashboard"""
    status = bot_manager.get_status()
    return render_template_string(HTML_TEMPLATE, status=status)

@app.route('/health')
def health():
    """Health check endpoint for Uptime Robot"""
    status = bot_manager.get_status()
    
    # Auto-start bot if not running
    if not status['running']:
        logger.info("Health check: Bot not running, starting...")
        bot_manager.start_bot()
        status = bot_manager.get_status()
    
    response = {
        "status": "healthy" if status['running'] else "starting",
        "bot_running": status['running'],
        "timestamp": time.time(),
        "restart_count": status['restart_count'],
        "uptime": status['uptime_str'],
        "message": "✅ Bot is running" if status['running'] else "🔄 Starting bot..."
    }
    
    return jsonify(response), 200 if status['running'] else 202

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return "🏓 Pong! Bot host is alive!", 200

@app.route('/keepalive')
def keepalive():
    """Keep-alive endpoint"""
    return "💓 I'm alive! " + time.strftime("%Y-%m-%d %H:%M:%S"), 200

@app.route('/start')
def start():
    """Manually start bot"""
    success = bot_manager.start_bot()
    if success:
        return jsonify({"success": True, "message": "Bot started"}), 200
    return jsonify({"success": False, "message": "Failed to start bot"}), 500

@app.route('/stop')
def stop():
    """Manually stop bot"""
    bot_manager.stop_bot()
    return jsonify({"success": True, "message": "Bot stopped"}), 200

@app.route('/restart')
def restart():
    """Manually restart bot"""
    success = bot_manager.restart_bot()
    if success:
        return jsonify({"success": True, "message": "Bot restarted"}), 200
    return jsonify({"success": False, "message": "Failed to restart"}), 500

@app.route('/status')
def status():
    """Get status in JSON format"""
    status = bot_manager.get_status()
    return jsonify(status), 200

@app.route('/debug')
def debug():
    """Debug information"""
    import platform
    info = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "replit": True,
        "bot_file_exists": os.path.exists(BOT_FILE),
        "env_token_set": "TELEGRAM_TOKEN" in os.environ,
        "cwd": os.getcwd(),
        "files": os.listdir(".")
    }
    return jsonify(info), 200

def cleanup():
    """Cleanup on exit"""
    logger.info("Cleaning up...")
    bot_manager.stop_bot()

# Register cleanup
atexit.register(cleanup)

# Start bot when host starts
def initialize():
    """Initialize the application"""
    logger.info("=" * 50)
    logger.info("🤖 TELEGRAM BOT HOST STARTING")
    logger.info("=" * 50)
    
    # Check if bot.py exists
    if not os.path.exists(BOT_FILE):
        logger.error(f"❌ {BOT_FILE} not found!")
        logger.info("Creating a sample bot.py...")
        with open(BOT_FILE, "w") as f:
            f.write("""# Your bot.py will be here
print("Sample bot.py - replace with your actual bot!")""")
    
    # Start bot
    logger.info("Starting bot automatically...")
    bot_manager.start_bot()
    
    logger.info(f"🌐 Web interface: http://0.0.0.0:{PORT}")
    logger.info(f"❤️  Health check: /health (for Uptime Robot)")
    logger.info(f"🏓 Ping endpoint: /ping")
    logger.info("=" * 50)

if __name__ == '__main__':
    # Initialize on startup
    initialize()
    
    # Start Flask app
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        threaded=True
    )

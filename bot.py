import requests
import time
import os
import json

TOKEN = os.environ.get("8815425327:AAFbjc9A-sWFKYshHGGNcg0fpHmljUAyPTw")
ASSEMBLYAI_KEY = os.environ.get("e44ffe593a3c43e0b9ad4c8e4537d467")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
CHANNEL_USERNAME = "Acc_po"
CHANNEL_LINK = "https://t.me/Acc_po"

# =============== فایل ذخیره اطلاعات کاربران ===============
USERS_FILE = "users_data.json"
BLOCKED_FILE = "blocked_users.json"

def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "users" in data:
                    return data
                else:
                    return {"users": []}
        else:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump({"users": []}, f, ensure_ascii=False, indent=2)
            return {"users": []}
    except:
        return {"users": []}

def save_users(users_data):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_blocked():
    try:
        if os.path.exists(BLOCKED_FILE):
            with open(BLOCKED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "blocked" in data:
                    return data
                else:
                    return {"blocked": []}
        else:
            with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
                json.dump({"blocked": []}, f, ensure_ascii=False, indent=2)
            return {"blocked": []}
    except:
        return {"blocked": []}

def save_blocked(blocked_data):
    try:
        with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
            json.dump(blocked_data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def add_user(user_id, username=None, first_name=None):
    users_data = load_users()
    if user_id not in users_data["users"]:
        users_data["users"].append(user_id)
        save_users(users_data)
    
    user_info_file = f"user_{user_id}.json"
    try:
        with open(user_info_file, "r", encoding="utf-8") as f:
            info = json.load(f)
    except:
        info = {}
    
    info["user_id"] = user_id
    info["username"] = username
    info["first_name"] = first_name
    info["last_activity"] = time.time()
    
    with open(user_info_file, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

def is_blocked(user_id):
    blocked_data = load_blocked()
    return user_id in blocked_data["blocked"]

def block_user(user_id):
    blocked_data = load_blocked()
    if user_id not in blocked_data["blocked"]:
        blocked_data["blocked"].append(user_id)
        save_blocked(blocked_data)
        return True
    return False

def unblock_user(user_id):
    blocked_data = load_blocked()
    if user_id in blocked_data["blocked"]:
        blocked_data["blocked"].remove(user_id)
        save_blocked(blocked_data)
        return True
    return False

# =============== توابع پایه ===============
def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"خطا: {e}")
        return None

def edit_message(chat_id, message_id, text, reply_markup=None):
    url = f"{BASE_URL}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"خطا: {e}")
        return None

def send_typing(chat_id):
    url = f"{BASE_URL}/sendChatAction"
    payload = {"chat_id": chat_id, "action": "typing"}
    try:
        requests.post(url, json=payload)
    except:
        pass

def download_file(file_id):
    try:
        url = f"{BASE_URL}/getFile"
        payload = {"file_id": file_id}
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get("ok"):
            file_path = data["result"]["file_path"]
            download_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            
            response = requests.get(download_url)
            if response.status_code == 200:
                filename = f"voice_{int(time.time())}.mp3"
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename
        return None
    except Exception as e:
        print(f"خطا: {e}")
        return None

# =============== بررسی عضویت ===============
def check_member(chat_id):
    try:
        url = f"{BASE_URL}/getChatMember"
        payload = {
            "chat_id": f"@{CHANNEL_USERNAME}",
            "user_id": chat_id
        }
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get("ok"):
            status = data["result"]["status"]
            return status in ["member", "administrator", "creator"]
        return False
    except:
        return False

def get_join_button():
    return {
        "inline_keyboard": [
            [
                {"text": "📢 عضویت در کانال", "url": CHANNEL_LINK}
            ],
            [
                {"text": "🔄 بررسی مجدد", "callback_data": "check_member"}
            ]
        ]
    }

# =============== دکمه‌های شیشه‌ای ===============
def get_main_menu():
    return {
        "inline_keyboard": [
            [
                {"text": "🎤 تبدیل صدا به متن", "callback_data": "voice_to_text", "bg_color": "#00D26A"}
            ],
            [
                {"text": "📖 راهنما", "callback_data": "help", "bg_color": "#FFB800"},
                {"text": "ℹ️ درباره", "callback_data": "about", "bg_color": "#0088FF"}
            ],
            [
                {"text": "📞 پشتیبانی", "url": CHANNEL_LINK, "bg_color": "#FF6B6B"}
            ]
        ]
    }

def get_admin_menu():
    return {
        "inline_keyboard": [
            [
                {"text": "📢 ارسال پیام همگانی", "callback_data": "broadcast", "bg_color": "#0088FF"}
            ],
            [
                {"text": "👥 لیست کاربران", "callback_data": "users_list", "bg_color": "#FFB800"},
                {"text": "🚫 کاربران بلاک شده", "callback_data": "blocked_list", "bg_color": "#FF4444"}
            ],
            [
                {"text": "📊 آمار ربات", "callback_data": "stats", "bg_color": "#9B59B6"}
            ],
            [
                {"text": "🔙 خروج از پنل", "callback_data": "exit_admin", "bg_color": "#FF6B6B"}
            ]
        ]
    }

def get_broadcast_menu():
    return {
        "inline_keyboard": [
            [
                {"text": "📝 از طرف پشتیبانی", "callback_data": "broadcast_support", "bg_color": "#00D26A"},
                {"text": "🤖 از طرف ربات", "callback_data": "broadcast_bot", "bg_color": "#0088FF"}
            ],
            [
                {"text": "🔙 انصراف", "callback_data": "back_admin", "bg_color": "#FF6B6B"}
            ]
        ]
    }

def get_back_menu():
    return {
        "inline_keyboard": [
            [
                {"text": "🔙 برگشت به منو", "callback_data": "back_main", "bg_color": "#FF6B6B"}
            ]
        ]
    }

def get_result_menu():
    return {
        "inline_keyboard": [
            [
                {"text": "🔄 تبدیل دوباره", "callback_data": "voice_to_text", "bg_color": "#00D26A"},
                {"text": "🔙 برگشت", "callback_data": "back_main", "bg_color": "#FF6B6B"}
            ],
            [
                {"text": "📞 پشتیبانی", "url": CHANNEL_LINK, "bg_color": "#FF6B6B"}
            ]
        ]
    }

# =============== لودینگ جذاب ===============
def get_loading_frames():
    frames = [
        "⏳ در حال پردازش...\n\n🔄 در حال آماده‌سازی...",
        "⏳ در حال پردازش...\n\n📤 در حال آپلود فایل...",
        "⏳ در حال پردازش...\n\n🎧 در حال پردازش صدا...",
        "⏳ در حال پردازش...\n\n🔍 در حال تشخیص گفتار...",
        "⏳ در حال پردازش...\n\n📝 در حال تبدیل به متن...",
        "⏳ در حال پردازش...\n\n✅ تقریباً آماده..."
    ]
    return frames

def get_loading_with_animation(step):
    frames = get_loading_frames()
    index = step % len(frames)
    circles = ["◐", "◓", "◑", "◒"]
    circle = circles[step % len(circles)]
    text = frames[index]
    text += f"\n\n{circle}"
    return text

# =============== توابع AssemblyAI ===============
def upload_audio_to_assemblyai(audio_file):
    try:
        with open(audio_file, "rb") as f:
            response = requests.post(
                "https://api.assemblyai.com/v2/upload",
                headers={"authorization": ASSEMBLYAI_KEY},
                data=f
            )
        
        if response.status_code == 200:
            return response.json()["upload_url"]
        return None
    except Exception as e:
        print(f"خطا: {e}")
        return None

def start_transcription(audio_url):
    try:
        payload = {
            "audio_url": audio_url,
            "language_code": "fa"
        }
        
        response = requests.post(
            "https://api.assemblyai.com/v2/transcript",
            headers={"authorization": ASSEMBLYAI_KEY},
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()["id"]
        return None
    except Exception as e:
        print(f"خطا: {e}")
        return None

def get_transcription_result(transcript_id):
    try:
        response = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers={"authorization": ASSEMBLYAI_KEY}
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"خطا: {e}")
        return None

def transcribe_audio(audio_file, chat_id):
    try:
        audio_url = upload_audio_to_assemblyai(audio_file)
        
        if not audio_url:
            return "❌ خطا در آپلود فایل"
        
        transcript_id = start_transcription(audio_url)
        
        if not transcript_id:
            return "❌ خطا در شروع تشخیص"
        
        while True:
            result = get_transcription_result(transcript_id)
            
            if not result:
                return "❌ خطا در دریافت نتیجه"
            
            if result["status"] == "completed":
                return result["text"]
            elif result["status"] == "error":
                return f"❌ خطا: {result.get('error', 'ناشناخته')}"
            
            time.sleep(2)
            
    except Exception as e:
        return f"❌ خطا: {str(e)}"

# =============== وضعیت کاربران ===============
user_states = {}
broadcast_data = {}
admin_mode = {}

def get_user_state(chat_id):
    return user_states.get(chat_id, {"message_id": None, "mode": "main"})

def set_user_state(chat_id, message_id=None, mode="main"):
    user_states[chat_id] = {"message_id": message_id, "mode": mode}

def is_admin_mode(chat_id):
    return admin_mode.get(chat_id, False)

def set_admin_mode(chat_id, status):
    admin_mode[chat_id] = status

def get_user_info(user_id):
    try:
        user_info_file = f"user_{user_id}.json"
        with open(user_info_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# =============== پردازش ===============
def process_callback(update):
    callback = update.get("callback_query", {})
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]
    data = callback.get("data", "")
    
    try:
        requests.post(f"{BASE_URL}/answerCallbackQuery", 
                     json={"callback_query_id": callback["id"]})
    except:
        pass
    
    if data == "exit_admin":
        set_admin_mode(chat_id, False)
        edit_message(chat_id, message_id,
            "✅ <b>از پنل مدیریت خارج شدید!</b>\n\n"
            "اکنون مانند یک کاربر عادی از ربات استفاده کنید.",
            get_main_menu()
        )
        set_user_state(chat_id, message_id, "main")
        return
    
    if data == "back_admin":
        if not is_admin_mode(chat_id):
            return
        edit_message(chat_id, message_id,
            "🛡️ <b>پنل مدیریت</b>\n\n"
            "خوش آمدید!\n"
            "یکی از گزینه‌ها را انتخاب کنید:",
            get_admin_menu()
        )
        set_user_state(chat_id, message_id, "admin")
        return
    
    if data == "stats":
        if not is_admin_mode(chat_id):
            return
        
        users_data = load_users()
        blocked_data = load_blocked()
        total_users = len(users_data["users"])
        total_blocked = len(blocked_data["blocked"])
        
        stats_text = (
            "📊 <b>آمار ربات</b>\n\n"
            f"👥 تعداد کل کاربران: {total_users}\n"
            f"🚫 کاربران بلاک شده: {total_blocked}\n"
            f"✅ کاربران فعال: {total_users - total_blocked}\n\n"
            f"📅 تاریخ: {time.strftime('%Y/%m/%d')}\n"
            f"⏰ زمان: {time.strftime('%H:%M:%S')}"
        )
        
        edit_message(chat_id, message_id, stats_text, get_admin_menu())
        set_user_state(chat_id, message_id, "admin")
        return
    
    if data == "broadcast":
        if not is_admin_mode(chat_id):
            return
        edit_message(chat_id, message_id,
            "📢 <b>ارسال پیام همگانی</b>\n\n"
            "لطفاً نحوه ارسال را انتخاب کنید:",
            get_broadcast_menu()
        )
        set_user_state(chat_id, message_id, "broadcast_select")
        return
    
    if data == "broadcast_support":
        if not is_admin_mode(chat_id):
            return
        broadcast_data[chat_id] = {"mode": "support"}
        edit_message(chat_id, message_id,
            "📝 <b>ارسال پیام از طرف پشتیبانی</b>\n\n"
            "لطفاً پیام مورد نظر خود را ارسال کنید.",
            get_back_menu()
        )
        set_user_state(chat_id, message_id, "waiting_broadcast")
        return
    
    if data == "broadcast_bot":
        if not is_admin_mode(chat_id):
            return
        broadcast_data[chat_id] = {"mode": "bot"}
        edit_message(chat_id, message_id,
            "🤖 <b>ارسال پیام از طرف ربات</b>\n\n"
            "لطفاً پیام مورد نظر خود را ارسال کنید.",
            get_back_menu()
        )
        set_user_state(chat_id, message_id, "waiting_broadcast")
        return
    
    if data == "users_list":
        if not is_admin_mode(chat_id):
            return
        users_data = load_users()
        users = users_data["users"]
        
        if not users:
            edit_message(chat_id, message_id,
                "👥 <b>لیست کاربران</b>\n\n"
                "هیچ کاربری در سیستم ثبت نشده است.",
                get_admin_menu()
            )
            return
        
        text = "👥 <b>لیست کاربران</b>\n\n"
        buttons = []
        for i, user_id in enumerate(users[:10], 1):
            user_info = get_user_info(user_id)
            name = user_info.get("first_name", "ناشناس")
            username = user_info.get("username", "")
            username_text = f" (@{username})" if username else ""
            text += f"{i}. {name}{username_text}\n   🆔: {user_id}\n\n"
            buttons.append([{"text": f"🚫 بلاک {name[:10]}", "callback_data": f"block_{user_id}", "bg_color": "#FF4444"}])
        
        if len(users) > 10:
            text += f"\n... و {len(users) - 10} کاربر دیگر"
        
        text += f"\n📊 مجموع: {len(users)} کاربر"
        
        buttons.append([{"text": "🔙 برگشت به پنل", "callback_data": "back_admin", "bg_color": "#FF6B6B"}])
        
        keyboard = {"inline_keyboard": buttons}
        edit_message(chat_id, message_id, text, keyboard)
        set_user_state(chat_id, message_id, "admin")
        return
    
    if data == "blocked_list":
        if not is_admin_mode(chat_id):
            return
        blocked_data = load_blocked()
        blocked = blocked_data["blocked"]
        
        if not blocked:
            edit_message(chat_id, message_id,
                "🚫 <b>کاربران بلاک شده</b>\n\n"
                "هیچ کاربری بلاک نشده است.",
                get_admin_menu()
            )
            return
        
        text = "🚫 <b>کاربران بلاک شده</b>\n\n"
        buttons = []
        for i, user_id in enumerate(blocked[:10], 1):
            user_info = get_user_info(user_id)
            name = user_info.get("first_name", "ناشناس")
            username = user_info.get("username", "")
            username_text = f" (@{username})" if username else ""
            text += f"{i}. {name}{username_text}\n   🆔: {user_id}\n\n"
            buttons.append([{"text": f"✅ رفع بلاک {name[:10]}", "callback_data": f"unblock_{user_id}", "bg_color": "#00D26A"}])
        
        if len(blocked) > 10:
            text += f"\n... و {len(blocked) - 10} کاربر دیگر"
        
        text += f"\n📊 مجموع: {len(blocked)} کاربر بلاک شده"
        
        buttons.append([{"text": "🔙 برگشت به پنل", "callback_data": "back_admin", "bg_color": "#FF6B6B"}])
        
        keyboard = {"inline_keyboard": buttons}
        edit_message(chat_id, message_id, text, keyboard)
        set_user_state(chat_id, message_id, "admin")
        return
    
    if data.startswith("block_"):
        if not is_admin_mode(chat_id):
            return
        user_id = int(data.split("_")[1])
        if block_user(user_id):
            edit_message(chat_id, message_id,
                f"✅ <b>کاربر {user_id} با موفقیت بلاک شد!</b>",
                get_admin_menu()
            )
        else:
            edit_message(chat_id, message_id,
                f"⚠️ <b>کاربر {user_id} قبلاً بلاک شده است!</b>",
                get_admin_menu()
            )
        set_user_state(chat_id, message_id, "admin")
        return
    
    if data.startswith("unblock_"):
        if not is_admin_mode(chat_id):
            return
        user_id = int(data.split("_")[1])
        if unblock_user(user_id):
            edit_message(chat_id, message_id,
                f"✅ <b>بلاک کاربر {user_id} برداشته شد!</b>",
                get_admin_menu()
            )
        else:
            edit_message(chat_id, message_id,
                f"⚠️ <b>کاربر {user_id} بلاک نبوده است!</b>",
                get_admin_menu()
            )
        set_user_state(chat_id, message_id, "admin")
        return
    
    if data == "check_member":
        if check_member(chat_id):
            edit_message(chat_id, message_id,
                "✅ <b>عضویت شما تأیید شد!</b>\n\n"
                "🎤 لطفاً یک ویس ارسال کنید.",
                get_main_menu()
            )
            set_user_state(chat_id, message_id, "main")
        else:
            edit_message(chat_id, message_id,
                "❌ <b>شما هنوز عضو کانال نشدید!</b>\n\n"
                "لطفاً ابتدا در کانال زیر عضو شوید:",
                get_join_button()
            )
        return
    
    if data == "back_main":
        if is_admin_mode(chat_id):
            set_admin_mode(chat_id, False)
        edit_message(chat_id, message_id,
            "🏠 <b>منوی اصلی</b>\n\n"
            "لطفاً یکی از گزینه‌ها را انتخاب کنید:",
            get_main_menu()
        )
        set_user_state(chat_id, message_id, "main")
        return
    
    if data == "voice_to_text":
        if is_blocked(chat_id):
            edit_message(chat_id, message_id,
                "🚫 <b>شما توسط ادمین بلاک شده‌اید!</b>\n\n"
                "📞 پشتیبانی: @Acc_po",
                get_main_menu()
            )
            return
        
        if not check_member(chat_id):
            edit_message(chat_id, message_id,
                "🔒 <b>عضویت در کانال الزامی است!</b>\n\n"
                "لطفاً ابتدا در کانال زیر عضو شوید:",
                get_join_button()
            )
            return
        
        edit_message(chat_id, message_id,
            "🎤 <b>ویس خود را ارسال کنید</b>\n\n"
            "📌 یک پیام صوتی (ویس) برای من بفرستید.\n\n"
            "⏳ پس از ارسال، به متن تبدیل میشود.",
            get_back_menu()
        )
        set_user_state(chat_id, message_id, "voice")
        return
    
    if data == "help":
        edit_message(chat_id, message_id,
            "📖 <b>راهنما</b>\n\n"
            "🎤 یک ویس بفرستید\n"
            "⏳ ربات به متن تبدیل میکند\n\n"
            "📞 پشتیبانی: @Acc_po",
            get_main_menu()
        )
        set_user_state(chat_id, message_id, "main")
        return
    
    if data == "about":
        edit_message(chat_id, message_id,
            "🤖 <b>درباره ربات</b>\n\n"
            "🔧 تبدیل صدا به متن\n"
            "📌 نسخه 2.0\n"
            "🇮🇷 پشتیبانی از فارسی\n\n"
            "📞 پشتیبانی: @Acc_po",
            get_main_menu()
        )
        set_user_state(chat_id, message_id, "main")
        return

def process_message(update):
    message = update.get("message", {})
    chat_id = message["chat"]["id"]
    user_state = get_user_state(chat_id)
    
    # ===== پردازش پیام برای ارسال همگانی =====
    if user_state.get("mode") == "waiting_broadcast" and is_admin_mode(chat_id):
        if "text" in message:
            broadcast_text = message["text"]
            mode = broadcast_data.get(chat_id, {}).get("mode", "support")
            
            send_message(chat_id, "⏳ در حال ارسال پیام همگانی...")
            
            users_data = load_users()
            users = users_data["users"]
            sent_count = 0
            failed_count = 0
            
            for user_id in users:
                if is_blocked(user_id):
                    continue
                try:
                    if mode == "support":
                        final_text = f"📩 <b>پیام از طرف پشتیبانی:</b>\n\n{broadcast_text}\n\n📞 @Acc_po"
                    else:
                        final_text = broadcast_text
                    
                    send_message(user_id, final_text)
                    sent_count += 1
                    time.sleep(0.05)
                except:
                    failed_count += 1
            
            result_text = f"✅ <b>ارسال همگانی انجام شد!</b>\n\n"
            result_text += f"📤 ارسال شد: {sent_count} کاربر\n"
            result_text += f"❌ ناموفق: {failed_count} کاربر"
            
            edit_message(chat_id, user_state["message_id"], result_text, get_admin_menu())
            set_user_state(chat_id, user_state["message_id"], "admin")
            
            broadcast_data[chat_id] = {}
            return
        
        if "voice" in message or "audio" in message:
            send_message(chat_id, "⚠️ لطفاً فقط متن ارسال کنید!")
            return
    
    # ===== پردازش ویس =====
    if "voice" in message or "audio" in message:
        if is_blocked(chat_id):
            send_message(chat_id, 
                "🚫 <b>شما توسط ادمین بلاک شده‌اید!</b>\n\n"
                "📞 پشتیبانی: @Acc_po",
                get_main_menu()
            )
            return
        
        if not check_member(chat_id):
            send_message(chat_id,
                "🔒 <b>عضویت در کانال الزامی است!</b>\n\n"
                "لطفاً ابتدا در کانال زیر عضو شوید:",
                get_join_button()
            )
            return
        
        user = message.get("from", {})
        add_user(
            chat_id,
            user.get("username"),
            user.get("first_name")
        )
        
        send_typing(chat_id)
        
        if "voice" in message:
            file_id = message["voice"]["file_id"]
        else:
            file_id = message["audio"]["file_id"]
        
        loading_text = get_loading_with_animation(0)
        result = send_message(chat_id, loading_text)
        
        if result and result.get("ok"):
            loading_message_id = result["result"]["message_id"]
        else:
            return
        
        audio_file = download_file(file_id)
        
        if not audio_file:
            edit_message(chat_id, loading_message_id, "❌ <b>خطا در دانلود فایل!</b>")
            return
        
        for step in range(1, 7):
            time.sleep(1)
            loading_text = get_loading_with_animation(step)
            edit_message(chat_id, loading_message_id, loading_text)
        
        edit_message(chat_id, loading_message_id, 
            "🔊 <b>در حال تشخیص گفتار...</b>\n\n"
            "⏳ این کار چند ثانیه طول میکشد...\n\n"
            "◐")
        
        text = transcribe_audio(audio_file, chat_id)
        
        try:
            os.remove(audio_file)
        except:
            pass
        
        if text and not text.startswith("❌"):
            result_text = (
                "✅ <b>تبدیل با موفقیت انجام شد!</b>\n\n"
                "📝 <b>متن تشخیص داده شده:</b>\n\n"
                f"<code>{text}</code>\n\n"
                "📞 پشتیبانی: @Acc_po"
            )
            edit_message(chat_id, loading_message_id, result_text, get_result_menu())
        else:
            edit_message(chat_id, loading_message_id, 
                f"❌ <b>خطا در تشخیص گفتار</b>\n\n{text}\n\n📞 پشتیبانی: @Acc_po",
                get_back_menu()
            )
        return
    
    # ===== پیام متنی =====
    if "text" in message:
        text = message["text"]
        user = message.get("from", {})
        username = user.get("username", "")
        
        # ===== دستور مخصوص ادمین (هر کسی میتونه وارد بشه) =====
        if text == "/modirm":
            set_admin_mode(chat_id, True)
            send_message(chat_id, 
                "🛡️ <b>پنل مدیریت</b>\n\n"
                "✅ <b>به پنل مدیریت خوش آمدید!</b>\n\n"
                "اکنون در حالت مدیریت هستید.\n"
                "از دکمه‌های زیر استفاده کنید:",
                get_admin_menu()
            )
            return
        
        if text == "/lgvmodir":
            if is_admin_mode(chat_id):
                set_admin_mode(chat_id, False)
                send_message(chat_id, 
                    "✅ <b>از پنل مدیریت خارج شدید!</b>\n\n"
                    "اکنون مانند یک کاربر عادی از ربات استفاده کنید.\n"
                    "برای ورود دوباره: /modirm",
                    get_main_menu()
                )
            else:
                send_message(chat_id, 
                    "⚠️ <b>شما در حالت مدیریت نیستید!</b>\n\n"
                    "برای ورود به پنل مدیریت از /modirm استفاده کنید.",
                    get_main_menu()
                )
            return
        
        # ===== اگر کاربر در حالت ادمین هست =====
        if is_admin_mode(chat_id) and user_state.get("mode") != "waiting_broadcast":
            send_message(chat_id, 
                "🛡️ <b>شما در حالت مدیریت هستید!</b>\n\n"
                "از دکمه‌های پنل مدیریت استفاده کنید.\n"
                "برای خروج: /lgvmodir",
                get_admin_menu()
            )
            return
        
        # ===== استارت =====
        if text == "/start":
            add_user(
                chat_id,
                user.get("username"),
                user.get("first_name")
            )
            
            if is_blocked(chat_id):
                send_message(chat_id,
                    "🚫 <b>شما توسط ادمین بلاک شده‌اید!</b>\n\n"
                    "📞 پشتیبانی: @Acc_po",
                    get_main_menu()
                )
                return
            
            result = send_message(chat_id, 
                "🎤 <b>به ربات تشخیص گفتار خوش آمدید!</b>\n\n"
                "✅ یک پیام صوتی (ویس) ارسال کنید\n"
                "✅ ربات به متن تبدیل میکند\n"
                "✅ پشتیبانی از فارسی\n\n"
                "📞 پشتیبانی: @Acc_po",
                get_main_menu()
            )
            if result and result.get("ok"):
                set_user_state(chat_id, result["result"]["message_id"], "main")
            return
        
        if text == "/help":
            send_message(chat_id, 
                "📖 <b>راهنما</b>\n\n"
                "🎤 ویس بفرستید تا به متن تبدیل شود\n\n"
                "📞 پشتیبانی: @Acc_po",
                get_main_menu()
            )
            return
        
        # ===== پیام معمولی =====
        if user_state.get("mode") != "waiting_broadcast":
            send_message(chat_id, 
                "👋 سلام!\n"
                "یک ویس بفرستید تا به متن تبدیل کنم.\n"
                "یا /start را بزنید.\n\n"
                "📞 پشتیبانی: @Acc_po",
                get_main_menu()
            )

def get_updates(offset=0):
    url = f"{BASE_URL}/getUpdates"
    payload = {"offset": offset, "timeout": 20}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if data.get("ok"):
            return data.get("result", [])
        return []
    except:
        return []

# =============== اجرا ===============
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 ربات تشخیص گفتار - صداتو")
    print("=" * 50)
    print("✅ ربات آماده است!")
    print(f"📢 کانال: {CHANNEL_LINK}")
    print("📌 برای شروع /start")
    print("🔑 ورود به پنل مدیریت: /modirm")
    print("🔑 خروج از پنل مدیریت: /lgvmodir")
    print("⚠️ توجه: هر کسی /modirm رو بزنه وارد پنل میشه!")
    print("-" * 50)
    
    offset = 0
    
    while True:
        try:
            updates = get_updates(offset)
            
            for update in updates:
                if update["update_id"] >= offset:
                    offset = update["update_id"] + 1
                
                if "callback_query" in update:
                    process_callback(update)
                elif "message" in update:
                    process_message(update)
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n👋 خاموش شد")
            break
        except Exception as e:
            print(f"❌ خطا: {e}")
            time.sleep(5)
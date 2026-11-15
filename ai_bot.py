import logging
import socket
import subprocess
import sys
import os
from configparser import ConfigParser
from pathlib import Path

import telebot
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "telegram_bot.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

# Load token and allowed Telegram IDs from bot_settings.ini
settings = ConfigParser()
settings_path = BASE_DIR / "bot_settings.ini"

if not settings.read(settings_path, encoding="utf-8"):
    raise FileNotFoundError(f"Settings file not found: {settings_path}")

BOT_TOKEN = settings.get("telegram", "bot_token", fallback="").strip()
ALLOWED_IDS_RAW = settings.get("telegram", "allowed_user_ids", fallback="").strip()

if not BOT_TOKEN:
    raise ValueError("bot_settings.ini is missing bot_token.")

try:
    ALLOWED_USER_IDS = {
        int(user_id.strip())
        for user_id in ALLOWED_IDS_RAW.split(",")
        if user_id.strip()
    }
except ValueError as exc:
    raise ValueError("allowed_user_ids must be comma-separated numeric Telegram IDs.") from exc

if not ALLOWED_USER_IDS:
    raise ValueError("bot_settings.ini is missing allowed_user_ids.")

bot = telebot.TeleBot(BOT_TOKEN)


def is_allowed(message):
    user = getattr(message, "from_user", None)
    return user is not None and user.id in ALLOWED_USER_IDS


def is_allowed_callback(call):
    user = getattr(call, "from_user", None)
    return user is not None and user.id in ALLOWED_USER_IDS


def port_is_open(port):
    """Checks if a local service is accepting connections on the given port."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def get_status():
    services = [
        ("Ollama", 11434),
        ("SillyTavern", 8000),
        ("ComfyUI", 8188),
    ]

    lines = ["🤖 <b>AI Stack Control Panel</b>", "", "<b>Local services status:</b>"]

    for name, port in services:
        state = "🟢 running" if port_is_open(port) else "🔴 not responding"
        lines.append(f"• {name} — {state} (port {port})")

    lines.extend(["", "<i>Note: Checking port availability only; this does not confirm the model is loaded.</i>"])
    return "\n".join(lines)


def get_main_keyboard():
    """Creates the inline keyboard with control buttons."""
    markup = InlineKeyboardMarkup(row_width=2)
    btn_start = InlineKeyboardButton("▶️ Start AI Stack", callback_data="start_all")
    btn_stop = InlineKeyboardButton("🛑 Stop AI Stack", callback_data="stop_all")
    btn_restart_stack = InlineKeyboardButton("🚀 Restart AI Stack", callback_data="restart_stack")
    btn_restart_bot = InlineKeyboardButton("🔄 Restart Bot", callback_data="restart_bot")
    btn_status = InlineKeyboardButton("🔄 Refresh Status", callback_data="status")
    
    markup.add(btn_start, btn_stop)
    markup.add(btn_restart_stack, btn_restart_bot)
    markup.add(btn_status)
    return markup


def run_script(script_name, message=None, chat_id=None):
    script_path = BASE_DIR / script_name

    if not script_path.is_file():
        text = f"❌ File not found: {script_path}"
        if message is not None:
            bot.reply_to(message, text)
        elif chat_id is not None:
            bot.send_message(chat_id, text)
        return False

    try:
        # Launch BAT without a separate CMD window; save output to log.
        with LOG_PATH.open("a", encoding="utf-8") as log_file:
            subprocess.Popen(
                ["cmd.exe", "/c", "call", str(script_path)],
                cwd=str(BASE_DIR),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

        text = f"✅ Command sent: {script_name}"
        if message is not None:
            bot.reply_to(message, text)
        elif chat_id is not None:
            bot.send_message(chat_id, text)
        return True

    except Exception:
        logging.exception("Failed to run %s", script_path)
        text = f"❌ Error running {script_name}. Check logs for details."
        if message is not None:
            bot.reply_to(message, text)
        elif chat_id is not None:
            bot.send_message(chat_id, text)
        return False


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    if not is_allowed(message):
        bot.reply_to(message, "❌ Access denied.")
        return

    bot.reply_to(
        message, 
        get_status(), 
        parse_mode="HTML", 
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(commands=["status"])
def status_command(message):
    if not is_allowed(message):
        bot.reply_to(message, "❌ Access denied.")
        return

    bot.reply_to(message, get_status(), parse_mode="HTML", reply_markup=get_main_keyboard())


@bot.message_handler(commands=["start_all"])
def start_all_command(message):
    if not is_allowed(message):
        bot.reply_to(message, "❌ Access denied.")
        return

    run_script("start_all.bat", message=message)


@bot.message_handler(commands=["stop", "stop_all"])
def stop_command(message):
    if not is_allowed(message):
        bot.reply_to(message, "❌ Access denied.")
        return

    run_script("stop_all.bat", message=message)


@bot.callback_query_handler(func=lambda call: call.data in ("start_all", "stop_all", "status", "restart_stack", "restart_bot"))
def button_callback(call):
    if not is_allowed_callback(call):
        bot.answer_callback_query(call.id, "❌ Access denied.")
        return

    if call.data == "start_all":
        bot.answer_callback_query(call.id, "Starting services...")
        run_script("start_all.bat", chat_id=call.message.chat.id)
        
    elif call.data == "stop_all":
        bot.answer_callback_query(call.id, "Stopping services...")
        run_script("stop_all.bat", chat_id=call.message.chat.id)
        
    elif call.data == "restart_stack":
        bot.answer_callback_query(call.id, "Restarting AI Stack...")
        bot.send_message(call.message.chat.id, "🔄 Stopping services...")
        # Запускаем стоп, ждем немного и запускаем старт (через батник или напрямую)
        run_script("stop_all.bat", chat_id=call.message.chat.id)
        import time
        time.sleep(5) # Ждем 5 секунд, чтобы порты освободились
        bot.send_message(call.message.chat.id, "🚀 Starting services...")
        run_script("start_all.bat", chat_id=call.message.chat.id)

    elif call.data == "restart_bot":
        bot.answer_callback_query(call.id, "Restarting bot...")
        bot.send_message(call.message.chat.id, "🔄 Bot is restarting. Please wait a few seconds...")
        
        # Перезапуск текущего скрипта Python
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    elif call.data == "status":
        bot.answer_callback_query(call.id, "Refreshing status...")
        try:
            # Edit the existing message to update the status smoothly
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_status(),
                parse_mode="HTML",
                reply_markup=get_main_keyboard()
            )
        except Exception as e:
            # If the text hasn't changed, Telegram throws an error. We ignore it.
            if "message is not modified" not in str(e).lower():
                logging.error(f"Failed to edit message: {e}")


@bot.message_handler(func=lambda message: True)
def other_messages(message):
    if not is_allowed(message):
        return

    text = message.text or ""
    if not text.startswith("/"):
        bot.reply_to(
            message, 
            "Use the buttons below or commands: /status, /start_all, /stop_all", 
            reply_markup=get_main_keyboard()
        )


if __name__ == "__main__":
    try:
        bot.set_my_commands(
            [
                BotCommand("start", "Show control panel"),
                BotCommand("status", "Check services status"),
                BotCommand("start_all", "Start AI services"),
                BotCommand("stop_all", "Stop AI services"),
            ]
        )
        logging.info("Bot is starting.")
        bot.infinity_polling(timeout=10, long_polling_timeout=10)
    except Exception:
        logging.exception("Error during bot startup or operation.")
import logging
import random
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging setting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ချစ်စရာနာမည်စာရင်း
NICKNAMES = [
    "ကလေးလေးရေ",
    "ကလေးရေ", 
    "မိန်းမရေ",
    "ကိုကို့မိန်းမရေ",
    "ရေသူမလေး",
    "သမီး",
    "ကိုကို့ကလေးလေးရေ",
    "ကို့အာလူးလေး",
    "သမီးရေ",
    "ဖေ့သီးရေ"
]

def get_random_name():
    return random.choice(NICKNAMES)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'မင်္ဂလာပါ! ကျွန်တော်က နေ့တိုင်း ကျပန်းနာမည်တွေနဲ့ စာပို့ပေးမယ့် Bot ပါ။\n\n'
        '/setjobs လို့ရိုက်ပြီး စတင်လိုက်ပါ။'
    )

async def send_morning_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    name = get_random_name()
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text=f"မင်္ဂလာမနက်ခင်းပါ {name} 🌅"
    )

async def send_evening_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    name = get_random_name()
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text=f"မင်္ဂလာရှိတဲ့ညချမ်းပါ {name} 🌙"
    )

async def set_daily_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    morning_time = time(hour=6, minute=0, second=0)
    context.job_queue.run_daily(
        send_morning_message, 
        morning_time, 
        chat_id=chat_id,
        name="morning_job"
    )
    
    evening_time = time(hour=21, minute=0, second=0)
    context.job_queue.run_daily(
        send_evening_message, 
        evening_time, 
        chat_id=chat_id,
        name="evening_job"
    )
    
    await update.message.reply_text("✅ နေ့စဉ်စာပို့တဲ့ အချိန်တွေကို သတ်မှတ်ပြီးပါပြီ။")

async def show_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names_list = "\n".join([f"• {name}" for name in NICKNAMES])
    await update.message.reply_text(
        f"📋 ကျပန်းရွေးချယ်မယ့် နာမည်စာရင်း:\n\n{names_list}"
    )

def main():
    # ဒီနေရာမှာ ခင်ဗျားရဲ့ Token ထည့်ပါ
    application = Application.builder().token('6741485363:AAEiD4ms0rwhi7K3ZJfm4Gj_KjPDWiNiaVg').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('setjobs', set_daily_jobs))
    application.add_handler(CommandHandler('names', show_names))

    application.run_polling()

if __name__ == '__main__':
    main()

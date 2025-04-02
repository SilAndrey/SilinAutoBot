from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8134362274:AAGoR7CvapHxk1sWENiluhiBTRzGnXPY0gw"
OWNER_ID = 487330910

user_data = {}

STEP_NAME = 1
STEP_PHONE = 2
STEP_BIZ = 3

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {"step": STEP_NAME}
    await update.message.reply_text("Привет! Давай сделаем заявку на Telegram-бота для тебя.\n📝 Введи своё имя:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_data:
        await start(update, context)
        return

    step = user_data[chat_id].get("step")

    if step == STEP_NAME:
        user_data[chat_id]["name"] = text
        user_data[chat_id]["step"] = STEP_PHONE
        await update.message.reply_text("Ок, введи телефон для связи:")

    elif step == STEP_PHONE:
        user_data[chat_id]["phone"] = text
        user_data[chat_id]["step"] = STEP_BIZ
        await update.message.reply_text("Какой у тебя бизнес или зачем нужен бот?")

    elif step == STEP_BIZ:
        user_data[chat_id]["biz"] = text
        info = user_data[chat_id]

        msg = f"✨ Новая заявка:\n"
        msg += f"Имя: {info['name']}\n📞 Телефон: {info['phone']}\n💼 Бизнес / задача: {info['biz']}"

        await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        await update.message.reply_text("Спасибо! Я скоро с тобой свяжусь ✨")

        user_data.pop(chat_id)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()

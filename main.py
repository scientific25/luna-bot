import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GRUPO_VIP_LINK = os.getenv("GRUPO_VIP_LINK")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Olá, amorzinho 😘\n\nPara acessar meu grupo VIP, escolha um plano aqui:\n\n"
        f"🔞 https://linktr.ee/lunaangelvip\n\n"
        f"💋 Depois do pagamento, me chama aqui ou aguarde o acesso automático!"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot iniciado...")
app.run_polling()

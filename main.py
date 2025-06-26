from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# LINKS DOS PLANOS
PLANOS = {
    "7_DIAS": {
        "pix": "https://app.pushinpay.com.br/service/pay/9F3EF990-5A7A-45D1-8C47-69DF06F06568",
        "cartao": "https://buy.stripe.com/7sY7sL2OFb5z1GRcKE0ZW01"
    },
    "30_DIAS": {
        "pix": "https://app.pushinpay.com.br/service/pay/9F3EFA7B-D3CB-42A7-A8D0-105D114FE464",
        "cartao": "https://buy.stripe.com/cNifZh74V0qVclv4e80ZW02"
    },
    "SEMESTRAL": {
        "pix": "https://app.pushinpay.com.br/service/pay/9F3F2A96-283F-4CB7-85B2-70CE16EE6D10",
        "cartao": "https://buy.stripe.com/3cI14nexnb5z85f2600ZW05"
    },
    "VITALICIA": {
        "pix": "https://app.pushinpay.com.br/service/pay/9F3EFB63-D89D-4076-9D07-6D4B749AAF76",
        "cartao": "https://buy.stripe.com/5kQbJ19d38Xrbhr2600ZW04"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("7 Dias 😍", callback_data="PLANO_7_DIAS")],
        [InlineKeyboardButton("30 Dias 🐵", callback_data="PLANO_30_DIAS")],
        [InlineKeyboardButton("Semestral 💖", callback_data="PLANO_SEMESTRAL")],
        [InlineKeyboardButton("Vitalícia 💎", callback_data="PLANO_VITALICIA")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Oi, amorzinho 😘\n\nEscolha um dos meus planos VIP aqui embaixo pra liberar tudinho pra você... 😈",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("PLANO_"):
        plano = data.replace("PLANO_", "")
        texto = f"🔥 Amor, você escolheu o plano {plano.replace('_', ' ').title()}...\nAgora é só escolher como quer pagar e veja o que tenho pra te dar 😈🌶"

        links = PLANOS.get(plano)
        if not links:
            await query.edit_message_text("Erro ao buscar os links do plano 😢")
            return

        keyboard = [
            [
                InlineKeyboardButton("💸 PIX", url=links['pix']),
                InlineKeyboardButton("💳 Cartão", url=links['cartao'])
            ],
            [InlineKeyboardButton("🔙 Voltar", callback_data="VOLTAR_MENU")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(texto, reply_markup=reply_markup)

    elif data == "VOLTAR_MENU":
        await start(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot iniciado...")
app.run_polling()


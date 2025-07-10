from db_utils import init_db, salvar_expiracao, carregar_expiracoes, remover_expiracao

import os
import json
import requests
from flask import Flask, request
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, CallbackContext
import threading
import time

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PUSHINPAY_API_KEY = os.getenv("PUSHINPAY_API_KEY")

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

PLANS = {
    "24_horas": {
        "label": "💦 24 horas – R$ 4,99",
        "link": "https://app.pushinpay.com.br/service/pay/9f5b0067-b56d-4051-8914-855691f58358",
        "hours": 24
    },
    "7_dias": {
        "label": "🔥 7 dias – R$ 9,99",
        "link": "https://app.pushinpay.com.br/service/pay/9f5b00c0-2f1f-41dd-946f-8d526c83b06f",
        "hours": 168
    },
    "30_dias": {
        "label": "👅 30 dias – R$ 19,99",
        "link": "https://app.pushinpay.com.br/service/pay/9f5b0103-c237-4ce7-a5a7-dae95e0872dd",
        "hours": 720
    },
    "vitalicio": {
        "label": "💎 PARA SEMPRE SUA SUBMISSA 😈 – R$ 29,99",
        "link": "https://app.pushinpay.com.br/service/pay/9f5b0152-6bb7-4756-b813-2a3787c61382",
        "hours": None
    }
}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(p["label"], callback_data=k)] for k, p in PLANS.items()
    ]
    msg = (
        "Oi, amor 😘\n"
        "Eu tenho um cantinho VIP cheio de safadeza e submissão só pra você…\n"
        "Escolhe quanto tempo quer me ter todinha só pra você 😈"
    )
    update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

def handle_plan_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    plan_key = query.data
    plan = PLANS.get(plan_key)

    if not plan:
        query.answer("Plano inválido!", show_alert=True)
        return

    # Gera link com custom_data
    custom_json = json.dumps({"user_id": user_id, "plan": plan_key})
    encoded_custom = requests.utils.quote(custom_json)
    link = f"{plan['link']}?custom_data={encoded_custom}"

    msg = (
        "Delícia 😈 Aqui está seu link de pagamento:\n\n"
        f"{link}\n\n"
        "Assim que o pagamento for confirmado, eu mesma te coloco no canal VIP 😘"
    )
    context.bot.send_message(chat_id=user_id, text=msg)
    query.answer()

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/pushinpay-webhook", methods=["POST"])
def pushinpay_webhook():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
        
    print("WEBHOOK:", data, flush=True)

    status = data.get("status", "")
    custom_data = data.get("custom_data", {})
    user_id = custom_data.get("user_id")
    plan_key = custom_data.get("plan")

    if status == "CONFIRMED" and user_id and plan_key:
        try:
            bot.send_message(
                chat_id=int(user_id),
                text="🔥 Pagamento confirmado! Você será adicionado(a) ao canal VIP em instantes..."
            )
            bot.send_message(
                chat_id=int(user_id),
                text="Se não for adicionado automaticamente, entra por aqui:\nhttps://t.me/+neZ92gCjq51kYWMx"
            )
            print(f"✅ Acesso liberado para o user_id: {user_id}", flush=True)
        except Exception as e:
            print("Erro ao liberar acesso:", e, flush=True)

    return {"ok": True}

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(handle_plan_selection))

init_db()

def monitorar_expiracoes():
    while True:
        now = int(time.time())
        expiracoes = carregar_expiracoes()
        for user_id, plan, horas, timestamp in expiracoes:
            if horas is None:
                continue
            limite = timestamp + (horas * 3600)
            if now >= limite:
                try:
                    bot.kick_chat_member(chat_id=int(CHANNEL_ID), user_id=int(user_id))
                    remover_expiracao(user_id)
                    print(f"👢 Removido (retardatário) user {user_id}", flush=True)
                except Exception as e:
                    print("Erro ao expulsar:", e, flush=True)
        time.sleep(60)

threading.Thread(target=monitorar_expiracoes, daemon=True).start()

if __name__ == "__main__":
    print("🔥 Bot rodando com Pushinpay + SQLite + expulsão automática")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

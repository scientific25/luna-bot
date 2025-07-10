import sqlite3
import os

DB_PATH = "pagamentos.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expiracoes (
            user_id INTEGER,
            plan TEXT,
            horas INTEGER,
            timestamp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def salvar_expiracao(user_id, plan, horas):
    import time
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO expiracoes VALUES (?, ?, ?, ?)", (user_id, plan, horas, int(time.time())))
    conn.commit()
    conn.close()

def carregar_expiracoes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, plan, horas, timestamp FROM expiracoes")
    rows = c.fetchall()
    conn.close()
    return rows

def remover_expiracao(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM expiracoes WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
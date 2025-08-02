import logging
import sqlite3
from datetime import datetime

# Configuração básica do logger para console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Função para logar no console
def log_console(author, action, target=None, extra=None):
    message = f"Ação: {action} | Autor: {author} | Alvo: {target} | Extra: {extra}"
    logging.info(message)

# Função para logar em banco de dados SQLite
def log_event_to_db(author, action, target=None, extra=None):
    conn = sqlite3.connect("eventos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor TEXT,
            acao TEXT,
            alvo TEXT,
            extra TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO eventos_log (autor, acao, alvo, extra, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (str(author), action, str(target), str(extra), datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Função combinada para logar em ambos
def log_event(author, action, target=None, extra=None):
    log_console(author, action, target, extra)
    log_event_to_db(author, action, target, extra)
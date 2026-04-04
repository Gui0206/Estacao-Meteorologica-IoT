"""
Script para popular o banco de dados com leituras de exemplo.
Gera 50 leituras com dados realistas simulando 24h de coleta.
"""

import math
import random
from datetime import datetime, timedelta
from database import init_db, get_db_connection


def seed():
    init_db()
    conn = get_db_connection()

    # Limpa dados existentes para evitar duplicatas ao re-executar
    conn.execute('DELETE FROM leituras')
    conn.commit()

    agora = datetime.now()
    total = 50

    for i in range(total):
        # Distribui leituras nas últimas 24h
        minutos_atras = (total - i) * (24 * 60 // total)
        timestamp = agora - timedelta(minutes=minutos_atras)

        hora = timestamp.hour + timestamp.minute / 60.0

        # Temperatura: mais fria de madrugada, mais quente à tarde
        variacao_temp = 5 * math.sin((hora - 6) * math.pi / 12)
        temperatura = round(25.0 + variacao_temp + random.uniform(-1.5, 1.5), 1)

        # Umidade inversamente proporcional
        variacao_umid = -8 * math.sin((hora - 6) * math.pi / 12)
        umidade = round(60.0 + variacao_umid + random.uniform(-3, 3), 1)
        umidade = max(25, min(95, umidade))

        # Pressão com leve variação
        pressao = round(1013.25 + random.uniform(-5, 5), 1)

        conn.execute(
            'INSERT INTO leituras (temperatura, umidade, pressao, localizacao, timestamp) VALUES (?, ?, ?, ?, ?)',
            (temperatura, umidade, pressao, 'Lab', timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        )

    conn.commit()
    conn.close()
    print(f'{total} leituras inseridas com sucesso.')


if __name__ == '__main__':
    seed()

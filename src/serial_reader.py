"""
Leitor da porta serial do Arduino.
Lê dados JSON da serial e envia via POST para a API Flask.

Uso com hardware real:
    python serial_reader.py

Para simulação sem hardware, use o simulador:
    python simulador.py
"""

import serial
import json
import requests
import time
from config import PORTA_SERIAL, BAUD_RATE, API_URL


def ler_serial():
    url = f'{API_URL}/leituras'
    print(f'Conectando à porta {PORTA_SERIAL} ({BAUD_RATE} baud)...')
    print(f'Enviando dados para {url}')

    try:
        with serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=2) as ser:
            print('Conexão serial estabelecida. Aguardando dados...')
            while True:
                linha = ser.readline().decode('utf-8').strip()
                if linha:
                    try:
                        dados = json.loads(linha)
                        resp = requests.post(url, json=dados, timeout=5)
                        print(f'Enviado: {dados} → Status: {resp.status_code}')
                    except json.JSONDecodeError:
                        print(f'JSON inválido: {linha}')
                    except requests.RequestException as e:
                        print(f'Erro ao enviar para API: {e}')
                time.sleep(0.1)
    except serial.SerialException as e:
        print(f'Erro na conexão serial: {e}')
        print('Verifique se o Arduino está conectado e a porta está correta.')
        print(f'Porta configurada: {PORTA_SERIAL}')


if __name__ == '__main__':
    ler_serial()

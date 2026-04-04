"""
Simulador de estação meteorológica.
Gera dados realistas de temperatura, umidade e pressão atmosférica
e envia via POST para a API Flask, substituindo o Arduino físico.
"""

import random
import math
import time
import requests
from config import API_URL, INTERVALO_SIMULACAO


# Valores base para simulação realista (clima tropical brasileiro)
TEMP_BASE = 25.0
UMID_BASE = 60.0
PRESS_BASE = 1013.25


def gerar_leitura(hora_simulada):
    """Gera uma leitura com variação realista baseada na hora do dia."""
    # Variação senoidal de temperatura ao longo do dia
    variacao_temp = 5 * math.sin((hora_simulada - 6) * math.pi / 12)
    temperatura = round(TEMP_BASE + variacao_temp + random.uniform(-1.5, 1.5), 1)

    # Umidade inversamente proporcional à temperatura
    variacao_umid = -8 * math.sin((hora_simulada - 6) * math.pi / 12)
    umidade = round(UMID_BASE + variacao_umid + random.uniform(-3, 3), 1)
    umidade = max(20, min(95, umidade))

    # Pressão atmosférica com pequena variação
    pressao = round(PRESS_BASE + random.uniform(-5, 5), 1)

    return {
        'temperatura': temperatura,
        'umidade': umidade,
        'pressao': pressao
    }


def main():
    url = f'{API_URL}/leituras'
    hora = 0.0
    print(f'Simulador de estação meteorológica iniciado')
    print(f'Enviando dados para {url} a cada {INTERVALO_SIMULACAO}s')
    print('Pressione Ctrl+C para parar\n')

    try:
        while True:
            dados = gerar_leitura(hora % 24)
            try:
                resp = requests.post(url, json=dados, timeout=5)
                status = '✓' if resp.status_code == 201 else f'✗ {resp.status_code}'
                print(f'[{status}] Temp: {dados["temperatura"]}°C | '
                      f'Umid: {dados["umidade"]}% | '
                      f'Press: {dados["pressao"]} hPa')
            except requests.RequestException as e:
                print(f'Erro de conexão: {e}')

            hora += INTERVALO_SIMULACAO / 3600  # avança o tempo simulado
            time.sleep(INTERVALO_SIMULACAO)
    except KeyboardInterrupt:
        print('\nSimulador encerrado.')


if __name__ == '__main__':
    main()

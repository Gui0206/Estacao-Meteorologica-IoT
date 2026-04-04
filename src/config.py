import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'dados.db')

# Configurações da porta serial (usado apenas com hardware real)
PORTA_SERIAL = os.environ.get('PORTA_SERIAL', '/dev/ttyUSB0')
BAUD_RATE = int(os.environ.get('BAUD_RATE', 9600))

# URL da API
API_URL = os.environ.get('API_URL', 'http://localhost:5001')

# Intervalo de envio do simulador (segundos)
INTERVALO_SIMULACAO = int(os.environ.get('INTERVALO_SIMULACAO', 5))

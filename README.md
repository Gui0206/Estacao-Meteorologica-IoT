# Estacao Meteorologica IoT

Sistema de medicao de estacao meteorologica IoT desenvolvido para o Modulo 5 de Engenharia de Computacao.

## Decisoes de Arquitetura

- **Simulacao em Python**: como nao ha hardware fisico disponivel, o Arduino e os sensores sao substituidos por um **simulador Python** (`simulador.py`) que gera dados realistas de temperatura, umidade e pressao atmosferica com variacao senoidal ao longo do dia.
- **Sketch Arduino incluso**: o arquivo `arduino/estacao.ino` esta incluido como referencia para uso com hardware real (Arduino Uno + DHT11).
- **Leitura serial disponivel**: o script `serial_reader.py` esta pronto para uso com hardware real, lendo dados JSON da porta serial e enviando via POST para a API.
- **Arquitetura mantida**: Flask + SQLite + Jinja2 conforme especificado, com WAL mode para suportar escritas concorrentes do simulador e da API.

## Estrutura do Projeto

```
src/
├── app.py                 # Aplicacao Flask principal
├── database.py            # Funcoes de acesso ao SQLite
├── config.py              # Configuracoes (porta, URL, intervalos)
├── serial_reader.py       # Leitura da porta serial do Arduino
├── simulador.py           # Simulador de sensores (substitui Arduino)
├── seed.py                # Script para popular o banco com dados de exemplo
├── schema.sql             # Script de criacao do banco
├── requirements.txt       # Dependencias Python
├── dados.db               # Banco SQLite com 50+ leituras de exemplo
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js        # Grafico Chart.js e interacoes
├── templates/
│   ├── base.html          # Template base com navbar
│   ├── index.html         # Painel principal / dashboard
│   ├── historico.html      # Listagem com paginacao
│   └── editar.html        # Formulario de edicao
└── arduino/
    └── estacao.ino         # Sketch do Arduino (referencia)
```

## Requisitos

- Python 3.10 ou superior
- Navegador web moderno

## Instalacao e Execucao

### 1. Criar ambiente virtual e instalar dependencias

```bash
cd src
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 2. Inicializar o banco de dados com dados de exemplo

```bash
python seed.py
```

Isso cria o arquivo `dados.db` com 50 leituras de exemplo.

### 3. Iniciar o servidor Flask

```bash
python app.py
```

O servidor inicia em `http://localhost:5000`.

### 4. (Opcional) Iniciar o simulador de sensores

Em outro terminal, com o ambiente virtual ativo:

```bash
python simulador.py
```

O simulador envia dados para a API a cada 5 segundos, simulando leituras de uma estacao meteorologica real.

### 5. (Opcional) Uso com hardware real

Conecte o Arduino com o sketch `estacao.ino` carregado e execute:

```bash
PORTA_SERIAL=/dev/ttyUSB0 python serial_reader.py
```

## Rotas da API

| Metodo | Rota               | Descricao                                    |
|--------|---------------------|----------------------------------------------|
| GET    | `/`                 | Painel principal com ultimas 10 leituras      |
| GET    | `/leituras`         | Historico completo com paginacao              |
| POST   | `/leituras`         | Recebe JSON com nova leitura                  |
| GET    | `/leituras/<id>`    | Exibe/edita uma leitura especifica            |
| PUT    | `/leituras/<id>`    | Atualiza campos de uma leitura                |
| DELETE | `/leituras/<id>`    | Remove uma leitura                            |
| GET    | `/api/estatisticas` | Media, minimo e maximo de temperatura/umidade |

Adicione `?formato=json` em qualquer rota GET para receber a resposta em JSON.

### Exemplo de uso com curl

```bash
# Criar leitura
curl -X POST http://localhost:5000/leituras \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 25.3, "umidade": 62.1, "pressao": 1013.5}'

# Listar (JSON)
curl http://localhost:5000/leituras?formato=json

# Atualizar
curl -X PUT http://localhost:5000/leituras/1 \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 26.0}'

# Deletar
curl -X DELETE http://localhost:5000/leituras/1

# Estatisticas
curl http://localhost:5000/api/estatisticas
```

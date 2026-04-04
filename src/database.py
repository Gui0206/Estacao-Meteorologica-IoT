import sqlite3
import os
from config import DATABASE, BASE_DIR


def get_db_connection():
    """Retorna uma conexão configurada com o banco SQLite."""
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas se não existirem."""
    conn = get_db_connection()
    schema_path = os.path.join(BASE_DIR, 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.close()


def inserir_leitura(temperatura, umidade, pressao=None, localizacao='Lab'):
    """Insere uma nova leitura no banco e retorna o ID."""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO leituras (temperatura, umidade, pressao, localizacao) VALUES (?, ?, ?, ?)',
        (temperatura, umidade, pressao, localizacao)
    )
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()
    return id_novo


def listar_leituras(limite=50, offset=0):
    """Retorna leituras com paginação, ordenadas da mais recente para a mais antiga."""
    conn = get_db_connection()
    leituras = conn.execute(
        'SELECT * FROM leituras ORDER BY id DESC LIMIT ? OFFSET ?',
        (limite, offset)
    ).fetchall()
    conn.close()
    return [dict(l) for l in leituras]


def contar_leituras():
    """Retorna o total de leituras no banco."""
    conn = get_db_connection()
    total = conn.execute('SELECT COUNT(*) FROM leituras').fetchone()[0]
    conn.close()
    return total


def buscar_leitura(id):
    """Retorna uma leitura específica pelo ID."""
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    if leitura:
        return dict(leitura)
    return None


def atualizar_leitura(id, dados):
    """Atualiza os campos de uma leitura existente."""
    campos = []
    valores = []
    for campo in ['temperatura', 'umidade', 'pressao', 'localizacao']:
        if campo in dados:
            campos.append(f'{campo} = ?')
            valores.append(dados[campo])

    if not campos:
        return False

    valores.append(id)
    conn = get_db_connection()
    result = conn.execute(
        f'UPDATE leituras SET {", ".join(campos)} WHERE id = ?',
        valores
    )
    conn.commit()
    alterado = result.rowcount > 0
    conn.close()
    return alterado


def deletar_leitura(id):
    """Remove uma leitura do banco."""
    conn = get_db_connection()
    result = conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    removido = result.rowcount > 0
    conn.close()
    return removido


def estatisticas():
    """Retorna média, mínimo e máximo de temperatura, umidade e pressão."""
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT
            COUNT(*) as total,
            ROUND(AVG(temperatura), 1) as temp_media,
            ROUND(MIN(temperatura), 1) as temp_min,
            ROUND(MAX(temperatura), 1) as temp_max,
            ROUND(AVG(umidade), 1) as umid_media,
            ROUND(MIN(umidade), 1) as umid_min,
            ROUND(MAX(umidade), 1) as umid_max,
            ROUND(AVG(pressao), 1) as press_media,
            ROUND(MIN(pressao), 1) as press_min,
            ROUND(MAX(pressao), 1) as press_max
        FROM leituras
    ''').fetchone()
    conn.close()
    return dict(stats)

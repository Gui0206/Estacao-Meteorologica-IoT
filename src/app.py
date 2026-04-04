from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import (
    init_db, inserir_leitura, listar_leituras, buscar_leitura,
    atualizar_leitura, deletar_leitura, estatisticas, contar_leituras
)

app = Flask(__name__)


@app.route('/')
def index():
    """Painel principal — últimas 10 leituras."""
    leituras = listar_leituras(limite=10)
    stats = estatisticas()
    if request.args.get('formato') == 'json':
        return jsonify({'leituras': leituras, 'estatisticas': stats})
    return render_template('index.html', leituras=leituras, stats=stats)


@app.route('/leituras', methods=['GET'])
def listar():
    """Histórico completo com paginação."""
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 20, type=int)
    offset = (pagina - 1) * por_pagina

    leituras = listar_leituras(limite=por_pagina, offset=offset)
    total = contar_leituras()
    total_paginas = (total + por_pagina - 1) // por_pagina

    if request.args.get('formato') == 'json':
        return jsonify({
            'leituras': leituras,
            'pagina': pagina,
            'total_paginas': total_paginas,
            'total': total
        })
    return render_template(
        'historico.html',
        leituras=leituras,
        pagina=pagina,
        total_paginas=total_paginas,
        total=total
    )


@app.route('/leituras', methods=['POST'])
def criar():
    """Recebe JSON do Arduino / simulador."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    temperatura = dados.get('temperatura')
    umidade = dados.get('umidade')

    if temperatura is None or umidade is None:
        return jsonify({'erro': 'temperatura e umidade são obrigatórios'}), 400

    id_novo = inserir_leitura(
        temperatura,
        umidade,
        dados.get('pressao'),
        dados.get('localizacao', 'Lab')
    )
    return jsonify({'id': id_novo, 'status': 'criado'}), 201


@app.route('/leituras/<int:id>', methods=['GET'])
def detalhe(id):
    """Exibe uma leitura específica."""
    leitura = buscar_leitura(id)
    if not leitura:
        return jsonify({'erro': 'Leitura não encontrada'}), 404

    if request.args.get('formato') == 'json':
        return jsonify(leitura)
    return render_template('editar.html', leitura=leitura)


@app.route('/leituras/<int:id>', methods=['PUT'])
def atualizar(id):
    """Atualiza campos de uma leitura."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    if not buscar_leitura(id):
        return jsonify({'erro': 'Leitura não encontrada'}), 404

    atualizar_leitura(id, dados)
    return jsonify({'status': 'atualizado'})


@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar(id):
    """Remove uma leitura do banco."""
    if not buscar_leitura(id):
        return jsonify({'erro': 'Leitura não encontrada'}), 404

    deletar_leitura(id)
    return jsonify({'status': 'removido'})


@app.route('/api/estatisticas')
def api_estatisticas():
    """Média, mín e máx do período."""
    stats = estatisticas()
    return jsonify(stats)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)

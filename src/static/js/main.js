let graficoTemporal = null;

function inicializarGrafico(leituras) {
    const ctx = document.getElementById('grafico-temporal');
    if (!ctx) return;

    const labels = leituras.map(l => l.timestamp ? l.timestamp.slice(11, 19) : '');
    const temperaturas = leituras.map(l => l.temperatura);
    const umidades = leituras.map(l => l.umidade);
    const pressoes = leituras.map(l => l.pressao);

    graficoTemporal = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperatura (°C)',
                    data: temperaturas,
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3
                },
                {
                    label: 'Umidade (%)',
                    data: umidades,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3
                },
                {
                    label: 'Pressão (hPa)',
                    data: pressoes,
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Temp (°C) / Umidade (%)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Pressão (hPa)' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

function atualizarDados() {
    const btn = document.getElementById('btn-atualizar');
    if (btn) {
        btn.textContent = 'Atualizando...';
        btn.disabled = true;
    }

    fetch('/?formato=json')
        .then(resp => resp.json())
        .then(data => {
            atualizarTabela(data.leituras);
            atualizarGrafico(data.leituras.slice().reverse());
            if (btn) {
                btn.textContent = 'Atualizar';
                btn.disabled = false;
            }
        })
        .catch(() => {
            if (btn) {
                btn.textContent = 'Atualizar';
                btn.disabled = false;
            }
        });
}

function atualizarTabela(leituras) {
    const tbody = document.querySelector('#tabela-leituras tbody');
    if (!tbody) return;

    if (leituras.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty">Nenhuma leitura registrada.</td></tr>';
        return;
    }

    tbody.innerHTML = leituras.map(l => `
        <tr>
            <td>${l.id}</td>
            <td>${l.temperatura}°C</td>
            <td>${l.umidade}%</td>
            <td>${l.pressao ? l.pressao + ' hPa' : '--'}</td>
            <td>${l.localizacao}</td>
            <td>${l.timestamp}</td>
        </tr>
    `).join('');
}

function atualizarGrafico(leituras) {
    if (!graficoTemporal) return;

    graficoTemporal.data.labels = leituras.map(l => l.timestamp ? l.timestamp.slice(11, 19) : '');
    graficoTemporal.data.datasets[0].data = leituras.map(l => l.temperatura);
    graficoTemporal.data.datasets[1].data = leituras.map(l => l.umidade);
    graficoTemporal.data.datasets[2].data = leituras.map(l => l.pressao);
    graficoTemporal.update();
}

function deletarLeitura(id) {
    if (!confirm('Tem certeza que deseja excluir a leitura #' + id + '?')) return;

    fetch('/leituras/' + id, { method: 'DELETE' })
        .then(resp => resp.json())
        .then(data => {
            if (data.status === 'removido') {
                const row = document.getElementById('row-' + id);
                if (row) row.remove();
            } else {
                alert('Erro ao excluir: ' + (data.erro || 'desconhecido'));
            }
        });
}

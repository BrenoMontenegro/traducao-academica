document.addEventListener('DOMContentLoaded', function () {
    //Aqui, deixei a lógica de geração do gráfico
    if (!document.getElementById('tempo-total') || !document.getElementById('graficoEstudo')) {
        console.warn('Elementos não encontrados. O script de dashboard não será executado.');
        return;
    }

    const tempoSpan = document.getElementById('tempo-total');
    const ctx = document.getElementById('graficoEstudo').getContext('2d');

    let dadosHistoricos = [0];
    let labelsHistoricos = ['Agora'];

    const grafico = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labelsHistoricos,
            datasets: [{
                label: 'Minutos Estudados',
                data: dadosHistoricos,
                borderColor: '#00FFAA',
                backgroundColor: 'rgba(0, 255, 170, 0.2)',
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            animation: false
        }
    });

    function atualizarTempo() {
        fetch('/tempo-estudo-ao-vivo/')
            .then(response => response.json())
            .then(data => {
                const minutos = data.tempo_total;
                tempoSpan.textContent = minutos;
                
            fetch('/obter_tempo_estudado_hoje/')
                .then(res => res.json())
                .then(data => {
                    const spanHoje = document.getElementById('tempo-hoje');
                    if (spanHoje) {
                        spanHoje.textContent = `${data.tempo_estudado_hoje} min`;
                    }
                });
                
            document.querySelectorAll('.meta-progresso').forEach(barra => {
                const tempoMeta = parseFloat(barra.dataset.meta);
                if (tempoMeta > 0) {
                    const progresso = Math.min(100, Math.round((minutos / tempoMeta) * 100));
                    barra.style.width = progresso + '%';
                }
            });
            
                const hora = new Date().toLocaleTimeString();
                dadosHistoricos.push(minutos);
                labelsHistoricos.push(hora);

                if (dadosHistoricos.length > 10) {
                    dadosHistoricos.shift();
                    labelsHistoricos.shift();
                }

                grafico.update();
            
            const spansFeito = document.querySelectorAll('.feito-meta');
            spansFeito.forEach(span => {
            span.textContent = minutos;
            });

        });
    }

    atualizarTempo();
    setInterval(atualizarTempo, 5000);
    
    //Aqui, eu deixei a lógica do botão flutuante que faz aparecer o widget
    
    const botao = document.getElementById('toggleForm');
    const widget = document.getElementById('metaForm');

    if(botao && widget) {
        botao.addEventListener('click', function (e) {
            e.stopPropagation();
            widget.style.display = (widget.style.display === 'block') ? 'none' : 'block';
        });

        document.addEventListener('click', function (e) {
            if (!widget.contains(e.target) && e.target !== botao) {
                widget.style.display = 'none';
            }
        });
    }
    
    const graficoSemanalCanvas = document.getElementById('graficoSemanal');
    if (graficoSemanalCanvas) {
    const ctxSemanal = graficoSemanalCanvas.getContext('2d');
    const dias = JSON.parse(graficoSemanalCanvas.dataset.labels);
    const minutos = JSON.parse(graficoSemanalCanvas.dataset.valores);

    new Chart(ctxSemanal, {
        type: 'bar',
        data: {
            labels: dias,
            datasets: [{
                label: 'Minutos por dia',
                data: minutos,
                backgroundColor: '#00FFAA',
                borderRadius: 8
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
});

function confirmar() {
    return confirm("Tem certeza que deseja zerar todo o progresso?");
}
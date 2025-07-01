document.addEventListener('DOMContentLoaded', function () {
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

                const hora = new Date().toLocaleTimeString();
                dadosHistoricos.push(minutos);
                labelsHistoricos.push(hora);

                if (dadosHistoricos.length > 10) {
                    dadosHistoricos.shift();
                    labelsHistoricos.shift();
                }

                grafico.update();
            });
    }

    atualizarTempo();
    setInterval(atualizarTempo, 5000);
});

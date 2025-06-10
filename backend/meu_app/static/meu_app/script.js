document.addEventListener('DOMContentLoaded', function () {
            const modal = document.getElementById('modalConfirmacao');
            const form = document.getElementById('form-deletar-modal');
            const tituloSpan = document.getElementById('titulo-resumo');
        
            modal.addEventListener('show.bs.modal', function (event) {
                const botao = event.relatedTarget;
                const resumoId = botao.getAttribute('data-resumo-id');
                const tituloResumo = botao.getAttribute('data-titulo');
        
                form.action = `/deletar-resumo/${resumoId}/`;
                tituloSpan.textContent = `"${tituloResumo}"`;
            });
            
            const toggleButton = document.getElementById('toggle-darkmode');
            const body = document.body;
            
                
            if (localStorage.getItem('modo') === 'dark') {
                body.classList.add('dark-mode');
                toggleButton.textContent = '☀️';
            }
            
            toggleButton.addEventListener('click', () => {
              body.classList.toggle('dark-mode');
              const escureceu = body.classList.contains('dark-mode');
              toggleButton.textContent = escureceu ? '☀️' : '🌙';
              localStorage.setItem('modo', escureceu ? 'dark' : 'light');
            });
        });
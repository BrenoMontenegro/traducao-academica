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
        });
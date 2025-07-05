document.querySelectorAll('.cartao-kanban').forEach(card => {
    card.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', card.dataset.id);
        card.classList.add('arrastando');
    });

    card.addEventListener('dragend', (e) => {
        card.classList.remove('arrastando');
    });
});

document.querySelectorAll('.coluna-kanban').forEach(coluna => {
    coluna.addEventListener('dragover', (e) => {
        e.preventDefault();
        coluna.classList.add('drop-zone');
    });

    coluna.addEventListener('dragleave', () => {
        coluna.classList.remove('drop-zone');
    });

    coluna.addEventListener('drop', (e) => {
        e.preventDefault();
        coluna.classList.remove('drop-zone');
        
        const tarefaId = e.dataTransfer.getData('text/plain');
        const novoStatus = coluna.getAttribute('data-status');

        fetch(`/tarefas/${tarefaId}/mover/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: novoStatus })
        }).then(() => {
            window.location.reload(); 
        });
    });
});

document.querySelectorAll('.cartao-kanban').forEach(card => {
    card.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', card.dataset.id);
        card.classList.add('arrastando');
    });

    card.addEventListener('dragend', e => {
        card.classList.remove('arrastando');
    });
});

document.querySelectorAll('.coluna-kanban').forEach(coluna => {
    coluna.addEventListener('dragover', e => {
        e.preventDefault();
        coluna.classList.add('drop-zone');
    });

    coluna.addEventListener('dragleave', () => {
        coluna.classList.remove('drop-zone');
    });

    coluna.addEventListener('drop', e => {
        e.preventDefault();
        coluna.classList.remove('drop-zone');

        const tarefaId = e.dataTransfer.getData('text/plain');
        const novaColuna = coluna;
        const novoStatus = novaColuna.getAttribute('data-status');

        const card = document.querySelector(`.cartao-kanban[data-id='${tarefaId}']`);
        novaColuna.appendChild(card);  

        fetch('/atualizar-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken()
            },
            body: `id=${tarefaId}&status=${novoStatus}`
        }).then(res => res.json())
          .then(data => {
              if (!data.success) {
                  alert("Erro ao atualizar status da tarefa!");
              }
          });
    });
});

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const c = cookies[i].trim();
        if (c.startsWith(name + '=')) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return '';
}

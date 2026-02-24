async function carregarAlunos() {
    const response = await fetch('/api/alunos');
    const alunos = await response.json();
    const tabela = document.getElementById('tabelaAlunos');
    tabela.innerHTML = '';

    alunos.forEach(aluno => {
        const status = aluno.nota >= 7 ? 'Aprovado' : 'Reprovado';
        const classe = aluno.nota >= 7 ? 'aprovado' : 'reprovado';
        
        tabela.innerHTML += `
            <tr>
                <td>${aluno.nome}</td>
                <td>${aluno.nota}</td>
                <td class="${classe}">${status}</td>
            </tr>
        `;
    });
}

async function salvarAluno() {
    const nome = document.getElementById('nome').value;
    const nota = document.getElementById('nota').value;

    if(!nome || !nota) return alert("Preencha tudo!");

    await fetch('/cadastrar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ nome, nota: parseFloat(nota) })
    });

    document.getElementById('nome').value = '';
    document.getElementById('nota').value = '';
    carregarAlunos();
}

carregarAlunos();

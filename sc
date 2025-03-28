document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Obter valores dos campos
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value;
    const area = document.getElementById('area').value;

    // Validar os dados (exemplo básico)
    if (!nome || !email || !telefone || !area) {
        alert('Por favor, preencha todos os campos.');
        return;
    }

    // Aqui você pode adicionar a lógica para enviar os dados para um servidor ou armazená-los localmente
    console.log('Dados do voluntário:', { nome, email, telefone, area });

    // Limpar o formulário após o envio
    document.getElementById('cadastroForm').reset();
});
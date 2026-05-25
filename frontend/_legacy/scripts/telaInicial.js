// Gerenciar tema claro/escuro
const html = document.documentElement;
const sunIcon = document.getElementById('sun-icon');
const moonIcon = document.getElementById('moon-icon');

// Gerenciar abas de login/cadastro
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const submitBtn = document.getElementById('submit-btn');
let currentTab = 'login';

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
    const tab = btn.getAttribute('data-tab');
                
    // Atualizar conteúdo
    tabContents.forEach(content => content.classList.add('hidden'));
    document.getElementById(`${tab}-content`).classList.remove('hidden');
                
    // Atualizar estilo dos botões
    tabBtns.forEach(b => {
        b.classList.remove('bg-white', 'dark:bg-gray-700', 'text-gray-900', 'dark:text-white', 'shadow-sm');
        b.classList.add('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-200');
    });

    btn.classList.remove('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-200');
    btn.classList.add('bg-white', 'dark:bg-gray-700', 'text-gray-900', 'dark:text-white', 'shadow-sm');
                
    // Atualizar botão de submit
    currentTab = tab;
    submitBtn.textContent = tab === 'login' ? 'Entrar' : 'Criar Conta';
    });
});

// Manipular envio do formulário
document.getElementById('auth-form').addEventListener('submit', (e) => {
    e.preventDefault();
    console.log(`Formulário de ${currentTab} enviado`);
    // Adicionar lógica de API aqui
});

// Inicializar
initializeTheme();
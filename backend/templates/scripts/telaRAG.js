const searchButton = document.getElementById('searchButton');
const searchInput = document.getElementById('searchInput');
const results = document.getElementById('results');

searchButton.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (!query) {
        results.innerHTML = '<div class="empty-state">Digite um termo de pesquisa para buscar jogos.</div>';
        return;
    }

    results.innerHTML = '<div class="empty-state">Buscando jogos para "' + query + '"...</div>';
    // Aqui você pode integrar com sua API ou backend para obter os resultados reais.
    });

searchInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        searchButton.click();
    }
});
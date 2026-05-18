const themeToggle = document.getElementById('theme-toggle');


// Carregar tema salvo ou usar preferência do sistema
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            
    if (savedTheme) {
        if (savedTheme === 'dark') {
            html.classList.add('dark');
        }
    } else if (prefersDark) {
        html.classList.add('dark');
    }    
        updateThemeIcons();
    }

function updateThemeIcons() {
    if (html.classList.contains('dark')) {
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
    } else {
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
    }
}

themeToggle.addEventListener('click', () => {
    html.classList.toggle('dark');
    const isDark = html.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcons();
});
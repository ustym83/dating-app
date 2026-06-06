document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-checkbox'); // Updated to new checkbox ID
    const body = document.getElementById('theme-body');

    // Load saved theme preference
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark-mode') {
        body.classList.add('dark-mode');
        themeToggle.checked = true; // Set checkbox to checked if dark mode
    } else {
        // Default to light mode if no preference is set or if it's explicitly light-mode
        body.classList.add('light-mode');
        themeToggle.checked = false;
    }

    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) { // Check if the checkbox is checked
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });
});
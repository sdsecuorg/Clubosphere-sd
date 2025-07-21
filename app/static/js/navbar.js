// File containing scripts for the navbar


document.addEventListener("DOMContentLoaded", function(event){
    const openMenuBtn = document.getElementById('openMenu');
    const closeMenuBtn = document.getElementById('closeMenu');
    const sidebar = document.getElementById('sidebar');
    openMenuBtn.addEventListener('click', () => {
        sidebar.classList.add('active');
        openMenuBtn.classList.add('hidden');
    });

    closeMenuBtn.addEventListener('click', () => {
        sidebar.classList.remove('active');
        openMenuBtn.classList.remove('hidden');
    });
})
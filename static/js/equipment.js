// Dynamic Client-side Filtering for Equipment Marketplace
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const locationFilter = document.getElementById('locationFilter');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const catPills = document.querySelectorAll('.cat-pill');
    const equipmentItems = document.querySelectorAll('.equipment-item');
    const noResults = document.getElementById('noResults');

    function filterItems() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const selectedCat = categoryFilter.value;
        const selectedLoc = locationFilter.value;
        let visibleCount = 0;

        equipmentItems.forEach(item => {
            const name = item.getAttribute('data-name');
            const category = item.getAttribute('data-category');
            const location = item.getAttribute('data-location');

            const matchesSearch = !searchTerm || name.includes(searchTerm);
            const matchesCat = selectedCat === 'All' || category === selectedCat;
            const matchesLoc = selectedLoc === 'All' || location === selectedLoc;

            if (matchesSearch && matchesCat && matchesLoc) {
                item.classList.remove('d-none');
                visibleCount++;
            } else {
                item.classList.add('d-none');
            }
        });

        if (visibleCount === 0) {
            noResults.classList.remove('d-none');
        } else {
            noResults.classList.add('d-none');
        }
    }

    if (searchInput) searchInput.addEventListener('input', filterItems);
    if (categoryFilter) categoryFilter.addEventListener('change', (e) => {
        const catVal = e.target.value;
        catPills.forEach(pill => {
            pill.classList.toggle('active', pill.getAttribute('data-cat') === catVal);
        });
        filterItems();
    });

    if (locationFilter) locationFilter.addEventListener('change', filterItems);

    catPills.forEach(pill => {
        pill.addEventListener('click', () => {
            catPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const selectedCat = pill.getAttribute('data-cat');
            categoryFilter.value = selectedCat;
            filterItems();
        });
    });

    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', () => {
            searchInput.value = '';
            categoryFilter.value = 'All';
            locationFilter.value = 'All';
            catPills.forEach((p, idx) => p.classList.toggle('active', idx === 0));
            filterItems();
        });
    }
});

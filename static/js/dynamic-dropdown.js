document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('categorySelect');
    const subcategorySelect = document.getElementById('subcategorySelect');

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const categoryId = this.value;

            fetch(`/api/subcategories/${categoryId}/`) // Your endpoint here
            .then(response => response.json())
            .then(data => {
                subcategorySelect.innerHTML = ''; // Clear existing options
                data.subcategories.forEach(sub => {
                    const option = document.createElement('option');
                    option.value = sub.id;
                    option.textContent = sub.name;
                    subcategorySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
        });
    }
});

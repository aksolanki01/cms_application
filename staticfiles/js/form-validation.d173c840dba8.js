document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let valid = true;
            const inputs = form.querySelectorAll('input[required]');

            inputs.forEach(input => {
                if (!input.value) {
                    valid = false;
                    input.classList.add('is-invalid'); // Bootstrap class for invalid input
                    const error = document.createElement('div');
                    error.className = 'invalid-feedback';
                    error.innerText = `${input.name} is required.`;
                    input.parentNode.appendChild(error);
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                event.preventDefault(); // Prevent form submission if not valid
            }
        });
    });
});

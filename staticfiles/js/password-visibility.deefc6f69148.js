document.addEventListener('DOMContentLoaded', function() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    const toggleButtons = document.querySelectorAll('.toggle-password');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            passwordFields.forEach(field => {
                if (field.type === "password") {
                    field.type = "text";
                    button.textContent = 'Hide';
                } else {
                    field.type = "password";
                    button.textContent = 'Show';
                }
            });
        });
    });
});

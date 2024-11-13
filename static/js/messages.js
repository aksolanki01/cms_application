document.addEventListener('DOMContentLoaded', function() {
    const messageBox = document.getElementById('messageBox');

    if (messageBox) {
        setTimeout(() => {
            messageBox.style.display = 'none'; // Automatically hide after 3 seconds
        }, 3000);
    }
});

// Example: Dynamic form submission handling
document.addEventListener('DOMContentLoaded', function() {
    // Example for the like button toggle
    const likeButton = document.getElementById('like_button');
    if (likeButton) {
        likeButton.addEventListener('click', function() {
            const postSlug = likeButton.getAttribute('data-post-slug');
            fetch(`/like/${postSlug}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Get CSRF token
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update the likes count and button text based on response
                document.getElementById('likes_count').innerText = data.likes_count;
                likeButton.innerText = data.liked ? 'Unlike' : 'Like';
            })
            .catch(error => console.error('Error:', error));
        });
    }
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

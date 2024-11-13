document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.getElementById('like_button');

    if (likeButton) {
        likeButton.addEventListener('click', function() {
            fetch(likeButton.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': likeButton.dataset.csrf,
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('likes_count').innerText = data.likes_count;
                likeButton.innerText = data.liked ? 'Unlike' : 'Like';
                likeButton.classList.toggle('btn-secondary'); // Change button style
                likeButton.classList.toggle('btn-danger');
            })
            .catch(error => console.error('Error:', error));
        });
    }
});

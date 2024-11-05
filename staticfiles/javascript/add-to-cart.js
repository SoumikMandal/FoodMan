document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.place-order a').addEventListener('click', function(event) {
        event.preventDefault();

        const name = document.querySelector('.details input[placeholder="Enter name"]').value;
        const address = document.querySelector('.details input[placeholder="Enter place to deliver at"]').value;
        const placeOrderUrl = this.getAttribute('data-url');

        if (!name || !address) {
            alert("Please fill in all fields.");
            return;
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        const data = { name, address };

        fetch(placeOrderUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


function acceptOrder(orderId) {

    disableButtons(orderId);

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/accept-order/${orderId}/`;

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCookie('csrftoken');
    
    form.appendChild(csrfInput);
    document.body.appendChild(form);
    form.submit();
}

function rejectOrder(orderId) {
    const dropdown = document.querySelector(`#reject-dropdown-${orderId}`);
    const reason = dropdown.value;

    disableButtons(orderId);

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/reject-order/${orderId}/`;

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCookie('csrftoken');
    
    const reasonInput = document.createElement('input');
    reasonInput.type = 'hidden';
    reasonInput.name = 'reason';
    reasonInput.value = reason;

    form.appendChild(csrfInput);
    form.appendChild(reasonInput);
    document.body.appendChild(form);
    form.submit();
}

function disableButtons(orderId) {
    const acceptButton = document.querySelector(`#accept-btn-${orderId}`);
    const rejectButton = document.querySelector(`#reject-btn-${orderId}`);
    const dropdown = document.querySelector(`#reject-dropdown-${orderId}`);

    if (acceptButton) acceptButton.style.display = 'none';
    if (rejectButton) rejectButton.style.display = 'none';
    if (dropdown) dropdown.style.display = 'none';
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


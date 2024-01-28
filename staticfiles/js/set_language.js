function changeLanguage(languageCode) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Get CSRF token

    fetch("{% url 'set_language' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `language=${languageCode}&next=${window.location.href}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_to;
        } else {
            // Handle any errors
            console.error("Language change failed:", data.error);
        }
    })
    .catch(error => {
        console.error("Error during language change:", error);
    });
}

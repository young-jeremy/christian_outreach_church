// Initialize TinyMCE for rich text editing
tinymce.init({
    selector: '.rich-text-editor',
    plugins: 'link image code table lists',
    toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image',
    height: 300
});

// File upload preview
document.querySelectorAll('.custom-file-input').forEach(input => {
    input.addEventListener('change', function (e) {
        const fileName = e.target.files[0].name;
        const label = e.target.nextElementSibling;
        label.textContent = fileName;
    });
});

// Dynamic form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function (e) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});

// Progress tracking
function updateProgress(lessonId, complete) {
    fetch(`/api/progress/update/${lessonId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({complete})
    })
        .then(response => response.json())
        .then(data => {
            const progressElement = document.querySelector(`#progress-${lessonId}`);
            progressElement.className = `progress-circle ${complete ? 'progress-complete' : 'progress-incomplete'}`;
        });
}

// CSRF Token helper
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
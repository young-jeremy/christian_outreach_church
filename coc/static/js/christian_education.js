// Course Progress Tracking
function updateProgress(courseId, moduleId) {
    fetch(`/api/courses/${courseId}/modules/${moduleId}/complete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateProgressUI(courseId, data.progress);
            }
        })
        .catch(error => console.error('Error:', error));
}

function updateProgressUI(courseId, progress) {
    const progressBar = document.querySelector(`#course-${courseId} .progress-bar`);
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.textContent = `${progress}%`;
    }
}

// Discussion Board Features
function previewPost() {
    const content = document.getElementById('id_content').value;
    const preview = document.getElementById('preview-content');
    if (preview) {
        // Basic markdown-like formatting
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
        preview.innerHTML = formatted;
    }
}

// File Upload Preview
function previewFile(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('file-preview');
            if (preview) {
                if (input.files[0].type.startsWith('image/')) {
                    preview.innerHTML = `<img src="${e.target.result}" class="img-fluid">`;
                } else {
                    preview.innerHTML = `<p>File selected: ${input.files[0].name}</p>`;
                }
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Certificate Generation
function generateCertificate(enrollmentId) {
    fetch(`/api/enrollments/${enrollmentId}/certificate/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'certificate.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
}

// CSRF Token Helper
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

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function () {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add event listeners for discussion preview
    const contentField = document.getElementById('id_content');
    if (contentField) {
        contentField.addEventListener('input', previewPost);
    }

    // Add event listeners for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function () {
            previewFile(this);
        });
    });
});
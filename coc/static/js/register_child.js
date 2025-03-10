function registerChildForEvent(eventId, childId) {
    console.log(`Sending registration request for child ${childId} to event ${eventId}`);

    if (!childId || childId <= 0) {
        alert("Error: Invalid child ID. Please try again.");
        return;
    }

    $.ajax({
        // Update this URL to match your pattern
        url: `/services/childrens/program/${eventId}/register/`,
        type: 'POST',
        data: {
            child_id: childId,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function (response) {
            console.log("Registration response:", response);
            if (response.status === 'success') {
                alert(response.message || "Registration successful!");
                location.reload();
            } else {
                alert(response.message || "Registration failed. Please try again.");
            }
        },
        error: function (xhr, status, error) {
            console.error("Registration error:", error);
            console.error("Response:", xhr.responseText);
            alert("An error occurred during registration. Please try again later.");
        }
    });
}
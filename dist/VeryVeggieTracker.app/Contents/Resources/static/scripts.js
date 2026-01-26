document.addEventListener('DOMContentLoaded', function() {
    // Select all checkboxes with the class 'goal-check'
    const checkboxes = document.querySelectorAll('.goal-checkbox');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const goalId = this.dataset.goalid;
            const isCompleted = this.checked ? 1 : 0; // Convert boolean to 1/0 for SQLite

            // Using the fetch API to send data to Flask
            fetch('/update_goal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    goal_id: goalId,
                    completed: isCompleted
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                // Optional: You could trigger a W3.CSS toast/notification here
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert checkbox if the update failed
                this.checked = !this.checked;
                alert("Failed to update goal. Please try again.");
            });
        });
    });
});

document.querySelectorAll('.aspiration-checkbox').forEach(box => {
    box.addEventListener('change', function() {
        const genId = this.dataset.genId;
        const status = this.checked ? 1 : 0;

        fetch('/update_aspiration', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ gen_id: genId, completed: status })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Aspiration updated:", data);
        });
    });
});
   
        // JavaScript for interactivity could be added here
        document.addEventListener('DOMContentLoaded', function() {
            // Example: Toggle checkbox state
            const checkboxes = document.querySelectorAll('.checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('click', function() {
                    this.classList.toggle('checked');
                });
            });
        });
 
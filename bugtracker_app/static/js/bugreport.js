   
        // File upload interaction
        document.querySelector('.file-upload').addEventListener('click', () => {
            alert('File upload dialog would open here');
        });

        document.querySelector("form").addEventListener("submit", function() {
    // copy editor content into hidden input
    document.getElementById("bug-description").value = document.getElementById("content").innerHTML;
     });

     //submit actions(fetch api)
      document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submitBugReport');
    const form = document.getElementById('bug_report');
      })

      // data saved to database
      document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('bug_report');
    const contentDiv = document.getElementById('content');
    const hiddenDescription = document.getElementById('bug_description');
    
    // Update hidden field with editor content before form submission
    form.addEventListener('submit', function(e) {
        hiddenDescription.value = contentDiv.innerHTML;
        
        // For AJAX submission (optional)
        if (window.location.search.includes('ajax=true')) {
            e.preventDefault();
            submitFormViaAjax();
        }
    });
    
    // File upload interaction
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (fileUpload && fileInput) {
        fileUpload.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileUpload.querySelector('p span').textContent = this.files[0].name;
            }
        });
    }
    
    // Optional: AJAX form submission function
    function submitFormViaAjax() {
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.alert('Bug reported successfully!');
                form.reset();
                contentDiv.innerHTML = 'Lorem, ipsum.'; // Reset editor
            } else {
                window.alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting the form.');
        });
    }
    
    // Helper function to get CSRF token
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
});

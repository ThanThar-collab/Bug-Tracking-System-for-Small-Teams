// // File upload interaction
// document.querySelector(".file-upload").addEventListener("click", () => {
//     alert("File upload dialog would open here");
// });

// document.querySelector("form").addEventListener("submit", function () {
//     // copy editor content into hidden input
//     document.getElementById("bug_description").value =
//         document.getElementById("content").innerHTML;
// });

// //submit actions(fetch api)
// document.addEventListener("DOMContentLoaded", function () {
//     const submitButton = document.getElementById("submitBugReport");
//     const form = document.getElementById("bug_report");
// });

// // data saved to database
// document.addEventListener("DOMContentLoaded", function () {
//     const form = document.getElementById("bug_report");
//     const contentDiv = document.getElementById("content");
//     const hiddenDescription = document.getElementById("bug_description");

//     // Update hidden field with editor content before form submission
//     form.addEventListener("submit", function (e) {
//         hiddenDescription.value = contentDiv.innerHTML;

//         // For AJAX submission (optional)
//         if (window.location.search.includes("ajax=true")) {
//             e.preventDefault();
//             submitFormViaAjax();
//         }
//     });

//     // File upload interaction
//     const fileUpload = document.querySelector(".file-upload");
//     const fileInput = document.querySelector('input[type="file"]');

//     if (fileUpload && fileInput) {
//         fileUpload.addEventListener("click", function () {
//             fileInput.click();
//         });

//         fileInput.addEventListener("change", function () {
//             if (this.files.length > 0) {
//                 fileUpload.querySelector("p span").textContent = this.files[0].name;
//             }
//         });
//     }

//     // Optional: AJAX form submission function
//     function submitFormViaAjax() {
//         const formData = new FormData(form);

//         fetch(form.action, {
//             method: "POST",
//             body: formData,
//             headers: {
//                 "X-Requested-With": "XMLHttpRequest",
//                 "X-CSRFToken": getCookie("csrftoken"),
//             },
//         })
//             .then((response) => response.json())
//             .then((data) => {
//                 if (data.success) {
//                     window.alert("Bug reported successfully!");
//                     form.reset();
//                     contentDiv.innerHTML = "Lorem, ipsum."; // Reset editor
//                 } else {
//                     window.alert("Error: " + data.error);
//                 }
//             })
//             .catch((error) => {
//                 console.error("Error:", error);
//                 alert("An error occurred while submitting the form.");
//             });
//     }

//     // Helper function to get CSRF token
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== "") {
//             const cookies = document.cookie.split(";");
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === name + "=") {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
// });
document.addEventListener('DOMContentLoaded', function () {
    // --- Element Variables ---
    const form = document.getElementById('bug_report');
    const contentDiv = document.getElementById('content'); // Your rich text editor content div
    const hiddenDescription = document.getElementById('bug_description'); // The hidden input field
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = document.querySelector('input[type="file"]');


    // --- 1. Form Submission Handler ---
    // This is the core logic for form submission.
    if (form) {
        form.addEventListener('submit', function (e) {
            // STEP A: ALWAYS update the hidden field with the final content from the editor
            hiddenDescription.value = contentDiv.innerHTML;

            // STEP B: Handle AJAX submission if required
            if (window.location.search.includes('ajax=true')) {
                e.preventDefault(); // Stop the default browser submission
                submitFormViaAjax();
            }

            // If ajax=false or not present, the form submits normally after Step A.
        });
    }


    // --- 2. File Upload Interaction ---
    if (fileUpload && fileInput) {
        // Clicking the custom upload area clicks the hidden file input
        fileUpload.addEventListener('click', function () {
            fileInput.click();
        });

        // Update the display text when a file is selected
        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                // Assuming your fileUpload element has a structure like <div><p><span>Placeholder</span></p></div>
                const span = fileUpload.querySelector('p span');
                if (span) {
                    span.textContent = this.files[0].name;
                }
            }
        });
    }


    // --- 3. Optional: AJAX Form Submission Function ---
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
            .then(response => {
                if (!response.ok) {
                    // Throw an error for bad responses (400s, 500s)
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    window.alert('Bug reported successfully!');
                    form.reset();
                    contentDiv.innerHTML = ''; // Clear the editor content
                } else {
                    window.alert('Error: ' + (data.error || 'Unknown error.'));
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                alert('An error occurred while submitting the form. See console for details.');
            });
    }


    // --- 4. Helper function to get CSRF token ---
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
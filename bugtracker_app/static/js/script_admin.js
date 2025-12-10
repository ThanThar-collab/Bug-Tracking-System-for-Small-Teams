// Simple navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            menuItems.forEach(i => i.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Get the page name from data attribute
            const page = this.getAttribute('data-page');
            
            // Update page title
            document.querySelector('.page-title').textContent = 
                page.charAt(0).toUpperCase() + page.slice(1);
            
            // In a real application, you would load the appropriate content here
            // For this example, we're just changing the title
        });
    });
});
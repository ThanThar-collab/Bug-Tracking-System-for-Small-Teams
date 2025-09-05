document.addEventListener('DOMContentLoaded', function() {
            // Card elements and containers
            const cards = document.querySelectorAll('.card');
            const containers = document.querySelectorAll('.cards-container');
            
            // Initialize drag and drop
            initDragAndDrop();
            
            // Update card counts initially
            updateCardCounts();
            
            function initDragAndDrop() {
                cards.forEach(card => {
                    card.addEventListener('dragstart', () => {
                        card.classList.add('dragging');
                    });
                    
                    card.addEventListener('dragend', () => {
                        card.classList.remove('dragging');
                        updateCardCounts();
                    });
                });
                
                containers.forEach(container => {
                    container.addEventListener('dragover', e => {
                        e.preventDefault();
                        const afterElement = getDragAfterElement(container, e.clientY);
                        const draggable = document.querySelector('.dragging');
                        
                        if (afterElement == null) {
                            container.appendChild(draggable);
                        } else {
                            container.insertBefore(draggable, afterElement);
                        }
                        
                        container.classList.add('drag-over');
                    });
                    
                    container.addEventListener('dragenter', () => {
                        container.classList.add('drag-over');
                    });
                    
                    container.addEventListener('dragleave', () => {
                        container.classList.remove('drag-over');
                    });
                    
                    container.addEventListener('drop', () => {
                        container.classList.remove('drag-over');
                    });
                });
            }
            
            function getDragAfterElement(container, y) {
                const draggableElements = [...container.querySelectorAll('.card:not(.dragging)')];
                
                return draggableElements.reduce((closest, child) => {
                    const box = child.getBoundingClientRect();
                    const offset = y - box.top - box.height / 2;
                    
                    if (offset < 0 && offset > closest.offset) {
                        return { offset: offset, element: child };
                    } else {
                        return closest;
                    }
                }, { offset: Number.NEGATIVE_INFINITY }).element;
            }
            
            function updateCardCounts() {
                const openCount = document.getElementById('open-container').children.length;
                const progressCount = document.getElementById('progress-container').children.length;
                const testingCount = document.getElementById('testing-container').children.length;
                const fixedCount = document.getElementById('fixed-container').children.length;
                
                document.getElementById('open-count').textContent = openCount;
                document.getElementById('progress-count').textContent = progressCount;
                document.getElementById('testing-count').textContent = testingCount;
                document.getElementById('fixed-count').textContent = fixedCount;

            }
            
            // Simulate adding a new bug (this would typically come from a database)
            // function simulateNewBug() {
            //     const openContainer = document.getElementById('open-container');
                
            //     // Create a new bug card
            //     const newBug = document.createElement('div');
            //     newBug.className = 'card';
            //     newBug.draggable = true;
            //     newBug.dataset.id = '8';
                
            //     const priorities = ['high', 'medium', 'low'];
            //     const randomPriority = priorities[Math.floor(Math.random() * priorities.length)];
                
            //     newBug.innerHTML = `
            //         <div class="card-header">
            //             <span class="bug-id">BUG-${Math.floor(100 + Math.random() * 900)}</span>
            //             <span class="priority ${randomPriority}">
            //                 <i class="fas fa-arrow-${randomPriority === 'high' ? 'up' : randomPriority === 'medium' ? 'right' : 'down'}"></i> 
            //                 ${randomPriority.charAt(0).toUpperCase() + randomPriority.slice(1)}
            //             </span>
            //         </div>
            //         <div class="card-content">
            //             <div class="bug-title">New bug report from client</div>
            //             <div class="bug-description">This is a new bug that was just reported and added to the system.</div>
            //         </div>
            //         <div class="card-footer">
            //             <div class="assignee">
            //                 <div class="avatar">ND</div>
            //                 <span>New Developer</span>
            //             </div>
            //             <div class="tags">
            //                 <span class="tag backend">Backend</span>
            //             </div>
            //         </div>
            //     `;
                
            //     // Add drag events to the new bug
            //     newBug.addEventListener('dragstart', () => {
            //         newBug.classList.add('dragging');
            //     });
                
            //     newBug.addEventListener('dragend', () => {
            //         newBug.classList.remove('dragging');
            //         updateCardCounts();
            //     });
                
            //     // Add to open container
            //     openContainer.appendChild(newBug);
                
            //     // Update counts
            //     updateCardCounts();
            // }
            
            // Simulate a new bug being added every 30 seconds for demo purposes
        //     setInterval(simulateNewBug, 30000);
        // });
});
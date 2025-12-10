document.addEventListener("DOMContentLoaded", () => {
    const containers = document.querySelectorAll('.cards-container');

    function initDragAndDropForCard(card) {
        card.addEventListener('dragstart', () => card.classList.add('dragging'));
        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
            updateCardCounts();
        });
    }

    function initDragAndDropForContainers() {
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

            container.addEventListener('dragenter', () => container.classList.add('drag-over'));
            container.addEventListener('dragleave', () => container.classList.remove('drag-over'));
            container.addEventListener('drop', () => container.classList.remove('drag-over'));
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
        document.getElementById('open-count').textContent = document.getElementById('open-container').children.length;
        document.getElementById('progress-count').textContent = document.getElementById('progress-container').children.length;
        document.getElementById('testing-count').textContent = document.getElementById('testing-container').children.length;
        document.getElementById('fixed-count').textContent = document.getElementById('fixed-container').children.length;
    }

    // Fetch bugs and create cards dynamically
    fetch("/api/fetch-bugs/")
        .then(response => response.json())
        .then(bugs => {
            bugs.forEach(bug => {
                let containerId = "";
                if (bug.status === "Open") containerId = "open-container";
                else if (bug.status === "In Progress") containerId = "progress-container";
                else if (bug.status === "Resolved" || bug.status === "Closed") containerId = "fixed-container";

                if (containerId) {
                    const container = document.getElementById(containerId);
                    const card = document.createElement("div");
                    card.classList.add("card");
                    card.setAttribute("draggable", "true");
                    card.innerHTML = `
                        <div class="card-header">
                            <span class="bug-id">BUG-${bug.id}</span>
                            <span class="priority ${bug.severity.toLowerCase()}">${bug.severity}</span>
                        </div>
                        <div class="card-content">
                            <div class="bug-title">${bug.title}</div>
                            <div class="bug-description">${bug.description}</div>
                        </div>
                        <div class="card-footer">
                            <div class="assignee">
                                <div class="avatar">${bug.reported_by__username[0].toUpperCase()}</div>
                                <span>${bug.reported_by__username}</span>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);

                    // Attach drag-and-drop events to this new card
                    initDragAndDropForCard(card);
                }
            });

            // Initialize drag-over events for containers
            initDragAndDropForContainers();
            updateCardCounts();
        });
});

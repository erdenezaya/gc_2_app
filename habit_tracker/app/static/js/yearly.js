// Function to create GitHub-style contribution grid cells
function generateGridCells(containerId, year) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    // Create 12 months (columns)
    for (let month = 0; month < 12; month++) {
        const column = document.createElement('div');
        column.className = 'grid-column';
        
        // Determine days in each month for the given year
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Create cells for each day
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dayOfWeek = date.getDay(); // 0 is Sunday, 1 is Monday, etc.
            
            // Only show cells for Monday (1), Wednesday (3), and Friday (5)
            const relevantDays = {
                'monday-grid': 1,
                'wednesday-grid': 3,
                'friday-grid': 5,
                'monday-grid-water': 1,
                'wednesday-grid-water': 3,
                'friday-grid-water': 5,
                'monday-grid-takeout': 1,
                'wednesday-grid-takeout': 3,
                'friday-grid-takeout': 5,
                'monday-grid-meditate': 1,
                'wednesday-grid-meditate': 3,
                'friday-grid-meditate': 5
            };
            
            if (dayOfWeek === relevantDays[containerId]) {
                const cell = document.createElement('div');
                cell.className = 'grid-cell';
                
                // Random intensity for demo purposes
                const intensity = Math.floor(Math.random() * 5); // 0-4
                if (intensity > 0) {
                    cell.classList.add(`cell-level-${intensity}`);
                }
                
                column.appendChild(cell);
            }
        }
        
        container.appendChild(column);
    }
}

// Initialize all grids with the current year
function initializeGrids(year) {
    generateGridCells('monday-grid', year);
    generateGridCells('wednesday-grid', year);
    generateGridCells('friday-grid', year);
    generateGridCells('monday-grid-water', year);
    generateGridCells('wednesday-grid-water', year);
    generateGridCells('friday-grid-water', year);
    generateGridCells('monday-grid-takeout', year);
    generateGridCells('wednesday-grid-takeout', year);
    generateGridCells('friday-grid-takeout', year);
    generateGridCells('monday-grid-meditate', year);
    generateGridCells('wednesday-grid-meditate', year);
    generateGridCells('friday-grid-meditate', year);
}

// Year toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.year-button').forEach(button => {
        button.addEventListener('click', function() {
            const year = parseInt(this.getAttribute('data-year'));
            
            // Update active button
            document.querySelectorAll('.year-button').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Regenerate grids with selected year
            initializeGrids(year);
        });
    });
    
    // Initialize with 2025 (default active year)
    initializeGrids(2025);
    
    // Navigation buttons functionality (simplified for demo)
    document.querySelectorAll('.nav-button').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.textContent.includes('Logout')) {
                document.querySelectorAll('.nav-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
    
    // Share button functionality (simplified for demo)
    document.querySelector('.share-btn').addEventListener('click', function() {
        alert('Sharing functionality would go here!');
    });
});
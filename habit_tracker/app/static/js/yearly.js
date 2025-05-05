// Function to create GitHub-style annual contribution grid
function generateAnnualGrid(containerId, year, habitData, habitColor) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container not found: ${containerId}`);
        return;
    }

    container.innerHTML = '';

    // Calculate first day of the year and total days
    const firstDay = new Date(year, 0, 1);
    const firstDayOfWeek = firstDay.getDay(); // 0 (Sunday) to 6 (Saturday)
    const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    const totalDays = isLeapYear ? 366 : 365;

    // Create a container for the grid with labels
    const gridContainer = document.createElement('div');
    gridContainer.className = 'grid-container';

    // Add day labels (e.g., Sun, Mon, Tue, ...)
    const dayLabels = document.createElement('div');
    dayLabels.className = 'day-labels';
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    daysOfWeek.forEach(day => {
        const dayLabel = document.createElement('div');
        dayLabel.className = 'day-label';
        dayLabel.textContent = day;
        dayLabels.appendChild(dayLabel);
    });
    gridContainer.appendChild(dayLabels);

    // Add month labels (e.g., Jan, Feb, ...)
    const monthLabels = document.createElement('div');
    monthLabels.className = 'month-labels';
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    months.forEach((month, index) => {
        const monthLabel = document.createElement('div');
        monthLabel.className = 'month-label';
        monthLabel.textContent = month;

        // Position the month label based on the first day of the month
        const firstDayOfMonth = new Date(year, index, 1);
        const offset = Math.floor((firstDayOfMonth.getTime() - firstDay.getTime()) / (1000 * 60 * 60 * 24));
        monthLabel.style.gridColumnStart = Math.floor((offset + firstDayOfWeek) / 7) + 1;
        monthLabels.appendChild(monthLabel);
    });
    gridContainer.appendChild(monthLabels);

    // Create cells grid (7 rows × ~53 columns)
    const cellsGrid = document.createElement('div');
    cellsGrid.className = 'cells-grid';

    // Total weeks needed (first partial week to last partial week)
    const totalWeeks = Math.ceil((totalDays + firstDayOfWeek) / 7);

    // Create cells for the entire year
    for (let day = 0; day < 7; day++) { // 7 days in a week (rows)
        for (let week = 0; week < totalWeeks; week++) { // ~52-53 weeks (columns)
            const dayNumber = week * 7 + day - firstDayOfWeek + 1;
            const cell = document.createElement('div');
            cell.className = 'grid-cell';

            if (dayNumber > 0 && dayNumber <= totalDays) {
                // This is a valid day in the year
                const date = new Date(year, 0, dayNumber);
                const formattedDate = `${year}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;

                // Store the date as a data attribute for potential interactions
                cell.setAttribute('data-date', formattedDate);

                // Check if we have data for this date
                if (habitData && habitData[formattedDate] && habitData[formattedDate].intensity > 0) {
                    // Use the assigned habit color
                    cell.style.backgroundColor = habitColor;
                    cell.classList.add('completed');

                    // Add tooltip with date and notes if available
                    const tooltipText = habitData[formattedDate].notes
                        ? `${formattedDate}: ${habitData[formattedDate].notes}`
                        : formattedDate;

                    cell.setAttribute('title', tooltipText);
                } else {
                    // Add tooltip with just the date
                    cell.setAttribute('title', formattedDate);
                }
            } else {
                // This cell is outside the year range
                cell.classList.add('empty');
            }

            cellsGrid.appendChild(cell);
        }
    }

    // Add all components to the container
    gridContainer.appendChild(cellsGrid);
    container.appendChild(gridContainer);

    // Update the legend color for "Completed"
    const legendCompleted = container.parentElement.querySelector('.legend-cell.completed');
    if (legendCompleted) {
        legendCompleted.style.backgroundColor = habitColor;
    }
}

// Function to fetch habit data from backend
async function fetchHabitData(habitId, year) {
    try {
        console.log(`Fetching data for habit ${habitId}, year ${year}...`);
        
        // Make API request to get habit data for the specified year
        const response = await fetch(`/api/habits/${habitId}/data?year=${year}`);
        
        if (!response.ok) {
            console.error(`Error response: ${response.status} ${response.statusText}`);
            const errorText = await response.text();
            console.error(`Error details: ${errorText}`);
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(`Data received for habit ${habitId}`);
        return data;
    } catch (error) {
        console.error(`Error fetching data for habit ${habitId}:`, error);
        return {}; // Return empty object on error
    }
}

// Function to fetch all habits from the backend
async function fetchHabits() {
    try {
        const response = await fetch('/api/habits');
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching habits:', error);
        return []; // Return empty array on error
    }
}

// Initialize grids for all habits
async function initializeGrids(year) {
    try {
    // Define the colors array
    const colors = window.habitChartColors; 

        // Get all habit containers
        const habitContainers = document.querySelectorAll('.habit-container');

        // Process each habit container
        habitContainers.forEach((container, index) => {
            // Get habit title and ID
            const titleElement = container.querySelector('.habit-title');
            const gridElement = container.querySelector('.github-style-grid');

            if (!titleElement || !gridElement) return;

            const habitName = titleElement.textContent.trim();
            const habitId = gridElement.id.replace('grid-', '');

            console.log(`Processing habit: ${habitName}, ID: ${habitId}`);

            // Assign a unique color for this habit
            const habitColor = colors[index % colors.length];

            // Show loading state
            gridElement.innerHTML = '<div style="text-align: center; padding: 20px;">Loading data...</div>';

            // Fetch data for this habit
            fetchHabitData(habitId, year).then(habitData => {
                // Generate the grid with the data and the assigned color
                generateAnnualGrid(gridElement.id, year, habitData, habitColor);
            });
        });
    } catch (error) {
        console.error('Error initializing grids:', error);
        document.querySelectorAll('.github-style-grid').forEach(grid => {
            grid.innerHTML = '<div style="color: red; text-align: center; padding: 20px;">Error loading data</div>';
        });
    }
}

// Year toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle year button clicks
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
    
    // Initialize with default active year
    const activeYearButton = document.querySelector('.year-button.active');
    const defaultYear = activeYearButton ? parseInt(activeYearButton.getAttribute('data-year')) : 2025;
    
    // Initialize grids with the default year
    initializeGrids(defaultYear);
    
    // Share button functionality
    function submitShareForm() {
        const username = document.getElementById('modal-username').value;
        console.log("User to receive stats:", username);
        if (username) { // Check if username is not empty
            document.getElementById('receiver-username').value = username;
            document.getElementById('share-form').submit(); // Submit the form
        } else {
            alert("Please enter a username.");
        }
    };
});
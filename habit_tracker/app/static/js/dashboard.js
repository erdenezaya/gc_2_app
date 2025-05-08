/*  This is a JavaScript file for rendering a doughnut chart using Chart.js
  It uses the Chart.js library to create a doughnut chart that displays the percentage  
  of completed habits and the remaining habits for today.
  The chart is rendered in a canvas element with the ID 'daily_completion'.
*/
// Get canvas context
const ctx = document.getElementById("daily_completion").getContext("2d");

// Use colors from the backend
const stops = window.chartGradient || ["#FF1111", "#FFA500", "#FFFF00", "#00FF00"]; // Fallback colors if not provided
const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);

stops.forEach((color, i) => {
  gradient.addColorStop(i / (stops.length - 1), color);
});

const todayDone = window.todayDone;
const totalHabits = window.totalHabits;
const remaining = Math.max(totalHabits - todayDone, 0);
const percentage = totalHabits === 0 ? 0 : Math.round((todayDone / totalHabits) * 100);

const doughnutChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Completed', 'Remaining'],
    datasets: [{
      data: totalHabits === 0 ? [0, 1] : [todayDone, remaining],
      backgroundColor: [
        gradient, // Gradient for "Completed"
        '#e0e0e0' // Default color for "Remaining"
      ],
      borderColor: [
        "black", 
        "black"  
      ],
      borderWidth: 2 // Set border width to 2px
    }]
  },
  options: {
    cutout: '65%',
        plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
      doughnutLabel: {
        labels: [
          {
            text: percentage + '%',
            font: {
              size: '24',
              weight: 'bold'
            },
            color: '#333'
          }
        ]
      }
    },
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 1000,
    }
  },
  plugins: [{
    id: 'doughnutLabel',
    beforeDraw(chart, args, options) {
      const {ctx, chartArea: {width, height}} = chart;
      ctx.save();
      const fontSize = options.labels[0].font.size || '20';
      ctx.font = `${fontSize}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = options.labels[0].color || '#000';
      ctx.fillText(options.labels[0].text, width / 2, height / 2);
    }
  }]
});

// function to send a share request
function submitShareForm() {
  const username = document.getElementById('modal-username').value;
  console.log("User to receive stats:", username);
  if (username) { // Check if username is not empty
      document.getElementById('receiver-username').value = username;
      document.getElementById('share-form').submit(); // Submit the form
  } else {
      alert("Please enter a username.");
  }
}

const today = new Date().toLocaleDateString('en-CA'); // Get today's date in YYYY-MM-DD format considering timezone

// Set the placeholder value of the date input to today's date
document.addEventListener("DOMContentLoaded", function () {
    const datePicker = document.getElementById('date-picker');
    datePicker.value = today; // Set the value of the date input to today's date
})

// Function to handle date selection
function handleDateSelection() {
    const selectedDate = document.getElementById('date-picker').value;

    if (selectedDate) {
        if (selectedDate > today) {
            alert('You cannot track habit in the future. Please choose a valid date.');
        } else {
            // Fetch habits for the selected date
            fetch(`/habits_by_date?date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const habitList = document.getElementById("habit-list");
                        habitList.innerHTML = ""; // Clear the current list

                        data.habits.forEach(habit => {
                            const habitItem = document.createElement("div");
                            habitItem.className = "habit-item";

                            // Create a wrapper div for the checkbox and label
                            const checkboxLabelWrapper = document.createElement("div");
                            checkboxLabelWrapper.className = "checkbox-label-wrapper";
  
                            // Create the checkbox
                            const checkbox = document.createElement("input");
                            checkbox.type = "checkbox";
                            checkbox.id = `habit${habit.id}`;
                            checkbox.checked = habit.completed; // Set checkbox based on completion status
                            checkbox.dataset.habitId = habit.id; // Store habit ID for later use

                            // Create the label
                            const label = document.createElement("label");
                            label.htmlFor = `habit${habit.id}`;
                            label.textContent = habit.name;

                            // Append the checkbox and label to the wrapper
                            checkboxLabelWrapper.appendChild(checkbox);
                            checkboxLabelWrapper.appendChild(label);
                            // Append the wrapper to the habit item

                            habitItem.appendChild(checkboxLabelWrapper);
                            // Create the delete button
                            const deleteButton = document.createElement("button");
                            deleteButton.className = "delete-btn btn btn-danger";
                            deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
                            deleteButton.onclick = () => deleteHabit(habit.id);

                            habitItem.appendChild(deleteButton);

                            habitList.appendChild(habitItem);
                        });

                        // Add a "Save" button
                        const saveButton = document.createElement("button");
                        saveButton.textContent = "Save";
                        saveButton.className = "save-btn";
                        saveButton.onclick = () => saveHabitStatuses(selectedDate);
                        habitList.appendChild(saveButton);

                        // Hide the "Add Habit" form
                        const addHabitForm = document.querySelector(".add-habit-form");
                        if (addHabitForm) {
                            addHabitForm.style.display = "none"; // Hide the form
                        }
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error("Error fetching habits:", error);
                });
        }
    } else {
        alert('Please select a date.');
    }
}

// Function to save habit statuses
function saveHabitStatuses(selectedDate) {
    const checkboxes = document.querySelectorAll("#habit-list input[type='checkbox']");
    const habitStatuses = Array.from(checkboxes).map(checkbox => ({
        habit_id: checkbox.dataset.habitId,
        completed: checkbox.checked
    }));

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(`/save_habit_statuses`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({ date: selectedDate, habits: habitStatuses })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert(`Habit statuses updated successfully for ${selectedDate}!`);
        window.location.href = "/dashboard"; // Redirect to /dashboard
      } else {
        alert(data.error);
      }
    })
    .catch(error => {
      console.error("Error saving habit statuses:", error);
    });
}
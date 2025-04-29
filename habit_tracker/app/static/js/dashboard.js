/*  This is a JavaScript file for rendering a doughnut chart using Chart.js
  It uses the Chart.js library to create a doughnut chart that displays the percentage  
  of completed habits and the remaining habits for today.
  The chart is rendered in a canvas element with the ID 'daily_completion'.
*/
const ctx = document.getElementById('daily_completion').getContext('2d');

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
      backgroundColor: ['#4CAF50', '#e0e0e0'],
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
})

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

// Set the placeholder value of the date input to today's date
document.addEventListener("DOMContentLoaded", function () {
    const datePicker = document.getElementById('date-picker');
    const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
    datePicker.value = today; // Set the value of the date input to today's date
})

// Function to handle date selection
    function handleDateSelection() {
        const selectedDate = document.getElementById('date-picker').value;
        if (selectedDate) {
            alert(`You selected: ${selectedDate}`);
            // Need to add logic here to handle the selected date
        } else {
            alert('Please select a date.');
        }
    }
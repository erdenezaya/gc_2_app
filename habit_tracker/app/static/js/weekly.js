// This script is used to create a doughnut chart for each habit in weekly.html page

// center text plugin
const centerTextPlugin = {
    id: 'centerText',
    beforeDraw: (chart) => {
        const { width, height, ctx } = chart;
        const data = chart.data.datasets[0].data;
        const total = data.reduce((a, b) => a + b, 0);
        const completed = data[0];
        const percentage = Math.round((completed / total) * 100);

        ctx.save();
        ctx.font = 'bold 24px sans-serif'; // text font
        ctx.fillStyle = '#333';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${percentage}%`, width / 2, height / 2);
        ctx.restore();
    }
};

document.addEventListener("DOMContentLoaded", function () {

    const chartsData = window.habitChartData || [];
    const colors = window.habitChartColors; 


  chartsData.forEach((habit, index) => {
      new Chart(document.getElementById(`chart-${habit.id}`), {
          type: "doughnut",
          data: {
              labels: ["Completed", "Missed"],
              datasets: [{
                  data: [habit.completed_days, habit.total_days - habit.completed_days],
                  backgroundColor: [
                      colors[index % colors.length], // Assign color for "Completed"
                      "#e0e0e0" // Default color for "Missed"
                  ],
                  borderColor: [
                      "black", // Border color for "Completed"
                      "black"  // Border color for "Missed"
                  ],
                  borderWidth: 2 // Set border width to 2px
              }]
          },
          options: {
              responsive: true,
              cutout: "60%", // cutout percentage defines the size of the hole in the doughnut
              plugins: {
                  legend: { display: false },
                  tooltip: { enabled: true }
              }
          },
          plugins: [centerTextPlugin]
      });
  });
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
};
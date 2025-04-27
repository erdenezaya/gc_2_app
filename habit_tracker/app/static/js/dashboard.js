/*  This is a JavaScript file for rendering a doughnut chart using Chart.js
  It uses the Chart.js library to create a doughnut chart that displays the percentage  
  of completed habits and the remaining habits for today.
  The chart is rendered in a canvas element with the ID 'todayDoughnut'.
*/

const ctx = document.getElementById('todayDoughnut').getContext('2d');

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
      borderWidth: 1
    }]
  },
  options: {
    cutout: '70%',
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
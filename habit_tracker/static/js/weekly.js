// Weekly Page Chart

function createChart(ctxId, label, dataValue, color) {
    const ctx = document.getElementById(ctxId).getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [label, 'Remaining'],
            datasets: [{
                data: [dataValue, 100 - dataValue],
                backgroundColor: [color, '#e0e0e0'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { display: false }
            },
            cutout: '70%'
        }
    });
}

// Create individual charts
createChart('chartWakeUp', 'Wake Up Early', 85, '#FF6384');
createChart('chartWater', 'Drink Water', 100, '#36A2EB');
createChart('chartMeditate', 'Meditate', 85, '#FFCE56');
createChart('chartTakeout', 'No Takeout', 100, '#4BC0C0');

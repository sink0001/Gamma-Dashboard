

export function graph_ratio(ratio, chart) {
    // dummy x and y values for now
    new Chart(chart, {
            type: 'line', // Type of chart
            data: {
                labels: ['Date 1', 'Date 2', 'Date 3', 'Date 4'],
                datasets: [{
                    label: ratio,
                    data: [42.65, 41.42, 30.65, 29.85],
                    borderColor: 'rgba(90, 214, 255, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    pointStyle: 'circle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: ratio
                    },
                    tooltip: {
                        displayColors: false
                    }
                }
            }
        });
}




async function get_graph_values(ratio, period) {
    const response = await fetch(`/stock_data/graph/${period}_ratio/${ratio}`)
    const json_response = await response.json()
    if (!response.ok) {
        const error = json_response["error"]
        console.log(error)
        console.log(json_response)
    }
    else {
        const x_values = json_response["data"]["x_values"]
        const y_values = json_response["data"]["y_values"]
        return [x_values, y_values]
    }
}


export async function graph_ratio(ratio, ratio_display_name, period, chart) {
    const positional_values = await get_graph_values(ratio, period)
    const x_values = positional_values[0]
    const y_values = positional_values[1]
    const mobile = window.matchMedia('(max-width: 500px)').matches

    const graph = new Chart(chart, {
            type: 'line', // Type of chart
            data: {
                labels: x_values,
                datasets: [{
                    label: ratio_display_name,
                    data: y_values,
                    borderColor: 'rgba(90, 214, 255, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    pointStyle: 'circle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                }]
            },
            options: {
                responsive: !mobile,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: ratio_display_name
                    },
                    tooltip: {
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        grid: {display:false}
                    },
                    y: {
                        grid: {display:false}
                    }
                }
            }
        });
    return graph
}
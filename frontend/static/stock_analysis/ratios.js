import { graph_ratio } from "../graphing/graphing.js"


const ratio_selection_buttons = document.querySelectorAll(".ratio-button")
console.log(ratio_selection_buttons)

function button_event_listener(event) {
    for (const button of ratio_selection_buttons) {
        button.style.color = null
    }
    const button = event.target
    button.style.color = "rgb(68, 192, 233)"

    const chart = document.querySelector("#chart")
    chart.style.display = "block"
    graph_ratio("something", chart)
}

for (let i = 0; i < ratio_selection_buttons.length; i++) {
    ratio_selection_buttons[i].addEventListener('click', button_event_listener)
}
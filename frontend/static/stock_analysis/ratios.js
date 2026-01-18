import { graph_ratio } from "../graphing/graphing.js"


window.addEventListener("load", () => {
    console.log("triggered")
    const button = document.querySelector("#pe")
    button.click()
})

const ratio_selection_buttons = document.querySelectorAll(".ratio-button")
let current_ratio_button = document.querySelector("#pe")
let period = "annual"
const annual_toggle = document.querySelector("#annual")
const quarterly_toggle = document.querySelector("#quarterly")


function ratio_button_event_listener(event) {
    for (const button of ratio_selection_buttons) {
        button.style.color = null
    }
    const button = event.target
    button.style.color = "rgb(68, 192, 233)"

    current_ratio_button = button.id
    annual_toggle.click()
}

for (let i = 0; i < ratio_selection_buttons.length; i++) {
    ratio_selection_buttons[i].addEventListener("click", ratio_button_event_listener)
}


function period_toggle_event_listener(event) {
    const button = event.target
    period = button.id
    annual_toggle.style.color = null
    quarterly_toggle.style.color = null
    button.style.color = "rgb(68, 192, 233)"

    const chart = document.querySelector("#chart")
    chart.style.display = "block"
    const ratio = current_ratio_button.id
    graph_ratio(ratio, period, chart)
}
annual_toggle.addEventListener("click", period_toggle_event_listener)
quarterly_toggle.addEventListener("click", period_toggle_event_listener)
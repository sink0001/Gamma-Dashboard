import { graph_ratio } from "../graphing/graphing.js"


window.addEventListener("load", () => {
    console.log("triggered")
    const button = document.querySelector("#pe")
    if (button) {
        button.click()
    }
    else {
        console.log("pe button not found")
    }
    
})

const ratio_selection_buttons = document.querySelectorAll(".ratio-button")
const period = "annual"



function ratio_button_event_listener(event) {
    for (const button of ratio_selection_buttons) {
        button.style.color = null
    }
    const button = event.target
    button.style.color = "rgb(68, 192, 233)"

    const chart = document.querySelector("#chart")
    chart.style.display = "block"
    graph_ratio("something", "annual", chart)
}

for (let i = 0; i < ratio_selection_buttons.length; i++) {
    ratio_selection_buttons[i].addEventListener('click', ratio_button_event_listener)
}
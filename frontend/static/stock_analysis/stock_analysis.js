import { graph_ratio } from "../graphing/graphing.js"


window.addEventListener("load", () => {
    const button = document.querySelector("#pe")
    button.click()
})

const ratio_selection_buttons = document.querySelectorAll(".ratio-button")
let current_ratio_button = document.querySelector("#pe")
let period = "annual"
const annual_toggle = document.querySelector("#annual")
const quarterly_toggle = document.querySelector("#quarterly")
var graph = null


function ratio_button_event_listener(event) {
    for (const button of ratio_selection_buttons) {
        button.style.color = null
    }
    const button = event.target
    button.style.color = "rgb(68, 192, 233)"

    current_ratio_button = button
    annual_toggle.click()
}

for (let i = 0; i < ratio_selection_buttons.length; i++) {
    ratio_selection_buttons[i].addEventListener("click", ratio_button_event_listener)
}


async function period_toggle_event_listener(event) {
    const button = event.target
    period = button.id
    annual_toggle.style.color = null
    quarterly_toggle.style.color = null
    button.style.color = "rgb(68, 192, 233)"

    const chart = document.querySelector("#chart")
    chart.style.display = "block"
    const ratio = current_ratio_button.id
    const ratio_display_name = current_ratio_button.innerText

    if (graph) {
        graph.destroy()
    }
    graph = await graph_ratio(ratio, ratio_display_name, period, chart)
}
annual_toggle.addEventListener("click", period_toggle_event_listener)
quarterly_toggle.addEventListener("click", period_toggle_event_listener)


const ad_to_watchlist_toggle = document.querySelector("#favourite-checkbox")
ad_to_watchlist_toggle.addEventListener("click", async (event) => {
    event.preventDefault()
    const toggle = event.target
    if (toggle.checked) {
        const response = await fetch("/user_info/add_ticker_to_watchlist")
        const results = await response.json()
        console.log(results)
        if (results["success"]) {
            toggle.checked = true
            alert("added the ticker to watchlist")
        }
        else if (results["error_type"] === "ValueError") {
            alert("This stock is already in your watchlist")
        }
        else {
            alert("an error occured while inserting the stock into your watchlist")
        }
    }
})

const ratio_selection_buttons = document.querySelectorAll(".ratio-button")
console.log(ratio_selection_buttons)

function change_button_text_color(event) {
    for (const button of ratio_selection_buttons) {
        button.style.color = null
    }
    const button = event.target
    button.style.color = "rgb(68, 192, 233)"
}

for (let i = 0; i < ratio_selection_buttons.length; i++) {
    ratio_selection_buttons[i].addEventListener('click', change_button_text_color)
}
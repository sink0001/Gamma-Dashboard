const signup_form = document.querySelector("#signup-form")


signup_form.addEventListener("submit", (event) => {
    event.preventDefault()
    form = event.target
    const form_data = new FormData(form)
    if (form_data.get("password").length < 4) {
        alert("Password must be longer than 4 characters")
    }
})
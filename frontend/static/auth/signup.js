const signup_form = document.querySelector("#signup-form")


signup_form.addEventListener("submit", (event) => {
    event.preventDefault()
    form = event.target
    const form_data = new FormData(form)
    if (! (form_data.get("email").includes("@"))) {
        alert("Invalid email format")
    }
    else {
        
    }
})
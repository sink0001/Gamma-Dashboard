

const watchlist_toggle = document.querySelector("#favourite-checkbox")


watchlist_toggle.addEventListener("click", async (event) => {
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
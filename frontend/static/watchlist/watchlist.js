

const removers = document.querySelectorAll(".watchlist-remove-button")
for (const remover of removers) {
    remover.addEventListener("click", async (event) => {
        const remover_button = event.target
        const ticker = remover_button.getAttribute("data-ticker")

        await fetch("/user_info/remove_ticker_from_watchlist", {
            method: "POST",
            body: JSON.stringify({ticker: ticker}),
            headers: {
                "Content-Type": "application/json"
            }
        }
        )
        location.reload()
    })
}
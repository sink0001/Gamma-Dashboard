
fetch("/heartbeat",{
    method: "POST"
})
setInterval(() => {
    fetch("/heartbeat",{
        method: "POST"
    })
}, 60000)
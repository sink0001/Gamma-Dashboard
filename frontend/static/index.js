
function get_session_cookie_id() {
    session = document.cookie.toString()
    session = session.replace("session=", "")
    return session
}


setInterval(() => {
    fetch("/heartbeat",{
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cookie: get_session_cookie_id() })
    })
}, 1000)
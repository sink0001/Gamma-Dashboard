# Gamma-dashboard
## feature overview
- This web-application allows users to search up a stocks ticker and get graphs of the stocks ratios such as its p/e ratio or its debt to equity ratio
- There are 2 graphs for each ratio depending on whether annual or quarterly is toggled
- Users can also signup (no email, only unique username) and once a user is logged in they can add/remove stocks to their watchlist
- In the watchlist they can click on a stock to be taken to its analysis page (the page with the ratio graphs)
- This web app was built for learning purposes
---
## tech-stack
- Backend
    - I'm using Flask as my web framework
    - I'm using the financial modeling prep API (for financial statements) and the Twelve data API (for stock prices) both on free tiers
- Data storage
    - I'm using PostgreSQL as a database for persistent user and user info storage (username, password, watchlist)
    - I'm using Redis to cache API responses because I get rate limited quickly on the free tier and calling the API everytime a new graph is requested is slow
- Frontend
    - I'm using chart.js for graphs but other than that just vanilla html, css and javascript

## My caching model
- I'm using server side caching where the keys are the session id that is assigned to the session cookie in the users browser when they start a new session on my site (this way I'm caching by session aswell so no sign-in required to use core functionality)
- When a user enters a stocks ticker (e.g. AAPL) I call both APIs to get all the financial statements and stuff that i need and I cache them under the users session id key
- Then when a user presses on say debt to equity the graph is rendered quickly as I cache the API response right away and can read from cache quickly and don't have to call any APIs repeatedly
- The way i achieve this is by having a heartbeat in my client-side code that posts a heartbeat every 60 seconds and then when that heartbeat is posted to the server i extend the time to live for the session id (which is my key in redis) by 61 seconds
- As a result the key gets deleted once the user closes their session and 1 minute passes
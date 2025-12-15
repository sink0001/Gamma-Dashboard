from frontend import create_app
import uuid
from flask import session
import redis


app = create_app()
redis_server = redis.Redis(host="localhost", port=6379)

@app.before_request
def before_request():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())


if __name__ == "__main__":
    app.run(debug=True)
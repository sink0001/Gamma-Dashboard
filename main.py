from frontend import create_app
from uuid import uuid4
from flask import session
import redis


app = create_app()


@app.before_request
def before_request():
    if "session_id" not in session:
        session["session_id"] = str(uuid4())


if __name__ == "__main__":
    app.run(debug=True)
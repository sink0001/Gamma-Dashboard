from frontend import create_app
import uuid
from flask import session
import redis
# TODO: once back on main branch, put finances and the statements into Stock class self after deserializing them and make api calls async, keep finances as is for now for easier testing

app = create_app()


@app.before_request
def before_request():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())


if __name__ == "__main__":
    app.run(debug=True)
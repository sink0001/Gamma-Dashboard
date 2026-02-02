from flask import current_app


def create_user(username: str, password: str) -> None:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        conn.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                     (username, password)
                     )
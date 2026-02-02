from flask import current_app


def create_user(username: str, password: str) -> None:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        conn.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                     (username, password)
                     )

def username_exists(username: str) -> bool:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        cur = conn.execute("SELECT * FROM users WHERE username = %s", [username])
        if cur.fetchone():
            return True
        return False
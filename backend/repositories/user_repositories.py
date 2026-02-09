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


def get_username_password(username: str) -> str | None:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        cur = conn.execute("SELECT password FROM users WHERE username = %s", [username])
        result = cur.fetchone()
        if result:
            return result[0]
        return None


def get_username_by_id(id: int) -> str | None:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        cur = conn.execute("SELECT username FROM users WHERE id = %s", [id])
        result = cur.fetchone()
        if result:
            return result[0]
        return None


def get_id_by_username(username: str) -> int | None:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        cur = conn.execute("SELECT id FROM users WHERE username = %s", [username])
        result = cur.fetchone()
        if result:
            return result[0]
        return None
 

def add_to_user_watchlist(user_id: int, to_add: str) -> None:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        conn.execute("""UPDATE users
                     SET stock_watchlist = array_append(stock_watchlist, %s)
                     WHERE id = %s""", [to_add, user_id]
                     )
        

def ticker_already_in_user_watchlist(user_id: int, ticker: str) -> bool:
    with current_app.pg_connection_pool.connection() as conn: # type:ignore
        cur = conn.execute("SELECT %s = ANY(stock_watchlist) FROM users WHERE id = %s", [ticker, user_id])
        result = cur.fetchone()
        if result:
            return True
        return False
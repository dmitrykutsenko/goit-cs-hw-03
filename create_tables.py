import psycopg2

from psycopg2 import Error
from contextlib import contextmanager


database = {
    "dbname": "task_manager",
    "user": "postgres",
    "password": "postgreser12",
    "host": "localhost",
    "port": 5432
}

@contextmanager
def create_connection(db_params):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        yield conn
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES status (id),
        user_id INTEGER REFERENCES users (id) ON DELETE CASCADE
    );
    """

    with create_connection(database) as conn:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_status_table)
        create_table(conn, sql_create_tasks_table)

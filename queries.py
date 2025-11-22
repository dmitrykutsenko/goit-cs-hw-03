import psycopg2
from psycopg2 import Error

from create_tables import create_connection, database


def get_tasks_by_user(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
    rows = cur.fetchall()
    cur.close()
    return rows


def get_tasks_by_status(conn, status_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status_id = %s;", (status_id,))
    rows = cur.fetchall()
    cur.close()
    return rows


def update_task_status(conn, task_id, new_status_id):
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status_id = %s WHERE id = %s;", (new_status_id, task_id))
    conn.commit()
    cur.close()
    return f"Task {task_id} updated to status {new_status_id}"


def get_users_without_tasks(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.fullname
        FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        WHERE t.id IS NULL;
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def insert_task(conn, title, description, status_id, user_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id;",
        (title, description, status_id, user_id)
    )
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return f"Task {task_id} created"


def get_unfinished_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');")
    rows = cur.fetchall()
    cur.close()
    return rows


def delete_task(conn, task_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    return f"Task {task_id} deleted"


def find_users_by_email(conn, pattern):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email LIKE %s;", (f"%{pattern}%",))
    rows = cur.fetchall()
    cur.close()
    return rows


def update_user_name(conn, user_id, new_name):
    cur = conn.cursor()
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s;", (new_name, user_id))
    conn.commit()
    cur.close()
    return f"User {user_id} renamed to {new_name}"


def count_tasks_by_status(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT s.name, COUNT(t.id)
        FROM status s
        LEFT JOIN tasks t ON s.id = t.status_id
        GROUP BY s.name;
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_tasks_by_user_domain(conn, domain):
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, t.title, u.email
        FROM tasks t
        JOIN users u ON t.user_id = u.id
        WHERE u.email LIKE %s;
    """, (f"%{domain}",))
    rows = cur.fetchall()
    cur.close()
    return rows


def get_tasks_without_description(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
    rows = cur.fetchall()
    cur.close()
    return rows


def get_users_with_inprogress_tasks(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT u.fullname, t.title
        FROM users u
        JOIN tasks t ON u.id = t.user_id
        JOIN status s ON t.status_id = s.id
        WHERE s.name = 'in progress';
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_users_task_count(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT u.fullname, COUNT(t.id) as task_count
        FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        GROUP BY u.fullname;
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


if __name__ == "__main__":
    with create_connection(database) as conn:
        print("1. Tasks by user 1:", get_tasks_by_user(conn, 1))
        print("2. Tasks with status 1:", get_tasks_by_status(conn, 1))
        print("3. Update task status:", update_task_status(conn, 1, 2))
        print("4. Users without tasks:", get_users_without_tasks(conn))
        print("5. Insert new task:", insert_task(conn, "Demo Task", "Demo Description", 1, 1))
        print("6. Unfinished tasks:", get_unfinished_tasks(conn))
        print("7. Delete task 1:", delete_task(conn, 1))
        print("8. Find users by email '@gmail.com':", find_users_by_email(conn, "@gmail.com"))
        print("9. Update user name:", update_user_name(conn, 1, "Updated User"))
        print("10. Count tasks by status:", count_tasks_by_status(conn))
        print("11. Tasks by user domain gmail.com:", get_tasks_by_user_domain(conn, "gmail.com"))
        print("12. Tasks without description:", get_tasks_without_description(conn))
        print("13. Users with in-progress tasks:", get_users_with_inprogress_tasks(conn))
        print("14. Users task count:", get_users_task_count(conn))

from psycopg2 import Error
from faker import Faker

import random

from create_tables import create_connection, database

fake = Faker()

def insert_user(conn, user):
    sql = """
    INSERT INTO users(fullname, email)
    VALUES (%s, %s)
    RETURNING id;
    """
    cur = conn.cursor()

    try:
        cur.execute(sql, user)
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Error as e:
        print(e)
    finally:
        cur.close()


def insert_status(conn, status_name):
    sql = """
    INSERT INTO status(name)
    VALUES (%s)
    ON CONFLICT (name) DO NOTHING
    RETURNING id;
    """
    cur = conn.cursor()

    try:
        cur.execute(sql, (status_name,))
        result = cur.fetchone()
        conn.commit()
        return result[0] if result else None
    except Error as e:
        print(e)
    finally:
        cur.close()


def insert_task(conn, task):
    sql = """
    INSERT INTO tasks(title, description, status_id, user_id)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """
    cur = conn.cursor()
    
    try:
        cur.execute(sql, task)
        task_id = cur.fetchone()[0]
        conn.commit()
        return task_id
    except Error as e:
        print(e)
    finally:
        cur.close()


if __name__ == '__main__':
    with create_connection(database) as conn:
        if conn is not None:
            # 1. Заповнюємо таблицю status
            statuses = ['new', 'in progress', 'completed']
            status_ids = {}
            for s in statuses:
                sid = insert_status(conn, s)
                if sid:
                    status_ids[s] = sid

            # 2. Генеруємо користувачів
            user_ids = []
            for _ in range(5):  # створимо 5 випадкових користувачів
                fullname = fake.name()
                email = fake.unique.email()
                uid = insert_user(conn, (fullname, email))
                user_ids.append(uid)

            # 3. Генеруємо завдання
            for _ in range(10):  # створимо 10 випадкових завдань
                title = fake.sentence(nb_words=5)
                description = fake.text(max_nb_chars=200)
                status_id = random.choice(list(status_ids.values()))
                user_id = random.choice(user_ids)
                tid = insert_task(conn, (title, description, status_id, user_id))
                print(f"Task {tid} created")
        else:
            print("Error! cannot create the database connection.")

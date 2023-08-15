import sqlite3


def main_():
    conn = sqlite3.connect("password.sqlite")
    cursor = conn.cursor()
    return cursor, conn


def create_table():
    cursor, conn = main_()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS password (login Varchar(32), email Varchar(32), password Varchar(32))"
    )
    conn.commit()
    conn.close()


def create_user_(user):
    create_table()
    cursor, conn = main_()
    cursor.execute("INSERT INTO password VALUES (?, ?, ?)", user)
    conn.commit()
    conn.close()


def authorization_(user):
    cursor, conn = main_()

    try:
        cursor.execute("SELECT 1 FROM password LIMIT 1")
    except sqlite3.OperationalError:
        conn.close()
        return False

    data_check = cursor.execute("SELECT * FROM password WHERE login = ? AND email = ? AND password = ?", user)
    result = data_check.fetchone()

    conn.close()
    return result is not None


def delete_user_(user):
    cursor, conn = main_()

    try:
        cursor.execute("SELECT 1 FROM password LIMIT 1")
    except sqlite3.OperationalError:
        conn.close()
        return False

    cursor.execute("DELETE FROM password WHERE login = ? AND email = ? AND password = ?", user)
    affected_rows = cursor.rowcount  
    conn.commit()

    conn.close()
    return affected_rows > 0  

import sqlite3


DATABASE_NAME = "bank_accounts.db"


def create_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bank_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT NOT NULL,
            balance REAL NOT NULL,
            account_type TEXT NOT NULL
        )
        """
    )
    connection.commit()


def add_account(connection, owner_name, balance, account_type):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO bank_accounts (owner_name, balance, account_type)
        VALUES (?, ?, ?)
        """,
        (owner_name, balance, account_type),
    )
    connection.commit()


def get_all_accounts(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, owner_name, balance, account_type
        FROM bank_accounts
        ORDER BY id
        """
    )
    return cursor.fetchall()


def main():
    connection = create_connection()

    create_table(connection)

    add_account(connection, "Alice Popescu", 1500.0, "checking")
    add_account(connection, "Bob Ionescu", 3200.5, "savings")

    accounts = get_all_accounts(connection)

    for account in accounts:
        print(account)

    connection.close()


if __name__ == "__main__":
    main()

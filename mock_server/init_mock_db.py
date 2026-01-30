"""
Mock DB 初始化腳本（可選）

建立 SQLite 資料庫與範例表（users、customers），
並可從 test_data 的 expected_result JSON 匯入一筆範例資料。
供日後擴充「Mock API 改由查詢 SQLite 回傳」時使用。
"""
import json
import os
import sqlite3

TEST_DATA_FOLDER = os.environ.get("TEST_DATA_FOLDER", "./test_data")
ENV = os.environ.get("ENV", "dev")
MOCK_DB_PATH = os.environ.get("MOCK_DB_PATH", "mock.db")


def _users_schema(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            is_active INTEGER,
            created_at TEXT
        )
    """)


def _customers_schema(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            customer_id TEXT,
            name TEXT,
            email TEXT,
            status TEXT,
            created_at TEXT
        )
    """)


def _insert_sample_users(cursor):
    path = os.path.join(
        TEST_DATA_FOLDER, ENV, "users", "expected_result", "get_users", "TC001.json"
    )
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for row in data.get("data", []):
        cursor.execute(
            """
            INSERT OR REPLACE INTO users (id, username, email, is_active, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                row.get("id"),
                row.get("username", ""),
                row.get("email", ""),
                1 if row.get("is_active", True) else 0,
                row.get("created_at", ""),
            ),
        )


def _insert_sample_customers(cursor):
    path = os.path.join(
        TEST_DATA_FOLDER, ENV, "customers", "expected_result",
        "get_customers", "TC001.json"
    )
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for row in data.get("data", []):
        cursor.execute(
            """
            INSERT OR REPLACE INTO customers (id, customer_id, name, email, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("id"),
                row.get("customer_id", ""),
                row.get("name", ""),
                row.get("email", ""),
                row.get("status", ""),
                row.get("created_at", ""),
            ),
        )


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = MOCK_DB_PATH if os.path.isabs(MOCK_DB_PATH) else os.path.join(base, MOCK_DB_PATH)
    d = os.path.dirname(db_path)
    if d:
        os.makedirs(d, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    _users_schema(cursor)
    _customers_schema(cursor)
    _insert_sample_users(cursor)
    _insert_sample_customers(cursor)
    conn.commit()
    conn.close()
    print(f"Mock DB 已建立: {db_path}")


if __name__ == "__main__":
    main()

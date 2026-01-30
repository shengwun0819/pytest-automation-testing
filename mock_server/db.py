"""
Mock DB 查詢模組

從 SQLite (mock.db) 查詢 users、customers，
供 Mock API 回傳與 expected_result 相同結構的 { data, pagination }。
"""
import os
import sqlite3
from typing import Any, Dict, List, Optional

MOCK_DB_PATH = os.environ.get("MOCK_DB_PATH", "mock.db")


def _get_db_path() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isabs(MOCK_DB_PATH):
        return MOCK_DB_PATH
    return os.path.join(base, MOCK_DB_PATH)


def _db_exists() -> bool:
    return os.path.isfile(_get_db_path())


def db_available() -> bool:
    """Mock DB 檔案是否存在（供 Mock API 判斷是否改從 DB 取資料）。"""
    return _db_exists()


def get_connection() -> Optional[sqlite3.Connection]:
    """取得 SQLite 連線；若檔案不存在則回傳 None。"""
    if not _db_exists():
        return None
    try:
        return sqlite3.connect(_get_db_path())
    except Exception:
        return None


def get_total(cursor: sqlite3.Cursor, table: str) -> int:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]


def fetch_users(limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """
    從 users 表查詢，回傳與 expected_result 格式一致的 list of dict。
    is_active 以 boolean 回傳。
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, is_active, created_at FROM users ORDER BY id LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "username": row["username"] or "",
                "email": row["email"] or "",
                "is_active": bool(row["is_active"]),
                "created_at": row["created_at"] or "",
            })
        return result
    finally:
        conn.close()


def fetch_customers(limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """從 customers 表查詢，回傳與 expected_result 格式一致的 list of dict。"""
    conn = get_connection()
    if not conn:
        return []
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, customer_id, name, email, status, created_at FROM customers ORDER BY id LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "customer_id": row["customer_id"] or "",
                "name": row["name"] or "",
                "email": row["email"] or "",
                "status": row["status"] or "",
                "created_at": row["created_at"] or "",
            })
        return result
    finally:
        conn.close()


def get_customers_total() -> int:
    conn = get_connection()
    if not conn:
        return 0
    try:
        cursor = conn.cursor()
        return get_total(cursor, "customers")
    finally:
        conn.close()


def get_users_total() -> int:
    conn = get_connection()
    if not conn:
        return 0
    try:
        cursor = conn.cursor()
        return get_total(cursor, "users")
    finally:
        conn.close()


def build_pagination_body(
    data: List[Dict[str, Any]],
    total: int,
    page: int,
    limit: int,
) -> Dict[str, Any]:
    """組出與 expected_result 一致的 { data, pagination }。"""
    total_pages = max(1, (total + limit - 1) // limit) if limit else 1
    return {
        "data": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
        },
    }

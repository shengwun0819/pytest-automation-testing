"""
Mock API Server

模擬 Gate/Hub 風格的 REST API：
- POST /v1/auth/login → 回傳 mock token
- GET /v1/users、GET /v1/customers → 優先從 Mock DB (SQLite) 查資料回傳；無 DB 時改從 test_data CSV/JSON 回傳

啟動：在專案根目錄執行
  python -m mock_server.app
  或
  flask --app mock_server.app:app run --port 5050
"""
import os

from flask import Flask, jsonify, request

from mock_server import db as mock_db
from mock_server.router import (
    _infer_cookie_type,
    find_case,
    get_mock_response,
)

app = Flask(__name__)

# 與 config.VERSION 對齊，例如 /v1
VERSION = os.environ.get("VERSION", "/v1")


# 是否從 Mock DB 取資料（預設 true；無 mock.db 或查詢失敗時會改從 CSV/JSON）
USE_MOCK_DB = os.environ.get("USE_MOCK_DB", "true").lower() in ("true", "1", "yes")


def _get_auth_header():
    return request.headers.get("Authorization") or request.headers.get("authorization")


def _parse_page_limit(default_limit=10):
    """從 request 解析 page、limit，回傳 (page, limit, offset)。"""
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        limit = max(1, min(100, int(request.args.get("limit", default_limit))))
    except (TypeError, ValueError):
        limit = default_limit
    offset = (page - 1) * limit
    return page, limit, offset


# ---------- Auth ----------
@app.route(f"{VERSION}/auth/login", methods=["POST"])
def login():
    """Mock OAuth2 登入：任意 account/password 皆回傳固定 token。"""
    return jsonify({"token": "mock_token_for_testing", "cookie": "mock_token_for_testing"}), 200


# ---------- Users ----------
@app.route(f"{VERSION}/users", methods=["GET"])
@app.route(f"{VERSION}/users/", methods=["GET"])
def get_users():
    query_string = request.query_string.decode("utf-8") if request.query_string else ""
    if query_string and not query_string.startswith("?"):
        query_string = "?" + query_string
    cookie_type = _infer_cookie_type(_get_auth_header())
    if cookie_type != "auth":
        return jsonify({"error": {"code": "E002", "message": "Unauthorized access"}}), 401

    # 僅在「成功案例」(CSV 對應 status 2xx) 且 Mock DB 存在時從 DB 取資料；其餘仍用 CSV/JSON（含 400 等）
    row = find_case("users", "get_users", query_string, cookie_type)
    if row and int(row.get("status_code", 200)) in range(200, 300) and USE_MOCK_DB and mock_db.db_available():
        try:
            page, limit, offset = _parse_page_limit()
            data = mock_db.fetch_users(limit=limit, offset=offset)
            total = mock_db.get_users_total()
            body = mock_db.build_pagination_body(data, total, page, limit)
            return jsonify(body), 200
        except Exception:
            pass  # fallback to file

    status, body = get_mock_response(
        module="users",
        api_name="get_users",
        csv_file_name="get_users",
        query_string=query_string,
        cookie_type=cookie_type,
    )
    return jsonify(body), status


# ---------- Customers ----------
@app.route(f"{VERSION}/customers", methods=["GET"])
@app.route(f"{VERSION}/customers/", methods=["GET"])
def get_customers():
    query_string = request.query_string.decode("utf-8") if request.query_string else ""
    if query_string and not query_string.startswith("?"):
        query_string = "?" + query_string
    cookie_type = _infer_cookie_type(_get_auth_header())
    if cookie_type != "auth":
        return jsonify({"error": {"code": "E002", "message": "Unauthorized access"}}), 401

    row = find_case("customers", "get_customers", query_string, cookie_type)
    if row and int(row.get("status_code", 200)) in range(200, 300) and USE_MOCK_DB and mock_db.db_available():
        try:
            page, limit, offset = _parse_page_limit()
            data = mock_db.fetch_customers(limit=limit, offset=offset)
            total = mock_db.get_customers_total()
            body = mock_db.build_pagination_body(data, total, page, limit)
            return jsonify(body), 200
        except Exception:
            pass

    status, body = get_mock_response(
        module="customers",
        api_name="get_customers",
        csv_file_name="get_customers",
        query_string=query_string,
        cookie_type=cookie_type,
    )
    return jsonify(body), status


# ---------- Health ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "mock-api"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("MOCK_SERVER_PORT", "5050"))
    app.run(host="0.0.0.0", port=port, debug=False)

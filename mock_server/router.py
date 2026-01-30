"""
Mock Server 路由邏輯

根據 request 的 path、query_string、認證狀態，
對應 test_data 的 CSV 與 expected_result JSON，回傳預設回應。
"""
import json
import os
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


# 預設與 test_data 一致
TEST_DATA_FOLDER = os.environ.get("TEST_DATA_FOLDER", "./test_data")
ENV = os.environ.get("ENV", "dev")


def _normalize_query(q: Optional[str]) -> str:
    """統一 query 格式以便與 CSV 比對（去掉開頭 ?、空白）"""
    if not q or not str(q).strip():
        return ""
    s = str(q).strip()
    return s if s.startswith("?") else f"?{s}"


def _infer_cookie_type(auth_header: Optional[str]) -> str:
    """
    依 Authorization header 推斷 CSV 的 cookie 類型。
    與 utils.auth 的 get_cookie 類型對齊：auth, no-auth, auth_invalid, auth_expired 等。
    """
    if not auth_header or not str(auth_header).strip() or str(auth_header).strip().lower() == "none":
        return "no-auth"
    lower = str(auth_header).lower()
    if "invalid" in lower:
        return "auth_invalid"
    if "expired" in lower:
        return "auth_expired"
    if "random" in lower:
        return "random"
    return "auth"


def load_csv_cases(module: str, file_name: str) -> List[Dict[str, Any]]:
    """
    讀取 test_data 下的 CSV（與 FileProcess 路徑一致，header=0 以配合本專案 CSV）。
    """
    path = os.path.join(TEST_DATA_FOLDER, ENV, module, f"{file_name}.csv")
    if not os.path.isfile(path):
        return []
    df = pd.read_csv(path, header=0, dtype=str).dropna(how="all").fillna("")
    return [dict(df.loc[i]) for i in range(len(df))]


def find_case(
    module: str,
    file_name: str,
    query_string: str,
    cookie_type: str,
) -> Optional[Dict[str, Any]]:
    """
    依 query_string 與 cookie 類型找到對應的 CSV 列（一筆測試案例）。
    """
    cases = load_csv_cases(module, file_name)
    q = _normalize_query(query_string)
    for row in cases:
        row_q = _normalize_query(row.get("query_string", ""))
        row_cookie = (row.get("cookie") or "").strip().lower()
        if row_q == q and row_cookie == cookie_type.lower():
            return row
    return None


def load_expected_json(module: str, api_name: str, case_id: str) -> Optional[Dict[str, Any]]:
    """讀取 expected_result 下的 JSON。"""
    path = os.path.join(
        TEST_DATA_FOLDER, ENV, module, "expected_result", api_name, f"{case_id}.json"
    )
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_mock_response(
    module: str,
    api_name: str,
    csv_file_name: str,
    query_string: str,
    cookie_type: str,
) -> Tuple[int, Dict[str, Any]]:
    """
    依 path 對應的 module/api、query、認證，回傳 (status_code, json_body)。
    找不到案例時回傳 404 + 說明；4xx/5xx 若無預期 JSON 則回傳通用錯誤結構。
    """
    row = find_case(module, csv_file_name, query_string, cookie_type)
    if not row:
        return 404, {"error": {"message": "No matching test case in CSV"}}

    status = int(row.get("status_code", 200))
    case_id = (row.get("case_id") or "").strip()

    if status >= 200 and status < 300 and case_id:
        body = load_expected_json(module, api_name, case_id)
        if body is not None:
            return status, body

    # 4xx/5xx 若有對應 expected JSON 也可放進 expected_result（可選）
    body = load_expected_json(module, api_name, case_id)
    if body is not None:
        return status, body
    return status, {"error": {"message": f"Mock error for case {case_id}", "code": status}}

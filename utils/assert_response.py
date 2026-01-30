"""
回應斷言工具
提供統一的 API 回應驗證方法
"""
import common.constants as constants


class Assert:
    """
    提供統一的 API 請求發送和回應驗證方法
    """

    def request_switch(
        self,
        method: str,
        cookie_code: str,
        path: str,
        api,
        cookie: str,
        body: dict = {},
        params_query: str = '',
        service: str = 'service_a'
    ):
        """
        Args:
            method: HTTP 方法
            cookie_code: 認證類型
            path: API 路徑
            api: API 方法物件
            cookie: 認證 cookie/token
            body: 請求 body
            params_query: 查詢參數字串
            service: 服務選擇

        Returns:
            requests.Response: HTTP 回應物件
        """
        return api.method_switch(
            cookie=cookie,
            method=method,
            body=body,
            params_query=params_query,
            cookie_code=cookie_code,
            path=path,
            service=service
        )

    def validate_status(self, status_code: int, case_input: dict):
        """
        驗證 HTTP 狀態碼

        Args:
            status_code: 實際回應的狀態碼
            case_input: 測試案例輸入（包含預期狀態碼）

        Raises:
            AssertionError: 當狀態碼不符合預期時
        """
        try:
            assert str(status_code) == case_input['status_code']
        except AssertionError:
            print(
                f"Status code mismatch. "
                f"Expected: {case_input.get('status_code', 'N/A')}, "
                f"Actual: {status_code}"
            )
            raise AssertionError

    def validate_error_stack(self, resp_json: dict):
        """
        驗證錯誤堆疊資訊

        某些 API 會在錯誤回應中包含 stack trace，
        這個方法會驗證 stack 的類型並移除它以便比較

        Args:
            resp_json: API 回應 JSON

        Returns:
            dict: 處理後的 JSON（移除 stack）
        """
        resp_json_ = resp_json.copy()

        if 'data' not in resp_json_:
            if 'error' in resp_json_ and 'stack' in resp_json_['error']:
                assert isinstance(resp_json_['error']['stack'], list)
                del resp_json_['error']['stack']
        else:
            if (
                'error' in resp_json_['data'][0] and
                'stack' in resp_json_['data'][0]['error']
            ):
                assert isinstance(
                    resp_json_['data'][0]['error']['stack'], list)
                del resp_json_['data'][0]['error']['stack']

        return resp_json_

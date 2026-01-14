"""
API 基礎類別
封裝 HTTP 請求的通用邏輯
"""
import requests

import config


class BaseAPI:
    """
    API 請求基礎類別

    提供統一的 HTTP 請求方法，支援多服務切換
    """
    service_a_base_url = config.SERVICE_A_BASE_URL
    service_b_base_url = config.SERVICE_B_BASE_URL
    version = config.VERSION

    def request(
        self,
        method: str,
        path: str,
        params_query: str = '',
        service: str = 'service_a',
        **kwargs
    ):
        """
        發送 HTTP 請求

        Args:
            method: HTTP 方法 (GET, POST, PUT, PATCH, DELETE)
            path: API 路徑
            params_query: 查詢參數字串 (例如: ?page=1&limit=10)
            service: 服務選擇 ('service_a' 或 'service_b')
            **kwargs: 其他 requests 參數 (headers, json, data 等)

        Returns:
            requests.Response: HTTP 回應物件

        Raises:
            requests.exceptions.RequestException: 請求失敗時
        """
        base_url = ''
        if service == 'service_a':
            base_url = f"{self.service_a_base_url}{self.version}{path}{params_query}"
        else:
            base_url = f"{self.service_b_base_url}{self.version}{path}{params_query}"

        try:
            # 預設 timeout 為 20 秒，等待資料傳輸完成
            print(f'>> API PATH: {method} {base_url}')
            response = requests.request(method, base_url, timeout=20, **kwargs)
            # 取消註解以下行以查看回應內容（用於除錯）
            # print(f'<< API RESPONSE: {response.status_code} {response.text}')
        except requests.exceptions.RequestException as err:
            raise requests.exceptions.RequestException(err)

        return response

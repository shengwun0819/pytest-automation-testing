"""
範例 API 方法
展示如何實作具體的 API 端點
"""
from api.base_api import BaseAPI
from utils import auth


class APIMethod(BaseAPI):
    """
    範例 API 方法類別
    
    繼承 BaseAPI，提供具體的 API 端點方法
    可以根據實際需求擴展更多方法
    """
    
    def method_switch(
        self,
        method: str,
        path: str,
        cookie: str,
        cookie_code: str = 'auth',
        params_query: str = '',
        body: dict = {},
        service: str = 'service_a'
    ):
        """
        統一的 API 請求方法
        
        Args:
            method: HTTP 方法
            path: API 路徑
            cookie: 認證 cookie/token
            cookie_code: 認證類型 ('auth', 'admin' 等)
            params_query: 查詢參數字串
            body: 請求 body (dict)
            service: 保留參數，目前僅使用 Service A
        
        Returns:
            requests.Response: HTTP 回應物件
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth.get_cookie(
                _type=cookie_code,
                cookie=cookie,
                service=service
            )
        }
        
        return self.request(
            method=method,
            path=path,
            headers=headers,
            params_query=params_query,
            json=body,
            service=service
        )

from api.base_api import BaseAPI
from utils import auth


class APIMethod(BaseAPI):
    
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
        Args:
            method: HTTP 方法
            path: API 路徑
            cookie: 認證 cookie/token
            cookie_code: 認證類型 ('auth', 'admin' 等)
            params_query: 查詢參數字串
            body: 請求 body (dict)
            service: 保留參數，目前僅使用 Service A
        
        Returns:
            requests.Response: HTTP response object
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

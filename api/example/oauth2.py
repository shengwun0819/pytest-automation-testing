import config
import requests
from api.base_api import BaseAPI


class OAuth2(BaseAPI):
    """
    OAuth2 認證類別
    
    處理使用者登入和 token 取得
    """
    
    def post_oauth2(
        self,
        account: str,
        credential: str,
        service: str = 'service_a'
    ):
        """
        執行 OAuth2 登入
        
        Args:
            account: 使用者帳號
            credential: 使用者密碼
            service: 保留參數，目前僅使用 Service A
        
        Returns:
            str: 認證 token/cookie
        """
        # 根據實際 API 調整登入端點和請求格式
        login_path = '/auth/login'
        login_body = {
            'account': account,
            'password': credential
        }
        
        url = f"{self.service_a_base_url}{self.version}{login_path}"
        
        try:
            response = requests.post(
                url,
                json=login_body,
                timeout=20
            )
            response.raise_for_status()
            
            # 根據實際 API 回應格式調整
            # 假設回應格式為: {"token": "xxx"} 或 {"data": {"cookie": "xxx"}}
            resp_json = response.json()
            
            # 從回應中提取 token/cookie
            if 'token' in resp_json:
                return resp_json['token']
            elif 'data' in resp_json and 'cookie' in resp_json['data']:
                return resp_json['data']['cookie']
            elif 'cookie' in resp_json:
                return resp_json['cookie']
            else:
                # 如果 API 使用 Set-Cookie header
                if 'Set-Cookie' in response.headers:
                    return response.headers['Set-Cookie']
                else:
                    raise ValueError("無法從回應中取得認證資訊")
        
        except requests.exceptions.RequestException as err:
            raise requests.exceptions.RequestException(
                f"OAuth2 登入失敗: {err}"
            )

"""
認證工具
處理各種認證類型的 token/cookie 生成
"""
import pytest


def get_cookie(_type: str, cookie: str, service: str = 'service_a'):
    """
    根據認證類型取得 cookie/token

    Args:
        _type: 認證類型 ('auth', 'no-auth', 'auth_invalid', 'auth_expired' 等)
        cookie: 有效的認證 cookie/token
        service: 服務選擇（用於多服務場景）

    Returns:
        str or None: 認證 token/cookie，或 None（無認證）

    Raises:
        SystemExit: 當認證類型不支援時
    """
    wrong_type = ['auth_invalid', 'random', 'auth_expired']

    if _type == 'no-auth':
        return None
    if _type == 'auth':
        return cookie
    if _type in wrong_type:
        # 可以根據需求實作無效 token 的生成邏輯
        # 這裡返回一個明顯無效的 token
        if _type == 'auth_invalid':
            return 'invalid_token_12345'
        elif _type == 'auth_expired':
            return 'expired_token_12345'
        else:
            return 'random_token_12345'
    else:
        pytest.exit(
            f"This cookie type is not supported: {_type}",
            returncode=1
        )


def get_x_api_key(_type: str, x_api_key: str):
    """
    根據認證類型取得 API Key

    Args:
        _type: 認證類型 ('auth', 'no-auth' 等)
        x_api_key: 有效的 API Key

    Returns:
        str or None: API Key，或 None（無認證）

    Raises:
        SystemExit: 當認證類型不支援時
    """
    if _type == 'no-auth':
        return None
    if _type == 'auth':
        return x_api_key
    else:
        pytest.exit(
            f"This x_api_key type is not supported: {_type}",
            returncode=1
        )

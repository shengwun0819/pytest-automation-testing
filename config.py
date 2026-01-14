"""
配置管理模組
統一管理環境變數和配置資訊
"""
import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key, default=None, is_required=True):
    """
    取得環境變數
    
    Args:
        key: 環境變數名稱
        default: 預設值
        is_required: 是否為必需項
    
    Returns:
        環境變數值
    
    Raises:
        ValueError: 當必需項不存在時
    """
    env_value = os.getenv(key)
    if is_required:
        if env_value is None:
            raise ValueError(f'{key} is required')
        return env_value
    return env_value or default


# ============================================
# 環境設定
# ============================================
ENV = get_env('ENV', default='dev')
VERSION = get_env('VERSION', default='/v1')

# ============================================
# Service A 配置（對應原始專案中的 ORI）
# ============================================
SERVICE_A_BASE_URL = get_env('SERVICE_A_BASE_URL')
SERVICE_A_ACCOUNT = get_env('SERVICE_A_ACCOUNT')
SERVICE_A_PASSWORD = get_env('SERVICE_A_PASSWORD')

# ============================================
# Service B 配置（對應原始專案中的 BEN）
# ============================================
SERVICE_B_BASE_URL = get_env('SERVICE_B_BASE_URL')
SERVICE_B_ACCOUNT = get_env('SERVICE_B_ACCOUNT')
SERVICE_B_PASSWORD = get_env('SERVICE_B_PASSWORD')

# ============================================
# 測試資料設定
# ============================================
TEST_DATA_FOLDER = get_env('TEST_DATA_FOLDER', default='./test_data')

# ============================================
# 可選配置（用於 CI/CD）
# ============================================
AWS_S3_BUCKET_NAME = get_env('AWS_S3_BUCKET_NAME', is_required=False)
SLACK_WEBHOOK_URL = get_env('SLACK_WEBHOOK_URL', is_required=False)
REPORT_URL_EXPIRED_DATE = get_env('REPORT_URL_EXPIRED_DATE', is_required=False)
GITHUB_ACTOR = get_env('GITHUB_ACTOR', is_required=False)
COMMIT_SHA = get_env('COMMIT_SHA', is_required=False)
GITHUB_HEAD_REF = get_env('GITHUB_HEAD_REF', is_required=False)
GITHUB_REPOSITORY = get_env('GITHUB_REPOSITORY', is_required=False)

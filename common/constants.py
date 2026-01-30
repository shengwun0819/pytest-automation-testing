"""
常數定義
定義測試中使用的各種常數和枚舉
"""
from enum import Enum


class ErrorCode(Enum):
    """
    錯誤代碼枚舉
    根據實際 API 定義調整
    """
    INVALID_INPUT = ('E001', 'Invalid input parameter')
    UNAUTHORIZED = ('E002', 'Unauthorized access')
    NOT_FOUND = ('E003', 'Resource not found')
    INTERNAL_ERROR = ('E999', 'Internal server error')

    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[1]

    @classmethod
    def get(cls, code):
        """根據代碼取得錯誤枚舉"""
        try:
            return cls[code]
        except KeyError:
            return None


# 地址類型（範例）
ADDRESS_TYPES = [
    "HOME",
    "BIZZ",
    "GEOG"
]

# 國家代碼類型（範例）
NATIONAL_IDENTIFIER_TYPES = [
    "ARNU",  # Alien Registration Number
    "CCPT",  # Passport Number
    "RAID",  # Registration Authority Identifier
    "DRLC",  # Driver's License Number
    "FIIN",  # Financial Institution Identifier
    "TXID",  # Tax Identification Number
    "SOCS",  # Social Security Number
    "IDCD",  # Identity Card Number
    "LEIX",  # Legal Entity Identifier
    "MISC"   # Miscellaneous
]


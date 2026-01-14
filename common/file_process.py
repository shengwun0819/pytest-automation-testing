"""
檔案處理工具
處理 CSV、JSON、TXT 等測試資料檔案
"""
import json

import pandas as pd

import config

testdata_folder = config.TEST_DATA_FOLDER
env = config.ENV


class FileProcess:
    """
    檔案處理類別

    提供讀取 CSV、JSON、TXT 等檔案的方法
    """

    @classmethod
    def read_csv_data(cls, file_name: str, path: str):
        """
        讀取 CSV 測試資料

        Args:
            file_name: CSV 檔案名稱（不含副檔名）
            path: 檔案所在路徑（相對於 test_data/{env}/）

        Returns:
            list: 包含字典的列表，每個字典代表一筆測試案例
        """
        file_path = f"./{testdata_folder}/{env}/{path}/{file_name}"
        sheet = pd.read_csv(
            filepath_or_buffer=f"{file_path}.csv",
            header=1,  # 從第二行開始讀取（第一行為標題）
            dtype=str
        ).dropna(how='all').reset_index(drop=True)  # 移除完全為空的列

        # 將 NaN 值替換為空字串
        sheet = sheet.where(pd.notnull(sheet), '')

        # 轉換為字典列表
        return [dict(sheet.loc[index]) for index in range(len(sheet))]

    @classmethod
    def read_json(cls, path: str):
        """
        讀取 JSON 檔案

        Args:
            path: JSON 檔案路徑

        Returns:
            dict or list: JSON 內容
        """
        with open(path, 'r', encoding='utf-8') as file_input:
            return json.loads(file_input.read())

    @classmethod
    def read_txt(cls, file_name: str, path: str):
        """
        讀取 TXT 檔案

        Args:
            file_name: TXT 檔案名稱（不含副檔名）
            path: 檔案所在路徑

        Returns:
            list: 以逗號分隔的內容列表
        """
        file_path = f"./{testdata_folder}/{env}/{path}/{file_name}.txt"
        with open(file_path, 'r', encoding='utf-8') as file_input:
            content = file_input.read()
            content_list = content.split(',')
            return [item.strip() for item in content_list if item.strip()]

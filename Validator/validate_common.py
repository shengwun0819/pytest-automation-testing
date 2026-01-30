"""
通用驗證器
提供 API 回應的驗證功能
"""
from common.file_process import FileProcess
from deepdiff import DeepDiff


class Validator:
    """
    通用驗證器類別
    
    用於驗證 API 回應是否符合預期結果
    """
    
    def __init__(
        self,
        api_tag: str,
        resp_json: dict,
        expected_path: str
    ):
        """
        初始化驗證器
        
        Args:
            api_tag: API 標籤（用於識別 API）
            resp_json: 實際 API 回應 JSON
            expected_path: 預期結果 JSON 檔案路徑
        """
        self.api_tag = api_tag
        self.resp_json = resp_json
        self.expected_resp = FileProcess.read_json(expected_path)
    
    def validate(self):
        """
        執行驗證
        
        比較實際回應和預期結果，並顯示差異
        """
        try:
            self.root_check(self.resp_json, self.expected_resp)
        except (KeyError, AssertionError):
            self.find_different(self.expected_resp, self.resp_json)
            assert self.resp_json == self.expected_resp
    
    def root_check(self, response: dict, expected: dict):
        """
        根層級檢查
        
        Args:
            response: 實際回應
            expected: 預期結果
        """
        self.find_different(expected, response)
        assert response == expected
    
    def find_different(self, expected_resp: dict, resp_json: dict):
        """
        找出差異並格式化輸出
        
        Args:
            expected_resp: 預期回應
            resp_json: 實際回應
        """
        def format_value_changes(path: str, value: dict) -> str:
            return (
                "Value of items been Changes:\n"
                f"Path: {path}\n"
                f"Expected value: {value['old_value']}\n"
                f"Actual value: {value['new_value']}\n"
            )
        
        def format_type_changes(key: str, change: dict) -> str:
            return (
                "Type of items been Changes:\n"
                f"Path: {key}\n"
                f"Expected type: {change['old_type']}\n"
                f"Actual type: {change['new_type']}\n"
            )
        
        def format_added_items(items: list) -> str:
            result = "Items added:\n"
            for item in items:
                if isinstance(item, str):
                    value = self._get_simple_value(resp_json, item)
                    result += f"- {item} = {value}\n"
                else:
                    result += f"- {item}\n"
            return result
        
        def format_removed_items(items: list) -> str:
            result = "Items Removed:\n"
            for item in items:
                if isinstance(item, str):
                    value = self._get_simple_value(expected_resp, item)
                    result += f"- {item} = {value}\n"
                else:
                    result += f"- {item}\n"
            return result
        
        diff_handlers = {
            'values_changed': lambda diff: [
                format_value_changes(path, value)
                for path, value in diff['values_changed'].items()
            ],
            'type_changes': lambda diff: [
                format_type_changes(key, change)
                for key, change in diff['type_changes'].items()
            ],
            'dictionary_item_added': lambda diff: [
                format_added_items(diff['dictionary_item_added'])
            ],
            'dictionary_item_removed': lambda diff: [
                format_removed_items(diff['dictionary_item_removed'])
            ]
        }
        
        diff = DeepDiff(expected_resp, resp_json)
        
        if diff:
            print("=== Show Matching details if DeepDiff error ===")
            print(f"expected result: {expected_resp}\n")
            print(f"actual result: {resp_json}")
            print("==================")
        
        for change_type, handler in diff_handlers.items():
            if change_type in diff:
                for output in handler(diff):
                    print(output)
    
    def _get_simple_value(self, data: dict, path: str):
        """
        根據路徑取得值
        
        Args:
            data: 資料字典
            path: 路徑字串（例如: "root['key']['subkey']"）
        
        Returns:
            路徑對應的值，或錯誤訊息
        """
        try:
            if path.startswith('root'):
                path = path[4:]
            
            if not path:
                return data
            
            safe_path = f"data{path}"
            return eval(safe_path, {"data": data})
        except Exception:
            return "Can not get value."
    
    def is_valid_type(self, item, valid_type, result: bool = True):
        """
        驗證類型
        
        Args:
            item: 要驗證的項目
            valid_type: 預期的類型
            result: 預期的結果（True/False）
        
        Returns:
            bool: 是否符合預期
        """
        return isinstance(item, valid_type) == result

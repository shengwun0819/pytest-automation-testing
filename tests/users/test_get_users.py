"""
使用者 API 測試範例
展示如何使用框架進行 API 測試
"""
import allure
import config
import pytest
from api.example.api_method import APIMethod
from api.example.oauth2 import OAuth2
from common.file_process import FileProcess
from utils.assert_response import Assert
from Validator.validate_common import Validator

testdata_folder = config.TEST_DATA_FOLDER
env = config.ENV


@allure.epic("Users")
@allure.feature("Get Users")
class TestGetUsers:
    oauth2 = OAuth2()
    api = APIMethod()
    
    path = '/users'
    
    def setup_class(self):
        """
        測試類別初始化
        在執行測試前進行認證
        """
        self.auth = self.oauth2.post_oauth2(
            account=config.SERVICE_A_ACCOUNT,
            credential=config.SERVICE_A_PASSWORD,
            service='service_a'
        )
    
    @allure.story("Positive/Negative Test Cases")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        'case_input',
        FileProcess.read_csv_data(file_name='get_users', path='users')
    )
    @pytest.mark.order(2)
    def test_get_users(self, is_run, case_input):
        """
        測試取得使用者列表
        
        Args:
            is_run: 是否執行測試 fixture
            case_input: 測試案例輸入（從 CSV 讀取）
        """
        allure.dynamic.title(
            f"{case_input['case_id']} - {case_input['case_description']}"
        )
        
        if not is_run(run=case_input['is_run'], tags=case_input['tags']):
            pytest.skip('Skip')
        
        resp = Assert.request_switch(
            self,
            method='GET',
            cookie_code=case_input['cookie'],
            params_query=case_input['query_string'],
            path=self.path,
            api=self.api,
            cookie=self.auth
        )
        
        resp_json = resp.json()
        
        Assert.validate_status(
            self,
            status_code=resp.status_code,
            case_input=case_input
        )
        
        validator = Validator(
            resp_json=resp_json,
            expected_path=(
                f"./{testdata_folder}/{env}/users/expected_result/"
                f"get_users/{case_input['case_id']}.json"
            ),
            api_tag='get_users'
        )
        validator.validate()
        
        print(
            f"{case_input['case_id']}, {case_input['case_description']}\n"
            f"API Path={case_input['query_string']}"
        )

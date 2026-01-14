"""
客戶 API 測試範例
展示如何測試客戶相關的 API 端點
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


@allure.epic("Customers")
@allure.feature("Get Customers")
class TestGetCustomers:
    """
    取得客戶列表測試類別
    """
    oauth2 = OAuth2()
    api = APIMethod()
    
    path = '/customers'
    
    def setup_class(self):
        """測試類別初始化"""
        self.auth = self.oauth2.post_oauth2(
            account=config.SERVICE_A_ACCOUNT,
            credential=config.SERVICE_A_PASSWORD,
            service='service_a'
        )
    
    @allure.story("Positive Test Cases")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        'case_input',
        FileProcess.read_csv_data(file_name='get_customers', path='customers')
    )
    @pytest.mark.order(1)
    def test_get_customers(self, is_run, case_input):
        """
        測試取得客戶列表
        
        Args:
            is_run: 是否執行測試
            case_input: 測試案例輸入
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
                f"./{testdata_folder}/{env}/customers/expected_result/"
                f"get_customers/{case_input['case_id']}.json"
            ),
            api_tag='get_customers'
        )
        validator.validate()
        
        print(
            f"{case_input['case_id']}, {case_input['case_description']}\n"
            f"API Path={case_input['query_string']}"
        )

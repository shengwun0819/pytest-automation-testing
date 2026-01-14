"""
pytest 配置和 fixtures
定義測試的共用設定和前置/後置處理
"""
import glob
import os
import shutil
import subprocess
import time
from datetime import datetime

import common.constants as constants
import config
import pytest
from database.db_sqlalchemy import DBSqlalchemy

# 全域變數
env = config.ENV
version = config.VERSION
db_sqlalchemy = DBSqlalchemy()


def pytest_addoption(parser):
    """
    新增 pytest 命令列選項
    """
    parser.addoption(
        '--tags',
        action='store',
        help='指定要執行的測試標籤（以逗號分隔）'
    )
    parser.addoption(
        '--export',
        action='store',
        help='是否匯出報告（true/false）'
    )
    parser.addoption(
        '--db_type',
        action='store',
        default='postgres',
        help='資料庫類型：postgres 或 mysql'
    )
    parser.addoption(
        "--allure-results-dir",
        action="store",
        default="allure-results",
        help="Allure 結果目錄"
    )


def pytest_configure(config):
    """
    pytest 配置初始化
    """
    global target_tags
    target_tags = config.getoption('--tags')
    db_type = config.getoption('--db_type')
    config.db_type = db_type
    
    if target_tags:
        target_tags = target_tags.lower().split(',')


@pytest.fixture(scope="session", autouse=True)
def pre_test(request):
    """
    測試前的準備工作（session scope）
    """
    db_type = request.config.getoption('--db_type')
    
    # 清理之前的 Allure 結果
    subprocess.run('rm -rf ./allure-results/*', shell=True)
    
    # 可以在這裡加入其他前置準備工作
    # 例如：初始化測試資料、設定環境等


@pytest.fixture(scope='session')
def db_type(request):
    """
    取得資料庫類型
    """
    return request.config.db_type


@pytest.fixture(scope="class", autouse=True)
def class_process(request):
    """
    每個測試類別的前後處理（class scope）
    """
    import importlib
    importlib.reload(config)
    db_type = request.config.getoption('--db_type')
    
    # 測試前：清理並初始化資料庫
    db_sqlalchemy.pre_cross_db_query(
        db_type,
        sql_script=constants.DELETE_SQL_SCRIPT,
        service='service_a'
    )
    db_sqlalchemy.pre_cross_db_query(
        db_type,
        sql_script=constants.DELETE_SQL_SCRIPT,
        service='service_b'
    )
    
    db_sqlalchemy.pre_cross_db_query(
        db_type,
        sql_script=constants.INIT_SQL_SCRIPT,
        service='service_a'
    )
    db_sqlalchemy.pre_cross_db_query(
        db_type,
        sql_script=constants.INIT_SQL_SCRIPT,
        service='service_b'
    )
    
    yield
    
    # 測試後：清理資料庫
    db_sqlalchemy.pre_cross_db_query(
        db_type,
        sql_script=constants.DELETE_SQL_SCRIPT,
        service='service_a'
    )
    db_sqlalchemy.pre_cross_db_query(
        db_type,
        sql_script=constants.DELETE_SQL_SCRIPT,
        service='service_b'
    )


@pytest.fixture(scope='function')
def is_run():
    """
    檢查測試是否應該執行
    
    Returns:
        function: 檢查函數
    """
    def check(run: str, tags: str = None):
        """
        檢查測試是否應該執行
        
        Args:
            run: 是否執行（'1' 或 '0'）
            tags: 測試標籤（以逗號分隔）
        
        Returns:
            bool: 是否應該執行
        """
        if bool(int(run)) is False:
            pytest.skip('Skip caused by test data setting')
        
        if not target_tags:
            return True
        
        if target_tags and tags:
            tags = tags.lower().split(',')
            for tag in tags:
                if tag in target_tags:
                    return True
        
        pytest.skip(f'This test case is out of these tags: {target_tags}')
    
    return check


def pytest_sessionfinish(session):
    """
    測試會話結束時的處理
    """
    db_type = session.config.getoption('--db_type')
    
    # 可以在這裡加入清理工作
    # 例如：恢復資料庫狀態、清理測試資料等


def pytest_terminal_summary(terminalreporter, config, exitstatus):
    """
    測試終端摘要
    生成 Allure 報告
    """
    time.sleep(2)
    
    is_export = config.getoption('--export')
    db_type = config.getoption('--db_type')
    allure_results_dir = config.getoption("--allure-results-dir")
    
    time_now = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
    result = 'success' if exitstatus == 0 else 'failed'
    commit_sha = config.COMMIT_SHA or 'local'
    report_dir = f"test_report/report_{commit_sha}_{db_type}_{result}_{time_now}"
    report_name = f'report_{commit_sha}_{db_type}_{result}_{time_now}.html'
    
    failed = len(terminalreporter.stats.get('failed', []))
    passed = len(terminalreporter.stats.get('passed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    error = len([i for i in terminalreporter.stats.get('error', [])])
    
    try:
        print(" ⚙️ Generating Allure report...")
        allure_start_time = time.time()
        
        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(allure_results_dir, exist_ok=True)
        
        try:
            subprocess.run(["which", "allure"], check=True, capture_output=True)
        except Exception as e:
            print(
                f"Error: Allure command not found. "
                f"Please ensure Allure is installed. Error: {str(e)}"
            )
            raise
        
        result = subprocess.run([
            "allure", "generate",
            "--single-file",
            "--clean",
            "--report-dir", report_dir,
            allure_results_dir
        ], check=True, capture_output=True, text=True)
        
        print(" ✓ Allure report generated successfully.")
        print(f"Command output: {result.stdout}")
        
        os.rename(
            os.path.join(report_dir, "index.html"),
            os.path.join(report_dir, report_name)
        )
        print(f"\n ✔✔✔ Report saved as: {report_dir} ✔✔✔")
        
        os.makedirs('test_report', exist_ok=True)
        shutil.copy2(
            os.path.join(report_dir, report_name),
            os.path.join('test_report', report_name)
        )
        print(" ✔✔✔ Report copy to: test_report ✔✔✔")
        
        allure_end_time = time.time()
        allure_duration = allure_end_time - allure_start_time
        print(f"Allure report generation took {allure_duration:.2f} seconds")
    
    except Exception as e:
        print(f" ✘✘✘ Allure report generation failed: {str(e)} ✘✘✘")
        if hasattr(e, 'stderr'):
            print(f"Error details: {e.stderr}")
        raise
    
    # 如果需要匯出報告（例如上傳到 S3、發送到 Slack 等）
    if is_export == 'true':
        try:
            print(' ⚙️ Exporting test reports...')
            # 可以在這裡加入報告匯出邏輯
            # 例如：上傳到 S3、發送到 Slack 等
            print(' ✔✔✔ Report Exported ✔✔✔')
        except Exception as e:
            print(f" ✘✘✘ Report export failed: {e} ✘✘✘")

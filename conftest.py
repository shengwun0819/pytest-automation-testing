"""
pytest 配置和 fixtures
定義測試的共用設定和前置/後置處理
"""
import os
import shutil
import subprocess
import time
from datetime import datetime

import config as app_config
import pytest

# 全域變數（使用 app_config 避免與 pytest hook 參數 config 混淆）
env = app_config.ENV
version = app_config.VERSION


def pytest_addoption(parser):
    """
    新增 pytest 命令列選項
    """
    parser.addoption(
        '--tags',
        action='store',
        default=None,
        help='指定要執行的測試標籤（以逗號分隔）'
    )
    parser.addoption(
        '--tag',
        action='store',
        default=None,
        dest='tag',
        help='同 --tags，單一標籤（例如 --tag=regression）'
    )
    parser.addoption(
        '--export',
        action='store',
        default=None,
        help='是否匯出報告（true/false）'
    )
    parser.addoption(
        "--allure-results-dir",
        action="store",
        default="allure-results",
        help="Allure 結果目錄"
    )


def pytest_configure(config):
    """
    pytest 配置初始化（參數名須為 config 以符合 pytest hookspec）
    """
    global target_tags
    target_tags = config.getoption('--tags', default=None) or config.getoption('--tag', default=None)
    if target_tags:
        target_tags = target_tags.lower().split(',')


@pytest.fixture(scope="session", autouse=True)
def pre_test(request):
    """
    測試前的準備工作（session scope）
    """
    # 清理之前的 Allure 結果
    subprocess.run('rm -rf ./allure-results/*', shell=True)
    
    # 可以在這裡加入其他前置準備工作
    # 例如：初始化測試資料、設定環境等


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
    # 可以在這裡加入清理工作
    # 例如：清理測試資料、重置環境等


def pytest_terminal_summary(terminalreporter, config, exitstatus):
    """
    測試終端摘要
    生成 Allure 報告（參數名須為 config 以符合 pytest hookspec）
    """
    time.sleep(2)
    
    is_export = config.getoption('--export', default=None)
    allure_results_dir = config.getoption("--allure-results-dir")
    
    time_now = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
    result = 'success' if exitstatus == 0 else 'failed'
    commit_sha = getattr(app_config, 'COMMIT_SHA', None) or 'local'
    report_dir = f"test_report/report_{commit_sha}_{result}_{time_now}"
    report_name = f'report_{commit_sha}_{result}_{time_now}.html'
    
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

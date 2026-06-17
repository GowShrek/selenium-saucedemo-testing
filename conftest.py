"""
conftest.py
-----------
File đặc biệt của pytest: mọi fixture và hook khai báo ở đây sẽ tự động
áp dụng cho TẤT CẢ file test trong cùng thư mục, không cần import.

Gồm 2 phần:
  1. fixture `driver`  -> khởi tạo/đóng trình duyệt Chrome cho mỗi test
  2. hook `pytest_runtest_makereport` -> tự động chụp ảnh màn hình
     mỗi khi một test case FAIL, lưu vào thư mục screenshots/
"""

import os
import pytest
from selenium import webdriver

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


@pytest.fixture
def driver():
    """
    Khởi tạo Chrome WebDriver trước mỗi test case (setup) và
    tự động đóng lại sau khi test case kết thúc (teardown).
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    # Biến môi trường HEADLESS=1 cho phép chạy ẩn (không hiện cửa sổ),
    # rất hữu ích khi chạy trên CI/CD (GitHub Actions) vì server không
    # có màn hình hiển thị.
    if os.environ.get("HEADLESS", "1") == "1":
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    # Các cờ dưới đây BẮT BUỘC khi chạy Chrome trong container/CI
    # (GitHub Actions runner cũng là một dạng container), vì Chrome
    # mặc định cần sandbox và shared-memory mà các môi trường này
    # thường giới hạn hoặc không hỗ trợ đầy đủ -> thiếu cờ này gây
    # crash ngay khi khởi tạo (SessionNotCreatedException).
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    # Trên CI (GitHub Actions), action setup-chrome cài Chrome vào một
    # đường dẫn không cố định. Biến CHROME_BIN (nếu có) chỉ rõ đường dẫn
    # đó cho Selenium, tránh trường hợp Selenium tìm sai bản Chrome.
    chrome_bin = os.environ.get("CHROME_BIN")
    if chrome_bin:
        chrome_options.binary_location = chrome_bin

    # Từ Selenium 4.6+, không cần webdriver-manager nữa: Selenium Manager
    # (tích hợp sẵn trong thư viện selenium) sẽ tự động tải đúng phiên bản
    # ChromeDriver khớp với Chrome đã cài trên máy/server, không phụ thuộc
    # domain tải driver bên thứ ba -> ổn định hơn khi chạy trên CI.
    drv = webdriver.Chrome(options=chrome_options)
    drv.implicitly_wait(3)

    yield drv

    drv.quit()


def screenshot(driver, name):
    """
    Lưu ảnh chụp màn hình hiện tại của trình duyệt với tên file cho trước.
    Dùng để thu thập minh chứng (proof of execution) tại các bước quan
    trọng của test case (khác với hook bên dưới, chỉ chụp khi test FAIL).
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, name)
    driver.save_screenshot(path)
    print(f"\n📸 [SCREENSHOT] Đã lưu minh chứng tại: screenshots/{name}")
    return path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook đặc biệt của pytest: tự động chạy sau mỗi bước test.
    Nếu bước "call" (chạy nội dung test) bị FAIL, ta tự động chụp
    ảnh màn hình hiện tại của trình duyệt và lưu lại - giúp việc
    debug dễ dàng hơn nhiều so với chỉ đọc traceback chữ.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            screenshot_path = os.path.join(
                SCREENSHOT_DIR, f"{item.name}.png"
            )
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\n📸 Đã lưu ảnh lỗi tại: {screenshot_path}")
            except Exception as e:
                print(f"\n⚠️ Không thể chụp ảnh lỗi: {e}")

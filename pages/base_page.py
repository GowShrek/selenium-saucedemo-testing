"""
base_page.py
------------
Lớp cha (BasePage) chứa các hành động chung mà mọi "page object" khác
đều cần dùng: chờ phần tử, click, nhập text, lấy text...

Đây là kỹ thuật kế thừa (inheritance) trong OOP - giúp không phải viết
lại logic "chờ rồi mới click" ở từng page riêng lẻ.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10


class BasePage:
    """Lớp cơ sở cho mọi Page Object trong project."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, url):
        """Mở một URL bất kỳ."""
        self.driver.get(url)

    def find(self, locator):
        """Chờ tới khi phần tử xuất hiện trong DOM, rồi trả về phần tử đó."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """Trả về danh sách tất cả phần tử khớp locator (không chờ riêng)."""
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """Chờ tới khi phần tử có thể click được, rồi click."""
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

    def type_text(self, locator, text):
        """Chờ phần tử xuất hiện, xoá nội dung cũ rồi nhập text mới."""
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        """Lấy nội dung text hiển thị của một phần tử."""
        return self.find(locator).text

    def is_visible(self, locator):
        """Kiểm tra phần tử có đang hiển thị trên trang không."""
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def wait_for_url_contains(self, fragment):
        """Chờ tới khi URL hiện tại chứa một đoạn chuỗi cho trước."""
        return self.wait.until(EC.url_contains(fragment))

    def current_url(self):
        return self.driver.current_url

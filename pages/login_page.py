"""
login_page.py
--------------
Page Object đại diện cho trang đăng nhập của saucedemo.com
(https://www.saucedemo.com/)

Mọi locator (cách định vị phần tử) và hành động liên quan tới trang
đăng nhập đều được gói gọn trong class này. Nếu sau này website đổi
giao diện, ta chỉ cần sửa ở ĐÚNG MỘT NƠI này, không cần sửa rải rác
trong các file test.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

BASE_URL = "https://www.saucedemo.com"


class LoginPage(BasePage):
    # ---- Locators: nơi định vị các phần tử trên trang ----
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open_login_page(self):
        """Mở trang chủ (chính là trang đăng nhập của saucedemo)."""
        self.open(BASE_URL + "/")
        return self

    def login(self, username, password):
        """Thực hiện hành động đăng nhập với username/password cho trước."""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self):
        """Lấy nội dung thông báo lỗi khi đăng nhập thất bại."""
        return self.get_text(self.ERROR_MESSAGE)

"""
cart_page.py
------------
Page Object đại diện cho trang giỏ hàng (Cart page), URL chứa "cart.html".
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    # ---- Locators ----
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def get_item_names(self):
        """Trả về danh sách tên tất cả sản phẩm đang có trong giỏ hàng."""
        elements = self.find_all(self.ITEM_NAMES)
        return [el.text for el in elements]

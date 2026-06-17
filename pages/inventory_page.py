"""
inventory_page.py
------------------
Page Object đại diện cho trang danh sách sản phẩm (Products page)
- xuất hiện ngay sau khi đăng nhập thành công, URL chứa "inventory.html".
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    # ---- Locators ----
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_page_title(self):
        """Lấy tiêu đề trang (mong đợi là 'Products')."""
        return self.get_text(self.PAGE_TITLE)

    def add_product_to_cart(self, product_id_slug):
        """
        Thêm một sản phẩm vào giỏ hàng.
        saucedemo.com đặt id nút "Add to cart" theo định dạng:
            add-to-cart-<ten-san-pham-dang-slug>
        Ví dụ: "Sauce Labs Backpack" -> id="add-to-cart-sauce-labs-backpack"
        """
        locator = (By.ID, f"add-to-cart-{product_id_slug}")
        self.click(locator)
        return self

    def get_cart_count(self):
        """Lấy số lượng sản phẩm hiển thị trên icon giỏ hàng."""
        if self.is_visible(self.CART_BADGE):
            return self.get_text(self.CART_BADGE)
        return "0"

    def go_to_cart(self):
        """Click vào icon giỏ hàng để chuyển sang trang Cart."""
        self.click(self.CART_LINK)
        return self

    def logout(self):
        """Mở menu hamburger và nhấn Logout."""
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return self

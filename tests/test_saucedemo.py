"""
========================================================================
BÀI THỰC HÀNH SELENIUM - KIỂM THỬ TỰ ĐỘNG WEBSITE SAUCEDEMO.COM
Viết theo mô hình Page Object Model (POM)
========================================================================

Website kiểm thử : https://www.saucedemo.com
Tài khoản hợp lệ : standard_user / secret_sauce
Tài khoản bị khoá: locked_out_user / secret_sauce

Cấu trúc project:
    pages/
        base_page.py        -> các hành động chung (click, type, wait...)
        login_page.py        -> Page Object cho trang đăng nhập
        inventory_page.py    -> Page Object cho trang sản phẩm
        cart_page.py          -> Page Object cho trang giỏ hàng
    tests/
        test_saucedemo.py    -> file này, chứa các test case
    conftest.py               -> fixture khởi tạo driver + tự chụp ảnh khi fail

3 Test case bắt buộc:
    1. test_01_login_thanh_cong       -> Đăng nhập thành công
    2. test_02_them_san_pham_vao_gio  -> Thêm sản phẩm vào giỏ hàng
    3. test_03_dang_xuat              -> Đăng xuất

Test case bổ sung (negative test):
    4. test_04_login_voi_tai_khoan_bi_khoa -> Đăng nhập với tài khoản bị khoá

Cách chạy:
    pytest tests/test_saucedemo.py -v -s
========================================================================
"""

import pytest
from conftest import screenshot
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USERNAME = "locked_out_user"


# ------------------------------------------------------------------
# TEST CASE 1: ĐĂNG NHẬP THÀNH CÔNG
# ------------------------------------------------------------------
def test_01_login_thanh_cong(driver):
    """
    Mục tiêu: Kiểm tra người dùng đăng nhập thành công với tài khoản hợp lệ.

    Bước thực hiện:
        1. Mở trang đăng nhập saucedemo.com
        2. Nhập username/password hợp lệ và nhấn Login

    Kết quả mong đợi:
        - URL chuyển sang trang chứa "inventory.html"
        - Tiêu đề trang hiển thị đúng chữ "Products"
    """
    login_page = LoginPage(driver)
    login_page.open_login_page()
    screenshot(driver, "01_login_page.png")

    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_url_contains("inventory.html")

    assert "inventory.html" in inventory_page.current_url(), (
        f"Đăng nhập thất bại, URL hiện tại: {inventory_page.current_url()}"
    )
    assert inventory_page.get_page_title() == "Products", (
        "Tiêu đề trang sau khi đăng nhập không đúng."
    )
    screenshot(driver, "02_login_success.png")


# ------------------------------------------------------------------
# TEST CASE 2: THÊM SẢN PHẨM VÀO GIỎ HÀNG
# ------------------------------------------------------------------
def test_02_them_san_pham_vao_gio(driver):
    """
    Mục tiêu: Kiểm tra thêm sản phẩm vào giỏ hàng hoạt động đúng.

    Bước thực hiện:
        1. Đăng nhập vào hệ thống
        2. Thêm "Sauce Labs Backpack" và "Sauce Labs Bike Light" vào giỏ

    Kết quả mong đợi:
        - Icon giỏ hàng hiển thị số lượng = 2
        - Trang giỏ hàng hiển thị đúng 2 sản phẩm đã chọn
    """
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_url_contains("inventory.html")

    inventory_page.add_product_to_cart("sauce-labs-backpack")
    inventory_page.add_product_to_cart("sauce-labs-bike-light")

    assert inventory_page.get_cart_count() == "2", (
        f"Số lượng giỏ hàng không đúng, nhận được: {inventory_page.get_cart_count()}"
    )
    screenshot(driver, "03_added_to_cart.png")

    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    cart_page.wait_for_url_contains("cart.html")

    items_in_cart = cart_page.get_item_names()
    assert "Sauce Labs Backpack" in items_in_cart
    assert "Sauce Labs Bike Light" in items_in_cart
    assert len(items_in_cart) == 2, f"Giỏ hàng có sai số sản phẩm: {items_in_cart}"
    screenshot(driver, "04_cart_page.png")


# ------------------------------------------------------------------
# TEST CASE 3: ĐĂNG XUẤT
# ------------------------------------------------------------------
def test_03_dang_xuat(driver):
    """
    Mục tiêu: Kiểm tra đăng xuất hoạt động đúng qua menu hamburger.

    Bước thực hiện:
        1. Đăng nhập vào hệ thống
        2. Mở menu hamburger, nhấn Logout

    Kết quả mong đợi:
        - Quay lại đúng trang đăng nhập (URL gốc)
        - Form đăng nhập hiển thị lại
    """
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_url_contains("inventory.html")
    inventory_page.logout()

    # Sau khi logout, trang đăng nhập phải hiển thị lại
    login_page.wait_for_url_contains("saucedemo.com")
    assert login_page.is_visible(LoginPage.LOGIN_BUTTON), (
        "Form đăng nhập không hiển thị lại sau khi đăng xuất."
    )
    assert "inventory.html" not in login_page.current_url(), (
        "Vẫn còn ở trang sản phẩm, đăng xuất thất bại."
    )
    screenshot(driver, "05_logout_success.png")


# ------------------------------------------------------------------
# TEST CASE 4 (BONUS - negative test): ĐĂNG NHẬP VỚI TÀI KHOẢN BỊ KHOÁ
# ------------------------------------------------------------------
def test_04_login_voi_tai_khoan_bi_khoa(driver):
    """
    Mục tiêu: Kiểm tra hệ thống từ chối đăng nhập đúng cách với tài khoản
    đã bị khoá (locked_out_user), và hiển thị thông báo lỗi phù hợp.
    Đây là ví dụ về "negative testing" - kiểm thử trường hợp lỗi/ngoại lệ,
    không chỉ test trường hợp thành công (happy path).
    """
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(LOCKED_USERNAME, VALID_PASSWORD)

    error_text = login_page.get_error_message()
    screenshot(driver, "06_locked_user_error.png")
    assert "locked out" in error_text.lower(), (
        f"Thông báo lỗi không như mong đợi: {error_text}"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

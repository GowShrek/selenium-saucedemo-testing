# Kiểm thử tự động website SauceDemo bằng Selenium (Python)

[![Selenium Automated Tests](https://github.com/GowShrek/selenium-saucedemo-testing/actions/workflows/selenium-tests.yml/badge.svg)](https://github.com/GowShrek/selenium-saucedemo-testing/actions/workflows/selenium-tests.yml)

## 1. Mục tiêu bài tập

Xây dựng tối thiểu 3 test case kiểm thử tự động (automation test) cho một
website, sử dụng Selenium WebDriver. Website được chọn:
**https://www.saucedemo.com** — một website thương mại điện tử giả lập,
được Sauce Labs tạo ra dành riêng cho việc luyện tập automation testing.

## 2. Công nghệ sử dụng

| Thành phần | Vai trò |
|---|---|
| Python 3.11+ | Ngôn ngữ viết test |
| Selenium WebDriver 4.20+ | Điều khiển trình duyệt Chrome tự động (dùng Selenium Manager tích hợp để tự tải đúng ChromeDriver) |
| pytest | Framework chạy test, báo cáo PASS/FAIL |
| GitHub Actions | Tự động chạy test mỗi khi push code (CI/CD) |

## 3. Kiến trúc project — Page Object Model (POM)

Project được tổ chức theo mô hình **Page Object Model**, một thực hành phổ
biến trong automation testing thực tế. Ý tưởng: mỗi trang web tương ứng với
một class Python riêng, chứa toàn bộ locator (cách định vị phần tử) và hành
động (click, nhập text...) của trang đó. File test chỉ gọi các hành động ở
mức cao (`login()`, `add_product_to_cart()`...), không chứa locator trực tiếp.

**Lợi ích**: khi website thay đổi giao diện (ví dụ đổi id của nút bấm), ta
chỉ cần sửa đúng 1 chỗ trong file `pages/`, không phải sửa rải rác trong
nhiều file test.

```
selenium-saucedemo-testing/
│
├── pages/                      # Page Object — đại diện cho từng trang web
│   ├── base_page.py            # Hành động chung: click, nhập text, chờ...
│   ├── login_page.py           # Trang đăng nhập
│   ├── inventory_page.py       # Trang danh sách sản phẩm
│   └── cart_page.py            # Trang giỏ hàng
│
├── tests/
│   └── test_saucedemo.py       # Các test case (nội dung kiểm thử chính)
│
├── conftest.py                 # Fixture khởi tạo trình duyệt + tự chụp
│                                #   ảnh màn hình khi test fail
├── .github/workflows/
│   └── selenium-tests.yml      # CI: tự động chạy test trên GitHub
├── requirements.txt            # Danh sách thư viện cần cài
├── .gitignore
└── README.md
```

## 4. Danh sách test case

| # | Tên hàm test | Loại | Mục tiêu |
|---|---|---|---|
| 1 | `test_01_login_thanh_cong` | Positive | Đăng nhập với tài khoản hợp lệ, xác minh chuyển đúng trang Products |
| 2 | `test_02_them_san_pham_vao_gio` | Positive | Thêm 2 sản phẩm vào giỏ, xác minh số lượng và tên sản phẩm hiển thị đúng |
| 3 | `test_03_dang_xuat` | Positive | Đăng xuất qua menu, xác minh quay về đúng trang đăng nhập |
| 4 | `test_04_login_voi_tai_khoan_bi_khoa` | Negative | Đăng nhập bằng tài khoản bị khoá, xác minh thông báo lỗi hiển thị đúng |

Test case #4 là ví dụ về **negative testing** — kiểm thử trường hợp lỗi/ngoại
lệ, không chỉ kiểm thử "đường happy path" (mọi thứ đều đúng).

## 5. Cách chạy test trên máy cá nhân

### Bước 1: Cài Python và Google Chrome
Đảm bảo máy đã có Python 3.10+ và Google Chrome.

### Bước 2: Cài thư viện
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy toàn bộ test
```bash
pytest tests/test_saucedemo.py -v -s
```

Mặc định test chạy ở chế độ **headless** (ẩn, không hiện cửa sổ Chrome) vì
biến môi trường `HEADLESS` mặc định là `"1"` trong `conftest.py`. Để xem
trình duyệt chạy trực quan (hiện cửa sổ), set biến môi trường trước khi chạy:

```bash
# Windows (PowerShell)
$env:HEADLESS="0"; pytest tests/test_saucedemo.py -v -s

# macOS / Linux
HEADLESS=0 pytest tests/test_saucedemo.py -v -s
```

### Khi test fail
Ảnh chụp màn hình tại đúng thời điểm fail sẽ tự động lưu vào thư mục
`screenshots/`, giúp xác định lỗi nhanh hơn nhiều so với chỉ đọc log chữ.

## 6. CI/CD — Tự động chạy test trên GitHub Actions

Mỗi khi có commit mới được push lên branch `main`, GitHub sẽ **tự động**:
1. Cài Python + Google Chrome trên máy chủ của GitHub
2. Cài các thư viện trong `requirements.txt`
3. Chạy toàn bộ test trong `tests/test_saucedemo.py`
4. Hiển thị kết quả PASS/FAIL ngay trên tab **Actions** của repository
5. Nếu có test fail, tự động đính kèm ảnh chụp màn hình lỗi để xem lại

Đây là cách xác minh đáng tin cậy nhất rằng bộ test thực sự hoạt động đúng,
vì nó chạy trên môi trường độc lập, không phụ thuộc vào máy cá nhân của ai.

**Đã xác nhận chạy thật và pass**: cả 4 test case (3 bắt buộc + 1 negative
test bổ sung) đã chạy thành công trên GitHub Actions với Chrome thật ở chế
độ headless. Xem badge trạng thái ở đầu file này, hoặc vào tab **Actions**
của repository để xem lịch sử các lần chạy.

Một lưu ý kỹ thuật quan trọng khi chạy Chrome trong môi trường container/CI:
cần các cờ `--no-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu` (đã
được thiết lập sẵn trong `conftest.py`), vì Chrome mặc định yêu cầu sandbox
và vùng nhớ chia sẻ (shared memory) mà môi trường container thường giới hạn
— thiếu các cờ này sẽ khiến Chrome crash ngay khi khởi tạo.

## 7. Giải thích các kỹ thuật Selenium quan trọng được áp dụng

- **Explicit Wait** (`WebDriverWait` + `expected_conditions`): chờ một điều
  kiện cụ thể (phần tử xuất hiện, có thể click, URL thay đổi...) trong tối
  đa N giây, thay vì dùng `time.sleep()` cố định. Giúp test chạy nhanh khi
  trang load nhanh, vẫn ổn định khi trang load chậm.

- **Page Object Model**: tách locator/hành động ra khỏi logic test, như đã
  giải thích ở mục 3.

- **Fixture của pytest** (`conftest.py`): tự động mở trình duyệt mới trước
  mỗi test case và đóng lại sau khi xong, đảm bảo các test độc lập với nhau,
  không bị ảnh hưởng lẫn nhau.

- **Hook `pytest_runtest_makereport`**: tự động chụp ảnh màn hình ngay khi
  một test case fail, hỗ trợ debug nhanh.

- **Headless mode**: chạy trình duyệt ở chế độ ẩn, cần thiết khi chạy trên
  máy chủ CI không có màn hình hiển thị.

## 8. Hướng phát triển tiếp theo

- Thêm test case cho chức năng sắp xếp sản phẩm (Name A-Z, Price low-high...).
- Thêm test case xoá sản phẩm khỏi giỏ hàng, hoặc luồng thanh toán (checkout).
- Tham số hoá (parametrize) test đăng nhập để chạy với nhiều bộ tài khoản
  khác nhau (`@pytest.mark.parametrize`).
- Thêm báo cáo HTML đẹp bằng `pytest-html`.

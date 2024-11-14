# Sử dụng Random Forest để dự đoán giá thuê phòng trọ và lưu trữ dữ liệu với MongoDB

## 1. Giới thiệu

Trong dự án này, chúng tôi sử dụng mô hình **Random Forest Regressor** để dự đoán giá thuê phòng trọ dựa trên các đặc trưng đã cho. Dữ liệu được lưu trữ và truy xuất từ cơ sở dữ liệu **MongoDB**. Quá trình bao gồm kết nối đến MongoDB, lấy dữ liệu, huấn luyện mô hình và đánh giá hiệu suất của mô hình.

## 2. Mã nguồn chi tiết

### 2.1. Import các thư viện cần thiết

```python
import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
```

-   **pandas**: Thư viện xử lý dữ liệu bảng.
-   **pymongo**: Thư viện kết nối và thao tác với MongoDB.
-   **sklearn**: Thư viện cho các thuật toán học máy và đánh giá mô hình.

### 2.2. Kết nối đến cơ sở dữ liệu MongoDB

```python
# Kết nối MongoDB
uri = 'mongodb+srv://GROUP_1:12345@cluster0.cjavi.mongodb.net/'
client = MongoClient(uri)
db = client['DB_G1']
collection = db['RentalRoom']
```

-   **uri**: Chuỗi kết nối đến MongoDB Atlas Cluster.
-   **client**: Tạo một MongoClient để kết nối đến MongoDB.
-   **db**: Chọn cơ sở dữ liệu `DB_G1`.
-   **collection**: Chọn bộ sưu tập `RentalRoom` trong cơ sở dữ liệu.

**Lưu ý:** Thông tin đăng nhập như username và password trong URI nên được bảo mật và không nên đưa trực tiếp vào mã nguồn. Nên sử dụng biến môi trường hoặc tệp cấu hình để lưu trữ thông tin này.

### 2.3. Lấy dữ liệu từ MongoDB và chuẩn bị dữ liệu

```python
# Lấy dữ liệu từ MongoDB và chuyển thành DataFrame
data = list(collection.find())
df = pd.DataFrame(data)

# Xóa cột _id do không cần dùng trong quá trình huấn luyện
df = df.drop(columns=['_id'])
```

-   **collection.find()**: Lấy toàn bộ dữ liệu từ bộ sưu tập `RentalRoom`.
-   **pd.DataFrame(data)**: Chuyển dữ liệu thành DataFrame để dễ dàng xử lý.
-   **df.drop(columns=['_id'])**: Loại bỏ cột `_id` được tự động thêm bởi MongoDB.

### 2.4. Tách dữ liệu thành biến đầu vào và biến mục tiêu

```python
# Tách dữ liệu thành X và y
X = df.drop(columns=['Price'])  # Giả sử cột mục tiêu là 'Price'
y = df['Price']
```

-   **X**: Chứa các đặc trưng dùng để dự đoán.
-   **y**: Biến mục tiêu, ở đây là cột `Price` biểu thị giá thuê phòng.

### 2.5. Chia dữ liệu thành tập huấn luyện và tập kiểm tra

```python
# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
```

-   **train_test_split**: Hàm chia dữ liệu với tỷ lệ 75% dữ liệu cho tập huấn luyện và 25% cho tập kiểm tra.
-   **random_state=42**: Đảm bảo tính tái lặp của kết quả.

### 2.6. Huấn luyện mô hình Random Forest

```python
# Huấn luyện mô hình Random Forest
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)
```

-   **RandomForestRegressor**: Khởi tạo mô hình Random Forest cho bài toán hồi quy.
-   **model.fit**: Huấn luyện mô hình trên tập huấn luyện.

### 2.7. Đánh giá mô hình trên tập huấn luyện

```python
print("======TRAIN======")
y_pre_train = model.predict(X_train)
score_train = mean_absolute_error(y_train, y_pre_train).round(5)
mse_score_train = mean_squared_error(y_train, y_pre_train).round(5)
rmse_train = mean_squared_error(y_train, y_pre_train, squared=False).round(5)
score_r2_train = round(r2_score(y_train, y_pre_train), 5)
print("Train error (MAE): {}".format(score_train))
print("Train error (MSE): {}".format(mse_score_train))
print("Train error (RMSE): {}".format(rmse_train))
print("R2 score : {}".format(score_r2_train))
```

-   **mean_absolute_error**: Tính MAE trên tập huấn luyện.
-   **mean_squared_error**: Tính MSE và RMSE trên tập huấn luyện.
-   **r2_score**: Tính hệ số xác định R² trên tập huấn luyện.

### 2.8. Đánh giá mô hình trên tập kiểm tra

```python
print("======TEST======")
y_pre_test = model.predict(X_test)
score_test = mean_absolute_error(y_test, y_pre_test).round(5)
mse_score_test = mean_squared_error(y_test, y_pre_test).round(5)
rmse_test = mean_squared_error(y_test, y_pre_test, squared=False).round(5)
score_r2_test = round(r2_score(y_test, y_pre_test), 5)
print("Test error (MAE): {}".format(score_test))
print("Test error (MSE): {}".format(mse_score_test))
print("Test error (RMSE): {}".format(rmse_test))
print("R2 score : {}".format(score_r2_test))
```

-   Tương tự như trên, nhưng đánh giá trên tập kiểm tra để xem mô hình hoạt động với dữ liệu mới như thế nào.

## 3. Kết quả thu được

Sau khi chạy mã nguồn trên, chúng tôi thu được kết quả như sau:

```
======TRAIN======
Train error (MAE): 0.13139
Train error (MSE): 0.04735
Train error (RMSE): 0.21761
R2 score : 0.97532
======TEST======
Test error (MAE): 0.35043
Test error (MSE): 0.32323
Test error (RMSE): 0.56854
R2 score : 0.83523
```

## 4. Phân tích kết quả

### 4.1. Kết quả trên tập huấn luyện

-   **Mean Absolute Error (MAE):** 0.13139
-   **Mean Squared Error (MSE):** 0.04735
-   **Root Mean Squared Error (RMSE):** 0.21761
-   **R² Score:** 0.97532

**Nhận xét:**

-   Mô hình dự đoán với sai số trung bình khoảng **0.13139** đơn vị trên tập huấn luyện.
-   **R² Score** cao (**97.532%**), cho thấy mô hình giải thích được phần lớn biến thiên của dữ liệu trên tập huấn luyện.

### 4.2. Kết quả trên tập kiểm tra

-   **Mean Absolute Error (MAE):** 0.35043
-   **Mean Squared Error (MSE):** 0.32323
-   **Root Mean Squared Error (RMSE):** 0.56854
-   **R² Score:** 0.83523

**Nhận xét:**

-   Sai số trung bình tăng lên khoảng **0.35043** đơn vị trên tập kiểm tra.
-   **R² Score** giảm xuống **83.523%**, nhưng vẫn cho thấy mô hình có khả năng dự đoán tốt trên dữ liệu mới.

### 4.3. Đánh giá tổng thể

-   **Hiện tượng overfitting:** Có dấu hiệu của overfitting khi mô hình hoạt động tốt trên tập huấn luyện nhưng kém hơn trên tập kiểm tra.
-   **Hiệu suất mô hình:** Mặc dù có sự giảm sút, mô hình vẫn đạt hiệu suất tốt trên tập kiểm tra, cho thấy khả năng tổng quát hóa.

## 5. Kết luận và đề xuất

### 5.1. Kết luận

Mô hình **Random Forest Regressor** đã được sử dụng để dự đoán giá thuê phòng trọ và cho kết quả khả quan. Mô hình có khả năng giải thích phần lớn biến thiên của dữ liệu và dự đoán với độ chính xác chấp nhận được trên tập kiểm tra.

Việc lưu trữ dữ liệu trên **MongoDB** giúp quá trình truy xuất và quản lý dữ liệu trở nên thuận tiện hơn, đặc biệt khi làm việc với dữ liệu lớn. Mô hình Random Forest đã chứng minh hiệu quả trong việc dự đoán giá thuê phòng trọ, tuy nhiên vẫn cần tiếp tục cải thiện để đạt kết quả tốt hơn trong thực tế.

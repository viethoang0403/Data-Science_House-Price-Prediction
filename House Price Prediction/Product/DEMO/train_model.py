import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib  # Thêm thư viện joblib để lưu mô hình

# Kết nối MongoDB
uri = 'mongodb+srv://GROUP_1:12345@cluster0.cjavi.mongodb.net/'
client = MongoClient(uri)
db = client['DB_G1']
collection = db['RentalRoom']

# Lấy dữ liệu từ MongoDB và chuyển thành DataFrame
data = list(collection.find())
df = pd.DataFrame(data)

# Xóa cột _id do không cần dùng trong quá trình huấn luyện
df = df.drop(columns=['_id'])
df = df.drop(columns=['Unnamed: 0'])
df = df.drop(columns=['District_Củ Chi'])
df = df.drop(columns=['District_Quận 4'])
df = df.drop(columns=['Date'])

# Tách dữ liệu thành X và y
X = df.drop(columns=['Price'])  # Giả sử cột mục tiêu là 'Price'
y = df['Price']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Huấn luyện mô hình Random Forest
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Đánh giá mô hình (như trước đây)
print("======TRAIN======")
y_pre_train = model.predict(X_train)
score_train = mean_absolute_error(y_train, y_pre_train).round(5)
mse_score = mean_squared_error(y_train, y_pre_train).round(5)
rmse = mean_squared_error(y_train, y_pre_train, squared=False).round(5)
score_r2 = round(r2_score(y_train, y_pre_train), 5)
print("Train error (MAE): {}".format(score_train))
print("Train error (MSE): {}".format(mse_score))
print("Train error (RMSE): {}".format(rmse))
print("R2 score : {}".format(score_r2))

print("======TEST======")
y_pre_test = model.predict(X_test)
score_test = mean_absolute_error(y_test, y_pre_test).round(5)
mse_score = mean_squared_error(y_test, y_pre_test).round(5)
rmse = mean_squared_error(y_test, y_pre_test, squared=False).round(5)
score_r2 = round(r2_score(y_test, y_pre_test), 5)
print("Test error (MAE): {}".format(score_test))
print("Test error (MSE): {}".format(mse_score))
print("Test error (RMSE): {}".format(rmse))
print("R2 score : {}".format(score_r2))

# Lưu mô hình đã huấn luyện vào file
joblib.dump(model, 'lr_model.sav')
print("Mô hình đã được lưu vào file lr_model.sav")
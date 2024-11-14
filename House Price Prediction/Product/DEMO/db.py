import pandas as pd
from pymongo import MongoClient

# Sử dụng URI đã cung cấp
uri = 'mongodb+srv://GROUP_1:12345@cluster0.cjavi.mongodb.net/'

# Tạo client MongoDB
client = MongoClient(uri)

# Chọn cơ sở dữ liệu và bộ sưu tập
db = client['DB_G1']
collection = db['RentalRoom']

# Đọc dữ liệu từ file CSV
df = pd.read_csv('clean_data_new.csv')

# Chuyển DataFrame thành danh sách các từ điển
data = df.to_dict(orient='records')

# Chèn dữ liệu vào bộ sưu tập
result = collection.insert_many(data)

# In ID của các tài liệu đã chèn
print('Inserted document IDs:', result.inserted_ids)
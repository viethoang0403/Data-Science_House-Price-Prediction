import streamlit as st 
import pandas as pd 
import numpy as np 
import joblib
import os 
def predict(data):
    path = os.path.dirname(__file__)
    lr = joblib.load(path + '/lr_model.sav') 
    return lr.predict(data) 


st.title("Dự đoán giá thuê phòng trọ sinh viên ở thành phố Hồ Chí Minh")

st.write('---')
st.header("Nhập các tham số sau")

district = st.selectbox("**Vị trí**", ('Bình Chánh', 'Bình Thạnh', 'Bình Tân', 
'Gò Vấp', 'Hóc Môn', 'Nhà Bè', 'Phú Nhuận', 'Quận 1', 'Quận 10', 'Quận  11', 'Quận 12', 
'Quận 2', 'Quận 3', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Thủ Đức', 
'Tân Bình', 'Tân Phú'))

area = st.slider('**Diện tích (m2)**', 5, 80)

isNew = st.radio('**Tình trạng phòng mới hay cũ**', ("Mới", "Cũ"))
if isNew == "Mới":
    isNew = [0, 1]
else: 
    isNew = [1, 0]

isNearCenter = st.radio('**Có gần trung tâm không**', ("Có", "Không"))
if isNearCenter == "Có":
    isNearCenter = [0, 1]
else: 
    isNearCenter = [1, 0]

hasFurniture = st.radio("**Phòng có nội thất hay không?**", ("Có", "Không")) 
if hasFurniture == "Có":
    hasFurniture = [0, 1]
else: 
    hasFurniture = [1, 0]

isWholeHouse = st.radio("**Có phải phòng nguyên căn không?**", ("Có", "Không")) 
if isWholeHouse == "Có":
    isWholeHouse = [0, 1]
else: 
    isWholeHouse = [1, 0]

liveTogether = st.radio("**Có ở ghép không?**", ("Có", "Không"))
if liveTogether == "Có":
    liveTogether = [0,1] 
else:
    liveTogether = [1,0]


isApartment = st.radio("**Có phải chung cư không?**", ("Có", "Không"))
if isApartment == "Có":
    isApartment = [0,1] 
else:
    isApartment = [1,0]

listOfCity = ['Bình Chánh', 'Bình Thạnh', 'Bình Tân', 'Gò Vấp', 'Hóc Môn', 'Nhà Bè', 'Phú Nhuận', 
'Quận 1', 'Quận 10', 'Quận 11', 'Quận 12', 'Quận 2', 
'Quận 3', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Thủ Đức', 'Tân Bình', 'Tân Phú']
listOfCity.sort()
pos = np.zeros(len(listOfCity))
pos[listOfCity.index(district)] = 1 
X = np.concatenate([pos, isNew, isNearCenter, hasFurniture, isWholeHouse, liveTogether, isApartment, [area]])
if st.button('**Predict House Price**'): 
    # X = np.array([[area, district, isNew, hasFurniture, liveTogether]])
    print(X)
    if X[-1] < 5:
        st.text("Diện tích phòng trọ phải lớn hơn 5m2.")
    else:        
        cost = predict([X])
        if cost[0] < 0:
            st.text("Không thể dự đoán. Xem lại các thông số đã chọn.")
        else:
            st.text("Tiền thuê phòng trọ dự đoán là: {:,} VND / 1 tháng".format(np.round(cost[0], 6)*1000000))
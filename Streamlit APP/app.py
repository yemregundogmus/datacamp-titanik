import streamlit as st
import numpy as np
import pickle

# Model yükleniyor
filename = '../Notebooks/titanic_model.sav'
model = pickle.load(open(filename, 'rb'))

# Eğitim verisinde kullanılan mapping'ler
title_mapping = {"Bay": 1, "Hanım": 2, "Bayan": 3, "Usta": 4, "Doktor": 5, "Özgü": 6}
embarked_mapping = {"Southampton, İngiltere": 1, "Cherbourg, Fransa": 2, "Queesntown, İrlanda": 3}
sex_mapping = {"Erkek": 0, "Kadın": 1}
ports_range = ('Southampton, İngiltere', 'Cherbourg, Fransa', 'Queesntown, İrlanda')

def prediction(pclass, sex, age, sibsp, parch, embarked, title):
    new_array = np.array([pclass, sex_mapping[sex], age, sibsp, parch, embarked_mapping[embarked], title_mapping[title]])
    new_array = new_array.reshape(1, -1)
    result = model.predict(new_array)
    proba = model.predict_proba(new_array)
    if result == 0:
        return ("Hayatta Kalamazdınız", proba[0][0])
    else:
        return ("Hayatta Kalırdınız", proba[0][1])

st.title('Titanik Hayatta Kalma Tahmin Uygulaması')

# Kullanıcı girişleri
pclass = st.selectbox('Sınıfınız (1=Business, 2=Ekonomi, 3=Alt Sınıf)', [1, 2, 3])
sex = st.selectbox('Cinsiyetiniz', ['Erkek', 'Kadın'])
title = st.selectbox('Ünvanınız', ['Bay', 'Hanım', 'Bayan', 'Usta', 'Doktor', 'Özgü'])
age = st.slider('Yaşınız', 0, 90, 28)
sibsp = st.slider('Titanikteki kardeş/eş sayınız', 0, 8, 0)
parch = st.slider('Titanikteki ebeveyn/çocuk sayınız', 0, 6, 0)
embarked = st.selectbox('Gemiye hangi limandan bindiniz?', ports_range)

# Tahmin
result = prediction(pclass, sex, age, sibsp, parch, embarked, title)

# Sonuçları göster
if result[0] == 'Hayatta Kalırdınız':
    st.success(f"%{round(result[1]*100, 2)} ihtimalle {result[0]}")
else:
    st.error(f"%{round((1-result[1])*100, 2)} ihtimalle {result[0]}")

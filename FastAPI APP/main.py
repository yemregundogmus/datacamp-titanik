from models import Argument, ArgumentResponse
from fastapi import FastAPI, Request
import pickle
import numpy as np 

app = FastAPI(
    title="Titanic API",
    version="0.1",
    description="Kader belirleyen servis"
)

filename = 'titanic_model.sav'
model = pickle.load(open(filename, 'rb'))

title_mapping = {"Bay": 1, "Hanım": 2, "Bayan": 3, "Usta": 4, "Doktor": 5, "Özgü": 6}
embarked_mapping = {"Southampton, İngiltere": 1, "Cherbourg, Fransa": 2, "Queesntown, İrlanda": 3}
sex_mapping = {"Erkek": 0, "Kadın": 1}
ports_range = ('Southampton, İngiltere', 'Cherbourg, Fransa', 'Queesntown, İrlanda')

async def prediction(pclass, sex, age, sibsp, parch, embarked, title):
    new_array = np.array([pclass, sex_mapping[sex], age, sibsp, parch, embarked_mapping[embarked], title_mapping[title]]).reshape(1, -1)
    result = model.predict(new_array)
    proba = model.predict_proba(new_array)
    print(proba)
    if result == 0:
         return ("Not Survived", proba[0][0]*100)
    else:
        return ("Survived", proba[0][1]*100)


@app.post('/predict', summary="Titanik kazasına karışsaydın hayatta kalır mıydın?")
async def predict_survive(arg: Argument):
    """
    Bu Endpoint ile Alttaki verilen değerler sonucu titanikteki yolcunun hayatta kalma olasılığı tahmin edilecektir. 

    Pclass: Yolcunun sınıfı (1 = Birinci, 2 = İkinci, 3 = Üçüncü)

    Sex: Yolcunun cinsiyeti ('Erkek' veya 'Kadın')

    Title: Yolcunun unvanı ('Bay', 'Hanım', 'Bayan', 'Usta', 'Doktor', 'Özgü')

    Age: Yolcunun yaşı

    Sibsp: Titanik'te bulunan kardeş/eş sayısı

    Parch: Titanik'te bulunan ebeveyn/çocuk sayısı

    Embarked: Binilen liman ('Southampton, İngiltere', 'Cherbourg, Fransa', 'Queesntown, İrlanda')

    """
    results = await prediction(arg.pclass, arg.sex, arg.age, arg.sibsp, arg.parch, arg.embarked, arg.title)
    response = ArgumentResponse(survive=results[0], proba=results[1])
    return response
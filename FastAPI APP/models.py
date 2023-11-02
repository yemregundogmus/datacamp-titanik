from pydantic import BaseModel, Field

class Argument(BaseModel):
    pclass: int = Field(..., description="Yolcunun sınıfı (1 = Birinci, 2 = İkinci, 3 = Üçüncü)")
    sex: str = Field(..., description="Yolcunun cinsiyeti ('Erkek' veya 'Kadın')")
    title: str = Field(..., description="Yolcunun unvanı ('Bay', 'Hanım', 'Bayan', 'Usta', 'Doktor', 'Özgü')")
    age: int = Field(..., description="Yolcunun yaşı")
    sibsp: int = Field(..., description="Titanik'te bulunan kardeş/eş sayısı")
    parch: int = Field(..., description="Titanik'te bulunan ebeveyn/çocuk sayısı")
    embarked: str = Field(..., description="Binilen liman ('Southampton, İngiltere', 'Cherbourg, Fransa', 'Queesntown, İrlanda')")

    class Config:
        schema_extra = {
            "example": {
                "pclass": 1,
                "sex": "Erkek",
                "title": "Doktor",
                "age": 35,
                "sibsp": 0,
                "parch": 0,
                "embarked": "Cherbourg, Fransa"
            }
        }

class ArgumentResponse(BaseModel):
    survive: str
    proba: float

    class Config:
        schema_extra = {
            "example": {
                "survive": "Hayatta Kaldı",
                "proba": 75.35
            }
        }

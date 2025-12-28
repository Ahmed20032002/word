from pymongo import MongoClient

class Veritabani:
    def __init__(self):
        # الاتصال بسيرفر MongoDB المحلي
        self.client = MongoClient("mongodb://localhost:27017/")
        
        # إنشاء / استخدام قاعدة بيانات باسم hospital_system
        self.db = self.client["hospital_system"]
        
        # إنشاء / استخدام collection باسم appointments
        self.randevular = self.db["appointments"]

    def randevu_ekle(self, veri):
        # إضافة موعد جديد إلى قاعدة البيانات
        self.randevular.insert_one(veri)

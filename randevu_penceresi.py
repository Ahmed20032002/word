#استيراد عناصر الواجهة من PyQt5 
from PyQt5.QtWidgets import (
    QWidget,          # نافذة أساسية
    QLabel,           # لعرض نصوص (Labels)
    QLineEdit,        # حقول إدخال نص
    QComboBox,        # قائمة منسدلة
    QPushButton,      # زر
    QVBoxLayout,      # ترتيب عمودي للعناصر
    QMessageBox,      # نافذة رسائل
    QTableWidget,     # جدول
    QTableWidgetItem, # عنصر داخل الجدول
    QDateEdit,        # اختيار تاريخ
    QTimeEdit         # اختيار وقت
)

# استيراد التاريخ والوقت
from PyQt5.QtCore import QDate, QTime

# استيراد كلاس قاعدة البيانات
from veritabani import Veritabani

# استيراد الأقسام والأطباء
from arayuz.bolumler import BOLUMLER


# ===== كلاس نافذة حجز المواعيد =====
class RandevuPenceresi(QWidget):
    def __init__(self):
        super().__init__()

        # ===== إعدادات النافذة =====
        self.setWindowTitle("Hasta Randevu Sistemi")  # عنوان النافذة
        self.setGeometry(200, 200, 700, 600)          # حجم ومكان النافذة

        # ===== الاتصال بقاعدة البيانات =====
        self.veritabani = Veritabani()

        # ===== تحميل الأقسام =====
        self.bolumler = BOLUMLER

        # ===== عناصر الإدخال =====

        # حقل إدخال الاسم
        self.ad_input = QLineEdit()

        # حقل إدخال اللقب
        self.soyad_input = QLineEdit()

        # حقل إدخال رقم الهوية
        self.tc_input = QLineEdit()

        # قائمة اختيار القسم
        self.bolum_combo = QComboBox()

        # قائمة اختيار الطبيب
        self.doktor_combo = QComboBox()

        # ===== اختيار التاريخ =====
        self.tarih_edit = QDateEdit()
        self.tarih_edit.setDate(QDate.currentDate())   # تعيين تاريخ اليوم
        self.tarih_edit.setCalendarPopup(True)         # إظهار تقويم

        # ===== اختيار الوقت =====
        self.saat_edit = QTimeEdit()
        self.saat_edit.setTime(QTime.currentTime())    # تعيين الوقت الحالي

        # ===== تحميل الأقسام في القائمة =====
        self.bolum_combo.addItems(self.bolumler.keys())

        # عند تغيير القسم يتم تحديث قائمة الأطباء
        self.bolum_combo.currentTextChanged.connect(self.doktorlari_guncelle)

        # تحميل الأطباء لأول مرة
        self.doktorlari_guncelle()

        # ===== زر حفظ الموعد =====
        self.kaydet_buton = QPushButton("Randevu Al")

        # ربط الزر بدالة حفظ الموعد
        self.kaydet_buton.clicked.connect(self.randevu_kaydet)

        # ===== جدول عرض المواعيد =====
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)  # عدد الأعمدة

        # عناوين الأعمدة
        self.tablo.setHorizontalHeaderLabels(
            ["Ad", "Soyad", "TC", "Bölüm", "Doktor", "Tarih", "Saat"]
        )

        # بناء واجهة المستخدم
        self.arayuz_olustur()

    # ===== دالة بناء الواجهة =====
    def arayuz_olustur(self):
        # ترتيب عمودي لكل العناصر
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Ad"))
        layout.addWidget(self.ad_input)

        layout.addWidget(QLabel("Soyad"))
        layout.addWidget(self.soyad_input)

        layout.addWidget(QLabel("TC Kimlik No"))
        layout.addWidget(self.tc_input)

        layout.addWidget(QLabel("Bölüm"))
        layout.addWidget(self.bolum_combo)

        layout.addWidget(QLabel("Doktor"))
        layout.addWidget(self.doktor_combo)

        layout.addWidget(QLabel("Tarih"))
        layout.addWidget(self.tarih_edit)

        layout.addWidget(QLabel("Saat"))
        layout.addWidget(self.saat_edit)

        layout.addWidget(self.kaydet_buton)
        layout.addWidget(self.tablo)

        # تعيين التصميم للنافذة
        self.setLayout(layout)

    # ===== دالة تحديث الأطباء حسب القسم =====
    def doktorlari_guncelle(self):
        # مسح الأطباء الحاليين
        self.doktor_combo.clear()

        # القسم المختار
        secilen_bolum = self.bolum_combo.currentText()

        # إضافة الأطباء المرتبطين بالقسم
        self.doktor_combo.addItems(self.bolumler[secilen_bolum])

    # ===== دالة حفظ الموعد =====
    def randevu_kaydet(self):
        # تجميع بيانات الموعد في Dictionary
        veri = {
            "ad": self.ad_input.text(),
            "soyad": self.soyad_input.text(),
            "tc": self.tc_input.text(),
            "bolum": self.bolum_combo.currentText(),
            "doktor": self.doktor_combo.currentText(),
            "tarih": self.tarih_edit.date().toString("dd.MM.yyyy"),
            "saat": self.saat_edit.time().toString("HH:mm")
        }

        # حفظ الموعد في MongoDB
        self.veritabani.randevu_ekle(veri)

        # ===== إضافة الموعد إلى الجدول =====
        satir = self.tablo.rowCount()   # رقم الصف الجديد
        self.tablo.insertRow(satir)     # إضافة صف

        kolon = 0
        for deger in veri.values():
            # تحويل القيمة إلى نص قبل وضعها في الجدول
            self.tablo.setItem(
                satir,
                kolon,
                QTableWidgetItem(str(deger))
            )
            kolon += 1

        # رسالة تأكيد
        QMessageBox.information(
            self,
            "Başarılı",
            "Randevu başarıyla kaydedildi ✅"
        )

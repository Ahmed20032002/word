import sys
from PyQt5.QtWidgets import QApplication
from arayuz.randevu_penceresi import RandevuPenceresi

# نقطة تشغيل البرنامج
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # إنشاء نافذة حجز المواعيد
    pencere = RandevuPenceresi()
    pencere.show()
    
    sys.exit(app.exec_())

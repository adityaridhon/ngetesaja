import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QSpacerItem, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import math

class MechMathApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('MechMath')
        self.setGeometry(500, 200, 400, 300)
        self.setMinimumSize(400, 300)
        # self.setMaximumSize(400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Membuat judul aplikasi
        title_label = QLabel('MechMath', self)

        # Variasi warna dan font judul aplikasi
        title_color = 'QLabel { color: red;}'
        title_label.setStyleSheet(title_color)
        # Mengatur jenis font, ukuran font, dan ketebalan font
        title_font = QFont('Sans-serif', 20, QFont.Bold) 
        title_label.setFont(title_font) 

        # Set agar judul berada di tengah
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Mengatur jarak space judul
        spacer_item = QSpacerItem(100, 400, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        # Membuat label untuk memilih bangun
        instruction_label = QLabel("Pilih bangun yang ingin dihitung:")
        instruction_color = 'QLabel { color: red;}'
        instruction_label.setStyleSheet(instruction_color)

        layout.addWidget(instruction_label)

        # Membuat tombol untuk setiap bangun
        shapes = ["Persegi", "Segitiga sama kaki", "Segitiga siku", "Segitiga sembarang", "Lingkaran", "Setengah Lingkaran"]
        for shape in shapes:
            button = QPushButton(shape)
            button.clicked.connect(lambda _, s=shape: self.calculateMoment(s))
            layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle("MechMath")

    # Membuat input untuk bangun yang dipilih
    def calculateMoment(self, shape):
        dialog = QDialog()
        dialog.setWindowTitle("Masukkan Dimensi")
        dialog.setGeometry(500, 300, 400, 100)

        # Membuat layout vertikal di dialog
        layout = QVBoxLayout(dialog)

        # Inisialisasi variabel input di luar blok percabangan if
        input1 = None
        input2 = None
        input3 = None

        # Menambahkan label dan input box untuk masing-masing dimensi
        if shape == "Persegi":
            label1 = QLabel("Panjang:")
            layout.addWidget(label1)
            input1 = QLineEdit()
            layout.addWidget(input1)

            label2 = QLabel("Lebar:")
            layout.addWidget(label2)
            input2 = QLineEdit()
            layout.addWidget(input2)

        if shape == "Segitiga sama kaki" or shape == "Segitiga siku":
            label1 = QLabel("Alas:")
            layout.addWidget(label1)
            input1 = QLineEdit()
            layout.addWidget(input1)

            label2 = QLabel("Tinggi:")
            layout.addWidget(label2)
            input2 = QLineEdit()
            layout.addWidget(input2)

        if shape == "Segitiga sembarang":
            label1 = QLabel("Alas 1:")
            layout.addWidget(label1)
            input1 = QLineEdit()
            layout.addWidget(input1)

            label2 = QLabel("Alas 2:")
            layout.addWidget(label2)
            input2 = QLineEdit()
            layout.addWidget(input2)

            label3 = QLabel("Tinggi:")
            layout.addWidget(label3)
            input3 = QLineEdit()
            layout.addWidget(input3)

        if shape == "Lingkaran":
            label1 = QLabel("Diameter:")
            layout.addWidget(label1)
            input1 = QLineEdit()
            layout.addWidget(input1)

        if shape == "Setengah Lingkaran":
            label1 = QLabel("Jari-jari:")
            layout.addWidget(label1)
            input1 = QLineEdit()
            layout.addWidget(input1)

        # Membuat tombol "Hitung" di input
        calculate_button = QPushButton("Hitung")
        calculate_button.clicked.connect(lambda _, s=shape, i1=input1, i2=input2, i3=input3: self.showMoment(s, i1.text(), i2.text() if i2 else None, i3.text() if i3 else None))
        layout.addWidget(calculate_button)

        dialog.exec_()


    # Menghasilkan perhitungan menggunakan fungsi-fungsi rumus momen inersia
    def showMoment(self, shape, dim1, dim2=None, dim3=None):
        if shape == "Persegi":
            Ix, Iy = self.hitung_moment_inersia_persegi(int(dim1), int(dim2))
        elif shape == "Segitiga sama kaki":
            Ix, Iy = self.momen_inersia_segitigasamakaki(int(dim1), int(dim2))
        elif shape == "Segitiga siku":
            Ix, Iy = self.momen_inersia_segitigasiku(int(dim1), int(dim2))
        elif shape == "Segitiga sembarang":
            Ix, Iy = self.momen_inersia_segitigasembarang(int(dim1), int(dim2), int(dim3))
        elif shape == "Lingkaran":
            Ix, Iy = self.momen_inersia_lingkaran(int(dim1))
        elif shape == "Setengah Lingkaran":
            Ix, Iy = self.momen_inersia_setengahlingkaran(int(dim1))

        # Membulatkan nilai momen inersia
        Ix = round(Ix, 2)
        Iy = round(Iy, 2)

        QMessageBox.information(self, "Hasil", f"Momen inersia terhadap sumbu x: {Ix} cm\nMomen inersia terhadap sumbu y: {Iy} cm")

    # FUNCTION UNTUK RUMUS MOMEN INERSIA

    def hitung_moment_inersia_persegi(self, b, h): 
        Ix = 1/12 * (b * h ** 3)
        Iy = 1/12 * (h * b ** 3)
        return Ix, Iy

    def momen_inersia_segitigasamakaki(self, b, h):
        Ix = 1/36 * (b * h ** 3)
        Iy = 1/48 * (h * b ** 3)
        return Ix, Iy

    def momen_inersia_segitigasiku(self, b, h):
        Ix = 1/36 * (b * h ** 3)
        Iy = 1/48 * (h * b ** 3)
        return Ix, Iy

    def momen_inersia_segitigasembarang(self, b1, b2, h):
        b = b1 + b2
        Ix = 1/36 * (b * h ** 3)
        Iy = 1/36 * (b * h * (b ** 2 - b * b2 + b2 ** 2))
        return Ix, Iy

    def momen_inersia_lingkaran(self, d):
        Ix = 1/64 * math.pi * d ** 4
        Iy = Ix
        return Ix, Iy

    def momen_inersia_setengahlingkaran(self, r):
        Ix = 1/8 * math.pi * r ** 4
        Iy = Ix
        return Ix, Iy


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MechMathApp()
    ex.show()
    sys.exit(app.exec_())

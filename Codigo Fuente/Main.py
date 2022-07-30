from PyQt5 import QtWidgets, uic, QtCore
import sys
import os.path
import os
from PyQt5.QtGui import QPixmap

class ventana (QtWidgets.QMainWindow):
    #--CONSTRUCTOR
    def __init__(self):
        super(ventana, self).__init__()
        uic.loadUi('Interfaz.ui', self)
        self.BEditor.clicked.connect(lambda: self.Vistas.setCurrentIndex(0))
        self.BSimbolos.clicked.connect(lambda: self.Vistas.setCurrentIndex(1))
        self.BErrores.clicked.connect(lambda: self.Vistas.setCurrentIndex(2))
        self.BBases.clicked.connect(lambda: self.Vistas.setCurrentIndex(3))
        self.BTablas.clicked.connect(lambda: self.Vistas.setCurrentIndex(4))
        self.BInfo.clicked.connect(lambda: self.Vistas.setCurrentIndex(5))
        self.show()

#Ejecución de la aplicación
app = QtWidgets.QApplication(sys.argv)
main = ventana()
sys.exit(app.exec_())

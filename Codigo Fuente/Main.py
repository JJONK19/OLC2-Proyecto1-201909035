from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
import sys
import os.path
import os
from PyQt5.QtGui import QPixmap

class ventana (QtWidgets.QMainWindow):
    
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


    def añadirFilas(self, info, tabla):
        """
        añadirFilas agrega una fila a una tabla. Se debe de llamar en un ciclo para añadir varias.
        :param info: Es un arreglo con la información de una fila. 
        :param tabla: Variable que referencia a la tabla a la que se desea añadir el valor: 

        """

        col = 0
        fila = tabla.rowCount()                     
        tabla.setRowCount(fila+1)                   #Añade una nueva fila al final
        for data in info:
            casilla = QTableWidgetItem(str(data))   #Crea una casilla con el dato
            tabla.setItem(fila, col, casilla)
            col +=1
        
    def reiniciarTabla(self, tabla):
        """
        reiniciarTabla borra todas las filas que se encuentran en la tabla.
        :param tabla: Variable que referencia a la tabla a la que se desea añadir el valor: 

        """
        tabla.setRowCount(0)

app = QtWidgets.QApplication(sys.argv)
main = ventana()
sys.exit(app.exec_())

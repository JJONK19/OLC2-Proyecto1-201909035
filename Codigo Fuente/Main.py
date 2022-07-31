from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from PyQt5.QtGui import *
import os
from PyQt5.QtGui import QPixmap
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

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
        self.BAnalizar.clicked.connect(self.analizar)
        self.BLimpiar.clicked.connect(self.limpiar)

        #Manejo de los editores
        #Basado en https://www.faqcode4u.com/faq/124137/qscintilla-based-text-editor-in-pyqt5-with-clickable-functions-and-variables
        font = QFont()
        font.setPointSize(12)
        font.setFamily('Courier')
        font.setFixedPitch(True)
        metrics = QFontMetrics(font)
        self.Consola.setReadOnly(True)
        self.Consola.setFont(font)
        self.Consola.setMarginsFont(font)
        self.Entrada.setFont(font)
        self.Entrada.setMarginsFont(font)
        self.Consola.setMarginsBackgroundColor(QColor("#395b64"))
        self.Entrada.setMarginsBackgroundColor(QColor("#395b64"))
        self.Entrada.setMarginsFont(font)
        self.Consola.setMarginsFont(font)
        self.Consola.setMarginLineNumbers(0, True)
        self.Entrada.setMarginLineNumbers(0, True)
        self.Entrada.setMarginWidth(0, metrics.width("00000") + 3)
        self.Consola.setMarginWidth(0, metrics.width("00000") + 3)

        #Variables de la aplicación
        ENTRADA = ""                #Texto ubicado en el espacio de entrada
        SALIDA = ""                 #Texto a colocar en la consola
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

    def analizar(self):
        """
        analizar toma el texto ubicado en Entrada y lo manda a analizar. Este metodo prepara
        y distribuye la información por toda la aplicación.

        """
        #--- Recopilar el texto
        ENTRADA = self.Entrada.text()

        #--- Analizar cadena

    def limpiar(self):
        """
        limpiar borra toda la información almacenada en la consola y en las tablas.

        """
        self.Entrada.setText("")
        self.Consola.setText("")
        self.TBases.setRowCount(0)
        self.TErrores.setRowCount(0)
        self.TSimbolos.setRowCount(0)
        self.TTablas.setRowCount(0)


app = QtWidgets.QApplication(sys.argv)
main = ventana()
sys.exit(app.exec_())

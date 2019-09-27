import sys, os, subprocess
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QRegExp, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QPixmap, QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QMainWindow, QAction, qApp, QDialog, QLabel, QMessageBox, QPushButton
from tftp import TFTPClient
from client import create_parser
from pathlib import PurePosixPath, Path

##LEvantar el server: python server.py -H 192.168.2.20 -p 69 -u C:\Users\Armando\Desktop\serv

class proyecto(QMainWindow):
	
	def __init__(self):
		super().__init__()
		uic.loadUi("windows.ui",self)
		#self.arg = arg
		self.radioU.setChecked(True)
		self.widgetDownload.setEnabled(False)
		self.setWindowIcon(QIcon('img/pplogo.png'))

		qApp.setStyle("kvantum-dark")
		#qApp.setStyle("Fusion")

		dark_palette = QPalette()

		dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.WindowText, Qt.white)
		dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Text, Qt.white)
		dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ButtonText, Qt.white)
		dark_palette.setColor(QPalette.BrightText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.HighlightedText, Qt.black)

		qApp.setPalette(dark_palette)

		qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")		

		

		#Definiendo el input port
		self.portValidate = QIntValidator(0, 1023, self)
		self.inputPort.setValidator(self.portValidate)
		self.inputPort.setEnabled(False)
		
		#Definiendo el input block
		self.blockValidate = QIntValidator(8, 1468, self) #En practica definimos 1468 o 65464 como en el rfc 2348
		self.inputBlocksize.setValidator(self.blockValidate) 
		self.inputBlocksize.setEnabled(False)
		
		#Definiendo el input Window
		self.winValidate = QIntValidator(1, 65535, self)
		self.inputWindow.setValidator(self.winValidate) 
		self.inputWindow.setEnabled(False)

		#Definiendo RadioButtons y CheckBox
		self.radioD.clicked.connect(self.activarDownload)
		self.radioU.clicked.connect(self.activarUpload)
		self.checkBoxPuerto.stateChanged.connect(self.activarPort)
		self.checkBoxBlocksize.stateChanged.connect(self.activarBlock)
		self.checkBoxWindowsize.stateChanged.connect(self.activarWind)

		#Definicion de los botones Upload y Download
		self.finalizarU.clicked.connect(self.finalizar_Up)
		self.finalizarD.clicked.connect(self.finalizar_Dw)
		
		self.model = QFileSystemModel()
		self.model.setRootPath('/home')
		self.arbolDir.setModel(self.model)
		self.arbolDir.clicked.connect(self.dummy)
		self.menusUI()
		
	
	def show_dialog(self):
		msg = QMessageBox()
		msg.setWindowIcon(QIcon('img/pplogo64.png'))
		msg.setIconPixmap(QPixmap('img/pplogo64.png'))
		#msg.setIcon(QMessageBox.Information)

		msg.setText("TrivialPiper")
		msg.setInformativeText("0.1.5")
		msg.setWindowTitle("TrivialPiper")
		msg.setDetailedText("TrivialPiper is a practical tftp gui client created by PiedPiper")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.setBaseSize(QSize(400, 120))
		#msg.buttonClicked.connect(self.msgButtonClick)

		

	#def msgButtonClick(i):
		#print("Button clicked is:",i.text())
		

	def menusUI(self):
		exitAction = QAction(QIcon('img/exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)

		statusbar = self.statusBar()
		menubar = self.menuBar()

		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		aboutAction = QAction(QIcon('img/info.png'), '&About', self)
		aboutAction.triggered.connect(self.show_dialog)
		helpMenu = menubar.addMenu('&Help')
		helpMenu.addAction(aboutAction)

	def finalizar_Up(self):
		self.ip = self.inputIP.text()
		self.port = self.inputPort.text()
		self.bsize = self.inputBlocksize.text()
		self.wsize = self.inputWindow.text()
		self.path = self.dummy()
		self.fname = PurePosixPath(self.path).name
		self.data = Path(self.path).read_bytes()
		#ejeecutamos el client.py como subproceso
		self.command = "python3 client.py -p "+ self.path+" -b "+ self.bsize+" -w "+ self.wsize+" "+ self.ip+" "+ self.port
		output = subprocess.run([self.command],shell=True)
		if output.returncode == 0:
			self.estadoUp.setText("Estado: Correcto")
		else:
			self.estadoUp.setText("Estado: Error")

	
	def finalizar_Dw(self):
		self.ip = self.inputIP.text()
		self.port = self.inputPort.text()
		self.bsize = self.inputBlocksize.text()
		self.wsize = self.inputWindow.text()
		self.fname = PurePosixPath(self.inputDownloadFile.text()).name
		#Llamar a funcion en client.py o tftp
		self.command = "client.py -g "+self.fname+" -b "+ self.bsize+" -w "+ self.wsize+" "+ self.ip+" "+ self.port
		output = subprocess.run([self.command],shell=True)
		if output.returncode == 0:
			self.estadoDw.setText("Estado: Correcto")
		else:
			self.estadoDw.setText("Estado: Error")
		
	def dummy(self):
		index = self.arbolDir.currentIndex()
		#print (self.model.filePath(index))
		return self.model.filePath(index)
	def activarDownload(self):
		self.widgetUpload.setEnabled(False)
		self.widgetDownload.setEnabled(True)
	def activarUpload(self):
		self.widgetDownload.setEnabled(False)
		self.widgetUpload.setEnabled(True)
	def activarWind(self, state):
		if QtCore.Qt.Checked == state:
			self.inputWindow.setEnabled(True)
		else:
			self.inputWindow.setEnabled(False)
	def activarPort(self, state):
		if QtCore.Qt.Checked == state:
			self.inputPort.setEnabled(True)
		else:
			self.inputPort.setEnabled(False)		
	def activarBlock(self, state):
		if QtCore.Qt.Checked == state:
			self.inputBlocksize.setEnabled(True)
		else:
			self.inputBlocksize.setEnabled(False)





if __name__ == '__main__':
	app = QApplication(sys.argv)
	proy = proyecto()
	proy.show()
	sys.exit(app.exec_())

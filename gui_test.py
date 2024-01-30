import sys

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets


class SocketWidget(QtWidgets.QWidget):
	pin_size: int = 15
	palette: QtGui.QPalette = QtGui.QPalette()
	palette.setColor(QtGui.QPalette.Background, QtGui.QColor("#456"))

	def __init__(self, parent) -> None:
		super().__init__(parent)

		self._layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
		self._layout.setContentsMargins(0, 3, 3, 3)
		self._layout.setSpacing(3)
		self.setLayout(self._layout)

		pin: QtWidgets.QLabel = QtWidgets.QLabel()
		pin.setFixedHeight(SocketWidget.pin_size)
		pin.setFixedWidth(SocketWidget.pin_size)
		pin.setAutoFillBackground(True)
		pin.setPalette(SocketWidget.palette)

		self._layout.addWidget(pin)
		self._layout.addWidget(QtWidgets.QLabel("Label"))
		self._line_edit: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
		self._line_edit.setPlaceholderText("Enter value")
		self._layout.addWidget(self._line_edit)
		self._layout.addWidget(QtWidgets.QPushButton("Ok"))


app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
main_window: QtWidgets.QWidget = QtWidgets.QWidget()
main_window.setWindowTitle("My App")
main_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
main_window.setLayout(main_layout)

gr_view: QtWidgets.QGraphicsView = QtWidgets.QGraphicsView()
gr_view.setRenderHint(QtGui.QPainter.Antialiasing)
gr_scene: QtWidgets.QGraphicsScene = QtWidgets.QGraphicsScene()
gr_view.setScene(gr_scene)
main_layout.addWidget(gr_view)

default_border: QtGui.QPen = QtGui.QPen(QtGui.QColor("black"))
default_border.setWidth(1)
default_brush: QtGui.QBrush = QtGui.QBrush(QtGui.QColor("#456"))

gr_rect: QtWidgets.QGraphicsRectItem = QtWidgets.QGraphicsRectItem(QtCore.QRect(50, 50, 200, 20))
gr_rect.setBrush(default_brush)
gr_rect.setPen(default_border)
gr_rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
shadow: QtWidgets.QGraphicsDropShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
shadow.setBlurRadius(5)
gr_rect.setGraphicsEffect(shadow)
gr_rect.moveBy(300, 200)
gr_scene.addItem(gr_rect)

socket_widget: SocketWidget = SocketWidget(None)
gr_socket: QtWidgets.QGraphicsProxyWidget = gr_scene.addWidget(socket_widget)
gr_socket.setGeometry(QtCore.QRect(50, 70, 200, 10))
gr_socket.setParentItem(gr_rect)

socket_widget: SocketWidget = SocketWidget(None)
gr_socket: QtWidgets.QGraphicsProxyWidget = gr_scene.addWidget(socket_widget)
gr_socket.setGeometry(QtCore.QRect(50, 95, 200, 10))
gr_socket.setParentItem(gr_rect)

main_window.resize(640, 400)
main_window.show()
app.exec_()

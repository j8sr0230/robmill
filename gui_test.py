import sys

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets


class SocketWidget(QtWidgets.QWidget):
	pin_size: int = 12
	layout_spacing: int = 4

	def __init__(self, parent) -> None:
		super().__init__(parent)

		self.setWindowTitle("My Node")
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

		self._layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
		self._layout.setContentsMargins(
			SocketWidget.pin_size + SocketWidget.layout_spacing,
			SocketWidget.layout_spacing,
			SocketWidget.layout_spacing,
			SocketWidget.layout_spacing
		)
		self._layout.setSpacing(SocketWidget.layout_spacing)
		self.setLayout(self._layout)

		self._layout.addWidget(QtWidgets.QLabel("Label"))
		self._line_edit: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
		self._line_edit.setPlaceholderText("Enter value")
		self._layout.addWidget(self._line_edit)
		self._layout.addWidget(QtWidgets.QPushButton("Ok"))
		self._layout.addWidget(QtWidgets.QCheckBox())

	def paintEvent(self, event: QtGui.QPaintEvent) -> None:
		super().paintEvent(event)

		painter: QtGui.QPainter = QtGui.QPainter(self)
		painter.save()

		brush: QtGui.QBrush = QtGui.QBrush()
		brush.setColor(QtGui.QColor("olive"))
		brush.setStyle(QtCore.Qt.SolidPattern)
		painter.setBrush(brush)

		pen: QtGui.QPen = QtGui.QPen()
		pen.setWidth(1)
		pen.setColor(QtGui.QColor("#292929"))
		painter.setPen(pen)

		rect = QtCore.QRect(
			0, painter.device().height() / 2 - SocketWidget.pin_size / 2,
			SocketWidget.pin_size, SocketWidget.pin_size
		)
		painter.drawEllipse(rect)

		painter.restore()


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

socket_widget: SocketWidget = SocketWidget(None)
gr_socket: QtWidgets.QGraphicsProxyWidget = gr_scene.addWidget(
	socket_widget, QtCore.Qt.Widget
)

shadow: QtWidgets.QGraphicsDropShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
shadow.setOffset(4)
shadow.setBlurRadius(12)

gr_rect: QtWidgets.QGraphicsRectItem = QtWidgets.QGraphicsRectItem()
gr_rect.setRect(QtCore.QRect(SocketWidget.pin_size // 2, 0, socket_widget.width() - 5, socket_widget.height()))
gr_rect.setBrush(QtGui.QBrush(QtGui.QColor("#aaa")))
gr_rect.setPen(QtGui.QPen(QtGui.QColor("#aaa")))
gr_rect.setZValue(-1)
gr_rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
gr_rect.setGraphicsEffect(shadow)
gr_scene.addItem(gr_rect)
gr_socket.setParentItem(gr_rect)

main_window.resize(640, 400)
main_window.show()
app.exec_()

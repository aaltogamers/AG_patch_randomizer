import sys
import time
import random
import threading

from PySide6 import QtCore, QtWidgets, QtGui

import sheets

class WorkerSignals(QtCore.QObject):

    selected = QtCore.Signal(str)


class UpdateThread(QtCore.QRunnable):

    def __init__(self, initial_list, stop_event):
        super().__init__()
        self.stop_event = stop_event
        self.initial_list = initial_list
        self.signals = WorkerSignals()

    def run(self):
        print("Update thread running")
        while not self.stop_event.is_set():
            data = random.choice(self.initial_list)
            # print(data)
            self.signals.selected.emit(data)
            time.sleep(0.25)  # sleep for a while so that the choice is visible in UI
        print("Update thread stopped")

class FetchThread(QtCore.QRunnable):

    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event
        self.signals = WorkerSignals()

    def run(self):
        patches = sheets.get_patches()
        name = []
        odds = []
        for patch in patches:
            name.append(patch)
            odds.append(patches[patch])
            print(f"{patch}, count: {patches[patch]}")
        data = random.choices(name, weights=odds)[0]
        print(f"Selected patch: {data}")
        sheets.update_inventory(data)
        self.stop_event.set()  # Signal UpdateThread to stop
        time.sleep(0.25)  # Not the prettiest but should make sure that UpdateThread has stopped
        self.signals.selected.emit(data)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initial_list = sheets.get_initial_list()

        self.button = QtWidgets.QPushButton("Click here!")
        self.text = QtWidgets.QLabel("AG Patch Roulette",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("QLabel{font-size: 18pt;}")
        self.button.setStyleSheet("QPushButton{height: 50px; width: 200px;font-size: 18pt;}")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.label = QtWidgets.QLabel(self, alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        
        self.threadpool = QtCore.QThreadPool()

        self.button.clicked.connect(self.start_threads)

    def update_label(self, s):
        print(s)
        pixmap = QtGui.QPixmap(f'assets/{s}.png').scaledToHeight(512)
        self.label.setPixmap(pixmap)

    @QtCore.Slot()
    def start_threads(self):
        self.stop_event = threading.Event()
        self.updater = UpdateThread(self.initial_list, self.stop_event)
        self.worker_thread = QtCore.QThread()

        self.updater.signals.selected.connect(self.update_label)

        fetcher = FetchThread(self.stop_event)
        fetcher.signals.selected.connect(self.update_label)

        self.threadpool.start(self.updater)
        self.threadpool.start(fetcher)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
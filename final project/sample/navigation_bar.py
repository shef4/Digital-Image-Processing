# a widget to handle the navigation bar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class NavigationBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # create open file button
        open_file_button = QPushButton('Open File')
        open_file_button.clicked.connect(self.parent.open_file)

        # create save file button
        save_file_button = QPushButton('Save File')
        save_file_button.clicked.connect(self.parent.save_file)

        # create run code button
        run_code_button = QPushButton('Run Code')
        run_code_button.clicked.connect(self.parent.run_code)

        # create about button
        about_button = QPushButton('About')
        about_button.clicked.connect(self.parent.show_about_message)

        # create layout
        layout = QHBoxLayout()
        layout.addWidget(open_file_button)
        layout.addWidget(save_file_button)
        layout.addWidget(run_code_button)
        layout.addWidget(about_button)

        # set layout
        self.setLayout(layout)




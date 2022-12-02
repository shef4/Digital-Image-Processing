# importing required libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
 
class ScribbleArea(QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.lastPoint = QPoint()

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False
    
    def getImage(self):
        return self.image

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        rad = self.myPenWidth / 2 + 2
        self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = QPoint(endPoint)

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = newImage

    def print_(self):
        printer = QPrinter(QPrinter.HighResolution)

        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)
            painter.end()

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth

# Creating main window class
class MainWindow(QMainWindow):
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.saveAsActs = []

        # setting window geometry
        self.setGeometry(100, 100, 600, 400)
        # creating a Qgridlayout
        layout = QGridLayout()


        '''
        touchpad widget start
        '''
        # creating a ScribbleArea object
        self.scribbleArea = ScribbleArea()
        # creating a QWidget touchpad
        touchpad = QWidget()
        # creating a Qgridlayout
        touchpad_layout = QGridLayout()
        # creating a Qpushbutton
        clear_button = QPushButton("Clear")
        # creating a Qpushbutton
        enter_button = QPushButton("Enter") 
        # adding action to the button
        clear_button.clicked.connect(self.scribbleArea.clearImage)
        # adding action to the button
        enter_button.clicked.connect(self.enter_symbol)
        # adding widgets to the layout
        touchpad_layout.addWidget(clear_button, 0, 0)
        touchpad_layout.addWidget(enter_button, 0, 1)
        touchpad_layout.addWidget(self.scribbleArea, 1, 0, 1, 2)
        touchpad.setLayout(touchpad_layout)
        '''
            touchpad widget end
        '''


        
        # creating a QPlainTextEdit object
        self.editor = QPlainTextEdit()
        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # create a QPlainTextEdit object
        self.terminal = QPlainTextEdit()
        # setting font to the terminal
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.terminal.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None
        # adding editor to layout
        layout.addWidget(self.editor, 0, 0)
        # adding touchpad to layout
        layout.addWidget(touchpad, 0, 1)
        # adding terminal to the layout
        layout.addWidget(self.terminal, 1, 0, 1, 2)
        # creating a QWidget layout
        container = QWidget()
        # setting layout to the container
        container.setLayout(layout)
        # making container as central widget
        self.setCentralWidget(container)
 
        # creating a status bar object
        self.status = QStatusBar()
        # setting stats bar to the window
        self.setStatusBar(self.status)

 


 
        # # creating actions to add in the file menu

        # # creating a open file action
        # open_file_action = QAction("Open file", self)
        # open_file_action.setStatusTip("Open file")
        # open_file_action.triggered.connect(self.file_open)
        # # similarly creating a save action
        # save_file_action = QAction("Save", self)
        # save_file_action.setStatusTip("Save current page")
        # save_file_action.triggered.connect(self.file_save)
        # # similarly creating save action
        # saveas_file_action = QAction("Save As", self)
        # saveas_file_action.setStatusTip("Save current page to specified file")
        # saveas_file_action.triggered.connect(self.file_saveas)
        # # for print action
        # print_action = QAction("Print", self)
        # print_action.setStatusTip("Print current page")
        # print_action.triggered.connect(self.file_print)

        # # creating a file tool bar
        # file_toolbar = QToolBar("File")
        # # adding file tool bar to the window
        # self.addToolBar(file_toolbar)
        # # add actions to tool bar
        # file_toolbar.addAction(open_file_action)
        # file_toolbar.addAction(save_file_action) 
        # file_toolbar.addAction(saveas_file_action)  
        # file_toolbar.addAction(print_action)  

        # # creating a file menu
        # file_menu = self.menuBar().addMenu("&File")
        # # add actions to file menu
        # file_menu.addAction(open_file_action)
        # file_menu.addAction(save_file_action)
        # file_menu.addAction(saveas_file_action)
        # file_menu.addAction(print_action)

        

        # # adding actions to the Edit menu and toolbar
        # # undo action
        # undo_action = QAction("Undo", self)
        # undo_action.setStatusTip("Undo last change")
        # undo_action.triggered.connect(self.editor.undo)
        # # redo action
        # redo_action = QAction("Redo", self)
        # redo_action.setStatusTip("Redo last change")
        # redo_action.triggered.connect(self.editor.redo)
        # # cut action
        # cut_action = QAction("Cut", self)
        # cut_action.setStatusTip("Cut selected text")
        # cut_action.triggered.connect(self.editor.cut)
        # # copy action
        # copy_action = QAction("Copy", self)
        # copy_action.setStatusTip("Copy selected text")
        # copy_action.triggered.connect(self.editor.copy)
        # # paste action
        # paste_action = QAction("Paste", self)
        # paste_action.setStatusTip("Paste from clipboard")
        # paste_action.triggered.connect(self.editor.paste)
        # # select all action
        # select_action = QAction("Select all", self)
        # select_action.setStatusTip("Select all text")
        # select_action.triggered.connect(self.editor.selectAll)
        # # adding actions to the tool bar and menu bar
        # run_action = QAction("Run", self)
        # run_action.setStatusTip("Run the code")
        # run_action.triggered.connect(self.run_code)
        # # wrap action
        # wrap_action = QAction("Wrap text to window", self)
        # wrap_action.setStatusTip("Check to wrap text to window")
        # wrap_action.setCheckable(True)
        # wrap_action.setChecked(True)
        # wrap_action.triggered.connect(self.edit_toggle_wrap)

        # # creating another tool bar for editing text
        # edit_toolbar = QToolBar("Edit")
        # # adding this tool bar to the main window
        # self.addToolBar(edit_toolbar)
        # # add action to tool and toolbar
        # edit_toolbar.addAction(undo_action)
        # edit_toolbar.addAction(redo_action)
        # edit_toolbar.addAction(cut_action)
        # edit_toolbar.addAction(copy_action)
        # edit_toolbar.addAction(paste_action)
        # edit_toolbar.addAction(select_action)
        # edit_toolbar.addAction(run_action)

        # # creating a edit menu bar
        # edit_menu = self.menuBar().addMenu("&Edit")
        # # add action to tool and menu bar
        # edit_menu.addAction(undo_action)
        # edit_menu.addAction(redo_action)
        # edit_menu.addAction(cut_action)
        # edit_menu.addAction(copy_action)
        # edit_menu.addAction(paste_action)
        # edit_menu.addAction(select_action)
        # edit_menu.addAction(run_action)
        # edit_menu.addAction(wrap_action)

        self.createActions()
        self.createToolbars()
        self.createMenus()

 
        # calling update title method
        self.update_title()
        # showing all the components
        self.show()

        
    def createActions(self):
        self.wrapAct = QAction("Wrap text to window", self, shortcut=QKeySequence(Qt.CTRL + Qt.Key_W),
                statusTip="Check to wrap text to window", triggered=self.edit_toggle_wrap)
        self.wrapAct.setCheckable(True)
        self.wrapAct.setChecked(True)

        self.openAct = QAction("Open file", self, shortcut=QKeySequence.Open,
                statusTip="Open file", triggered=self.file_open)

        self.runAct = QAction(QIcon('create.png'), '&Create', self, shortcut=QKeySequence(Qt.CTRL + Qt.Key_R),
                statusTip="Run the code", triggered=self.run_code)

        self.newAct = QAction(QIcon('new.png'), '&New', self, shortcut=QKeySequence.New,
                statusTip="Create a new file", triggered=self.file_new)

        self.saveAct = QAction(QIcon('save.png'), '&Save', self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.file_save)

        self.saveAsAct = QAction("Save &As...", self, shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.file_saveas)

        self.printAct = QAction(QIcon('print.png'), '&Print...', self, shortcut=QKeySequence.Print,
                statusTip="Print the document", triggered=self.file_print)

        self.exitAct = QAction("&Exit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)

        self.cutAct = QAction(QIcon('cut.png'), "&Cut", self, shortcut=QKeySequence.Cut,
                statusTip="Cut the current selection's contents to the clipboard",
                triggered=self.editor.cut)

        self.copyAct = QAction(QIcon('copy.png'), "&Copy", self, shortcut=QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.editor.copy)

        self.pasteAct = QAction(QIcon('paste.png'), "&Paste", self, shortcut=QKeySequence.Paste,
                statusTip="Paste the clipboard's contents into the current selection",
                triggered=self.editor.paste)

        self.undoAct = QAction(QIcon('undo.png'), "&Undo", self, shortcut=QKeySequence.Undo,
                statusTip="Undo the last operation", triggered=self.editor.undo)

        self.redoAct = QAction(QIcon('redo.png'), "&Redo", self, shortcut=QKeySequence.Redo,
                statusTip="Redo the last operation", triggered=self.editor.redo)


    def createToolbars(self):
        fileToolbar = self.addToolBar("File")
        fileToolbar.addAction(self.newAct)
        fileToolbar.addAction(self.openAct)
        fileToolbar.addAction(self.saveAct)
        fileToolbar.addAction(self.printAct)

        editToolbar = self.addToolBar("Edit")
        editToolbar.addAction(self.cutAct)
        editToolbar.addAction(self.copyAct)
        editToolbar.addAction(self.pasteAct)
        editToolbar.addAction(self.undoAct)
        editToolbar.addAction(self.redoAct)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)

    #method for entering symbol to editer
    def enter_symbol(self):
        #img = self.scribbleArea.getImage
        #set display text in qplaintextedit self.editor
        self.editor.appenPlainText("test")

    # method for runing the code
    def run_code(self):
        # # getting the text from the editor
        # code = self.editor.toPlainText()
        # sk = Symbolkast_Interperator()
        # # running the code
        # ok = sk.parse(code)
        # if ok:
        #     try:
        #         result = sk.run()
        #         self.terminal.setPlainText(result.__repr__())
        #     except Exception as e:
        #         print(e)
        #         self.terminal.setPlainText("Error: " + str(e))
        # else:
        #     self.terminal.setPlainText("Error: " + sk.error)
        #set display text in qplaintextedit self.termnal 
        self.terminal.appendPlainText("test")


    # creating dialog critical method
    # to show errors
    def dialog_critical(self, s):
 
        # creating a QMessageBox object
        dlg = QMessageBox(self)
 
        # setting text to the dlg
        dlg.setText(s)
 
        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)
 
        # showing it
        dlg.show()

    #action callend by newAct to create new file and save previous file if it is not saved
    def file_new(self):
        self.maybe_save()
        self.editor.clear()
        self.filename = None

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    
    def maybeSave(self):
        if self.scribbleArea.isModified():
            ret = QMessageBox.warning(self, "Scribble",
                        "The image has been modified.\n"
                        "Do you want to save your changes?",
                        QMessageBox.Save | QMessageBox.Discard |
                        QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile('png')
            elif ret == QMessageBox.Cancel:
                return False

        return True

        
 
    # action called by file open action
    def file_open(self):
 
        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                             "Text documents (*.txt);All files (*.*)")
 
        # if path is true
        if path:
            # try opening path
            try:
                with open(path, 'rU') as f:
                    # read the file
                    text = f.read()
 
            # if some error occurred
            except Exception as e:
 
                # show error using critical method
                self.dialog_critical(str(e))
            # else
            else:
                # update path value
                self.path = path
 
                # update the text
                self.editor.setPlainText(text)
 
                # update the title
                self.update_title()
 
    # action called by file save action
    def file_save(self):
 
        # if there is no save path
        if self.path is None:
 
            # call save as method
            return self.file_saveas()
 
        # else call save to path method
        self._save_to_path(self.path)
 
    # action called by save as action
    def file_saveas(self):
 
        # opening path
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                             "Text documents (*.txt);All files (*.*)")
 
        # if dialog is cancelled i.e no path is selected
        if not path:
            # return this method
            # i.e no action performed
            return
 
        # else call save to path method
        self._save_to_path(path)
 
    # save to path method
    def _save_to_path(self, path):
 
        # get the text
        text = self.editor.toPlainText()
 
        # try catch block
        try:
 
            # opening file to write
            with open(path, 'w') as f:
 
                # write text in the file
                f.write(text)
 
        # if error occurs
        except Exception as e:
 
            # show error using critical
            self.dialog_critical(str(e))
 
        # else do this
        else:
            # change path
            self.path = path
            # update the title
            self.update_title()
 
    # action called by print
    def file_print(self):
 
        # creating a QPrintDialog
        dlg = QPrintDialog()
 
        # if executed
        if dlg.exec_():
 
            # print the text
            self.editor.print_(dlg.printer())
 
    # update title method
    def update_title(self):
 
        # setting window title with prefix as file name
        # suffix aas PyQt5 Notepad
        self.setWindowTitle("%s - SymbolKast Notepad" %(os.path.basename(self.path)
                                                  if self.path else "Untitled"))
 
    # action called by edit toggle
    def edit_toggle_wrap(self):
 
        # chaining line wrap mode
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0 )
 
 
# drivers code
if __name__ == '__main__':
 
    # creating PyQt5 application
    app = QApplication(sys.argv)
 
    # setting application name
    app.setApplicationName("PyQt5-Note")
 
    # creating a main window object
    window = MainWindow()
 
    # loop
    app.exec_()
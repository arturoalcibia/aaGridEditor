from PyQt5 import QtCore, QtWidgets

import view

def createGridEditor():
    '''
    Create the grid Editor and displays the window.

    Returns:
        None.
    '''
    app = QtWidgets.QApplication([])

    aaView = view.View()

    scene = aaView.scene()

    aaView.show()
    app.exec_()

if __name__ == "__main__":
    gridEditor = createGridEditor()

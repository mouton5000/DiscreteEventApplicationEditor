#!/usr/bin/env python

import sys
from PyQt4.QtGui import QApplication as QApp
from gui.EditorWindow import MainWindow


def main():
    app = QApp(sys.argv)
    ex = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()





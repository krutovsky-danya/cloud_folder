# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019
@author: Даня
"""

import sys
from PyQt5.QtWidgets import QApplication

from Shell import Shell
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Shell()
    win.show()

    sys.exit(app.exec_())

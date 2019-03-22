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
    win.main_widget.ListOfUserFolders[self.main_widget.user_id].setSelected()
    win.main_widget.ListOfServerFolders[0].setSelected()
    win.show()

    sys.exit(app.exec_())

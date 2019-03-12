# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019
@author: Даня
"""

from PyQt5.QtGui import (QPixmap,
                         QIcon,
                         QMovie)
from PyQt5.QtWidgets import (QApplication,
                             QDialog,
                             QLabel,
                             QHBoxLayout)

from nanachi import nanachi
from Shell import Shell


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Shell()
    win.show()

    loading = QDialog()
    firstlay = QHBoxLayout()
    first = QLabel()
    dance = QMovie('Icons//loading.gif')
    first.setMovie(dance)
    dance.start()
    firstlay.addWidget(first)
    loading.setLayout(firstlay)
    loading.setWindowTitle('Loading')
    loading.setWindowIconText(nanachi)
    loading.setWindowIcon(QIcon(QPixmap('Icons//Tsu.jpg')))
    #loading.show()

    topLoading = QDialog()
    secondlay = QHBoxLayout()
    second = QLabel()
    parade = QMovie('Icons//topLoading.gif')
    #parade.setScaledSize(QSize(120, 120)) #Для сжатия
    second.setMovie(parade)
    parade.start()
    secondlay.addWidget(second)
    topLoading.setLayout(secondlay)
    topLoading.setWindowTitle('TopLoading')
    topLoading.setWindowIconText(nanachi)
    topLoading.setWindowIcon(QIcon(QPixmap('Icons//HirosavaUri.png')))
    #topLoading.show()

sys.exit(app.exec_())

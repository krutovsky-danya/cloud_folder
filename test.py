import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class Test(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        window = QWidget(self)
        self.setCentralWidget(window)

        verticalLayout = QHBoxLayout(window)

        self.tree = QTreeWidget(window)
        self.tree.header().setVisible(False)
        item = QTreeWidgetItem(self.tree, ["User_Name"])
        #self.tree.addTopLevelItem(item)

        item_1 = QTreeWidgetItem(item, ["For_Danya"])
        #item.addChild(item_1)
        item_1_1 = QTreeWidgetItem(item_1, ["Test.txt"])
        #item_1.addChild(item_1_1)
        item_1_2 = QTreeWidgetItem(item_1, ["png.txt"])
        #item_1.addChild(item_1_2)

        verticalLayout.addWidget(self.tree)

        list = QListWidget(window)
        list_item_1 = QListWidgetItem("Test.txt")
        list.addItem(list_item_1)

        verticalLayout.addWidget(list)

        self.setGeometry(300, 300, 700, 600)
        self.setMinimumSize(QtCore.QSize(700, 600))
        self.show()

        self.tree.itemSelectionChanged.connect(self.OpenFolder)

    def OpenFolder(self):
        item = self.tree.currentItem()
        print(item.text(0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())

    '''
self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
self.settingItem = QtWidgets.QListWidgetItem(QtGui.QIcon(":/resources/result_setting.png"), "")
    '''

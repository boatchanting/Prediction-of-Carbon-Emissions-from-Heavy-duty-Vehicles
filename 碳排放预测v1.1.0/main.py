import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect
from usemodel import ModelApp
from drawplot import PlotDataApp
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('碳排放预测')
        self.setGeometry(self.get_screen_work_area())
        #self.setGeometry(100, 100, 800, 600)

        # 设置程序图标
        self.setWindowIcon(QIcon('icon.png'))

        # 创建 QTabWidget 和添加页面
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # 添加 ModelApp 和 PlotDataApp 页面
        self.model_app = ModelApp()
        self.tab_widget.addTab(self.model_app, '碳排放预测')

        self.plot_data_app = PlotDataApp()
        self.tab_widget.addTab(self.plot_data_app, '数据可视化')

    def get_screen_work_area(self):
        # 获取屏幕的工作区域（去掉任务栏）
        screen_geometry = QApplication.primaryScreen().geometry()
        work_area = QApplication.primaryScreen().availableGeometry()
        # 设置窗口大小为工作区域
        return QRect(int(0.8*work_area.x()), int(0.8*work_area.y()), int(0.8*work_area.width()), int(0.8*work_area.height()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,QCheckBox,QComboBox, QLineEdit, QLabel, QFileDialog, QApplication, QSlider, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotDataApp(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化组件
        self.init_ui()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 文件路径输入
        self.file_path_label = QLabel("数据文件路径：")
        self.file_path_input = QLineEdit()
        self.file_path_input.setText(".\\model\\speed example_result.xlsx")
        self.browse_button = QPushButton("浏览")
        self.browse_button.clicked.connect(self.open_file_dialog)

        # 绘图风格下拉菜单
        self.plot_style_label = QLabel("绘图风格：")
        self.plot_style_combo = QComboBox()
        self.plot_style_combo.addItems(["白色网格", "黑色网格", "黑色", "刻度"])

         # 平滑曲线显示控制复选框
        self.show_smooth_line_checkbox = QCheckBox("平滑曲线")
        self.show_smooth_line_checkbox.setChecked(True)  # 默认勾选

        # 平滑因子滑动条
        self.smooth_factor_label = QLabel("平滑因子：")
        self.smooth_factor_slider = QSlider(Qt.Horizontal)
        self.smooth_factor_slider.setMinimum(1)
        self.smooth_factor_slider.setMaximum(30)
        self.smooth_factor_slider.setValue(5)  # 默认值为0.05
        self.smooth_factor_slider.setTickInterval(1)
        self.smooth_factor_slider.setTickPosition(QSlider.TicksBelow)
        self.smooth_factor_slider.setSingleStep(1)
        self.smooth_factor_slider.valueChanged.connect(self.update_smooth_factor_label)
        self.smooth_factor_value_label = QLabel("0.05")

        # 绘图类型下拉菜单
        self.plot_type_label = QLabel("绘图类型：")
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([ "排放", "车速", "车速累积", "排放累积"])

        # 线条颜色选择
        self.line_color_label = QLabel("线条颜色：")
        self.line_color_combo = QComboBox()
        self.line_color_combo.addItems(["蓝色", "橙色", "绿色", "红色", "紫色", "青色", "品红", "黑色", "自定义"])

        # 平滑曲线颜色选择
        self.smooth_line_color_label = QLabel("平滑曲线颜色：")
        self.smooth_line_color_combo = QComboBox()
        self.smooth_line_color_combo.addItems(["橙色", "绿色", "红色", "紫色", "青色", "品红", "黑色", "自定义"])

        # 自定义颜色按钮
        self.custom_line_color_button = QPushButton("选择自定义线条颜色")
        self.custom_line_color_button.clicked.connect(self.open_custom_line_color_dialog)
        self.custom_smooth_line_color_button = QPushButton("选择自定义平滑曲线颜色")
        self.custom_smooth_line_color_button.clicked.connect(self.open_custom_smooth_line_color_dialog)

        # 绘图按钮
        self.plot_button = QPushButton("绘制数据")
        self.plot_button.clicked.connect(self.plot_data)

        # 保存图片按钮
        self.save_button = QPushButton("保存图片")
        self.save_button.clicked.connect(self.save_plot)

        # 创建Matplotlib图表区域
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)

        # 创建一个水平布局
        main_layout = QHBoxLayout()

        # 创建左侧的垂直布局，用于放置所有控件
        left_layout = QVBoxLayout()

        # 将控件添加到左侧布局
        left_layout.addWidget(self.file_path_label)
        left_layout.addWidget(self.file_path_input)
        left_layout.addWidget(self.browse_button)
        left_layout.addWidget(self.plot_style_label)
        left_layout.addWidget(self.plot_style_combo)
        left_layout.addWidget(self.show_smooth_line_checkbox)
        left_layout.addWidget(self.smooth_factor_label)
        left_layout.addWidget(self.smooth_factor_slider)
        left_layout.addWidget(self.smooth_factor_value_label)
        left_layout.addWidget(self.plot_type_label)
        left_layout.addWidget(self.plot_type_combo)
        left_layout.addWidget(self.line_color_label)
        left_layout.addWidget(self.line_color_combo)
        left_layout.addWidget(self.custom_line_color_button)
        left_layout.addWidget(self.smooth_line_color_label)
        left_layout.addWidget(self.smooth_line_color_combo)
        left_layout.addWidget(self.custom_smooth_line_color_button)
        left_layout.addWidget(self.plot_button)
        left_layout.addWidget(self.save_button)

        # 将左侧布局添加到主布局
        main_layout.addLayout(left_layout, stretch=1)  # 左侧控件占0.2的宽度

        # 将画布添加到主布局的右侧
        main_layout.addWidget(self.canvas, stretch=4)  # 右侧图表占0.8的宽度

        # 设置主布局
        self.setLayout(main_layout)

        self.setWindowTitle('数据绘图应用程序')

        # 设置样式表
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 20px;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 20px;
            }
            QComboBox {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 20px;
            }
            QSlider {
                padding: 5px;
            }
        """)

        self.show()

        # 存储用户选择的颜色
        self.custom_line_color = None
        self.custom_smooth_line_color = None

        # 映射字典
        self.plot_style_map = {
            "白色网格": "whitegrid",
            "黑色网格": "darkgrid",
            "黑色": "dark",
            "刻度": "ticks"
        }
        self.color_map = {
            "蓝色": "blue",
            "橙色": "orange",
            "绿色": "green",
            "红色": "red",
            "紫色": "purple",
            "青色": "cyan",
            "品红": "magenta",
            "黑色": "black"
        }

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "打开数据文件", "", "Excel 文件 (*.xlsx);;所有文件 (*)", options=options)
        if file_path:
            self.file_path_input.setText(file_path)

    def update_smooth_factor_label(self):
        smooth_factor = self.smooth_factor_slider.value() / 100.0
        self.smooth_factor_value_label.setText(f"{smooth_factor:.2f}")

    def open_custom_line_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.custom_line_color = color.name()
            self.line_color_combo.setCurrentText("自定义")

    def open_custom_smooth_line_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.custom_smooth_line_color = color.name()
            self.smooth_line_color_combo.setCurrentText("自定义")

    def plot_data(self):
        data_path = self.file_path_input.text()
        plot_style = self.plot_style_map.get(self.plot_style_combo.currentText(), "whitegrid")
        smooth_factor = self.smooth_factor_slider.value() / 100.0
        plot_type = self.plot_type_combo.currentText()
        line_color = self.color_map.get(self.line_color_combo.currentText(), "blue")
        smooth_line_color = self.color_map.get(self.smooth_line_color_combo.currentText(), "orange")
        show_smooth_line = self.show_smooth_line_checkbox.isChecked()

        # 处理自定义颜色
        if self.line_color_combo.currentText() == "自定义" and self.custom_line_color:
            line_color = self.custom_line_color
        if self.smooth_line_color_combo.currentText() == "自定义" and self.custom_smooth_line_color:
            smooth_line_color = self.custom_smooth_line_color

        # 调用绘图函数
        self.plot_data_func(data_path, plot_style, smooth_factor, plot_type, line_color, smooth_line_color, show_smooth_line)

    def plot_data_func(self, data_path, plot_style, smooth_factor, plot_type, line_color, smooth_line_color, show_smooth_line):
        # 读取数据
        df = pd.read_excel(data_path)

        # 设置绘图风格
        sns.set(style=plot_style)

        # 平滑长度
        smooth_length = int(len(df) * smooth_factor)

        # 创建图表
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

        if plot_type == "车速":
            y_data = df['speed(km/h)']
            y_label = '车速(km/h)'
            title = '车速随时间变化'

        elif plot_type == "排放":
            y_data = df['emission(kg/s)']
            y_label = '排放(kg/s)'
            title = '排放随时间变化'

        elif plot_type == "车速累积":
            y_data = df['speed(km/h)'].cumsum()
            y_label = '车速累积(km)'
            title = '车速累积随时间变化'

        elif plot_type == "排放累积":
            y_data = df['emission(kg/s)'].cumsum()
            y_label = '排放累积(kg)'
            title = '排放累积随时间变化'

        else:
            return

        # 绘制线条
        sns.lineplot(x=df.index, y=y_data, ax=ax, color=line_color, label='原始数据')

        # 绘制平滑曲线
        if show_smooth_line and smooth_length > 1:
            smoothed_y_data = y_data.rolling(window=smooth_length, min_periods=1).mean()
            ax.plot(df.index, smoothed_y_data, color=smooth_line_color, label='平滑曲线')

        # 设置图表属性
        ax.set_title(title)
        ax.set_xlabel('时间')
        ax.set_ylabel(y_label)
        ax.legend()
        ax.grid(True)

        # 刷新画布
        self.canvas.draw()



    def save_plot(self):
        # 打开文件对话框让用户选择保存路径
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG文件 (*.png);;所有文件 (*)", options=options)
        if file_path:
            # 保存图片到指定路径
            self.figure.savefig(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotDataApp()
    sys.exit(app.exec_())

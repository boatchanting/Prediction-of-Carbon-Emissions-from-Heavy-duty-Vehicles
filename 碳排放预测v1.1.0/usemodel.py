import sys
import os
import torch
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QLineEdit, QMessageBox, QComboBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
import torch.nn as nn

class BPModel(nn.Module):
    def __init__(self, input_dim, hidden_dim1, hidden_dim2, output_dim):
        super(BPModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim1)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim1, hidden_dim2)
        self.fc3 = nn.Linear(hidden_dim2, output_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

class ModelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('模型预测工具')
        self.setWindowIcon(QIcon('icon.png'))  # Set your icon path here
        self.resize(600, 400)  # Increase the size of the window

        layout = QVBoxLayout()
        
        # 默认路径参数
        default_model_path = '.\\model\\model.pth'
        default_data_path = '.\\model\\speed example.xlsx'
        self.default_output_folder = os.path.dirname(default_data_path)
        self.desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

        # 设置字体
        font = QFont('Arial', 12)
        self.setFont(font)

        # 模型路径选择
        self.model_path_label = QLabel('选择模型路径:')
        self.model_path_edit = QLineEdit(self)
        self.model_path_edit.setText(default_model_path)
        self.model_path_button = QPushButton('选择模型路径', self)
        self.model_path_button.clicked.connect(self.chooseModelPath)

        # 数据路径选择
        self.data_path_label = QLabel('选择数据路径:')
        self.data_path_edit = QLineEdit(self)
        self.data_path_edit.setText(default_data_path)
        self.data_path_button = QPushButton('选择数据路径', self)
        self.data_path_button.clicked.connect(self.chooseDataPath)

        # 输出路径选择
        self.output_path_label = QLabel('选择输出文件夹:')
        self.output_path_combo = QComboBox(self)
        self.output_path_combo.addItem(f"与输入数据路径相同")
        self.output_path_combo.addItem(f"桌面")
        self.output_path_combo.addItem("自定义路径")
        self.output_path_combo.currentIndexChanged.connect(self.updateOutputPath)

        self.custom_output_folder = ''
        self.output_file_label = QLabel('输出文件名:')
        self.output_file_edit = QLineEdit(self)
        self.output_file_edit.setText(self.getDefaultOutputFilename())

        # 预测按钮
        self.predict_button = QPushButton('执行预测', self)
        self.predict_button.clicked.connect(self.runPrediction)

        # 布局
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.model_path_label)
        form_layout.addWidget(self.model_path_edit)
        form_layout.addWidget(self.model_path_button)
        form_layout.addWidget(self.data_path_label)
        form_layout.addWidget(self.data_path_edit)
        form_layout.addWidget(self.data_path_button)
        form_layout.addWidget(self.output_path_label)
        form_layout.addWidget(self.output_path_combo)
        form_layout.addWidget(self.output_file_label)
        form_layout.addWidget(self.output_file_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.predict_button)
        button_layout.addStretch()

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 应用样式
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
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QComboBox {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
        """)

    def chooseModelPath(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "选择模型文件", "", "PyTorch Model Files (*.pth)")
        if model_path:
            self.model_path_edit.setText(model_path)

    def chooseDataPath(self):
        data_path, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", "Excel Files (*.xlsx)")
        if data_path:
            self.data_path_edit.setText(data_path)
            self.default_output_folder = os.path.dirname(data_path)
            self.updateOutputPath()

    def updateOutputPath(self):
        index = self.output_path_combo.currentIndex()
        if index == 0:
            self.custom_output_folder = self.default_output_folder
        elif index == 1:
            self.custom_output_folder = self.desktop_path
        else:
            folder = QFileDialog.getExistingDirectory(self, "选择自定义输出路径")
            if folder:
                self.custom_output_folder = folder
                self.output_path_combo.setItemText(2, f"自定义路径: {self.custom_output_folder}")
            else:
                # 如果用户没有选择路径，恢复为默认的路径选择
                self.output_path_combo.setCurrentIndex(0)
                self.custom_output_folder = self.default_output_folder

        # 更新默认的输出文件名
        self.output_file_edit.setText(self.getDefaultOutputFilename())

    def getDefaultOutputFilename(self):
        data_path = self.data_path_edit.text()
        base_name = os.path.splitext(os.path.basename(data_path))[0]
        return f"{base_name}_result.xlsx"

    def runPrediction(self):
        model_path = self.model_path_edit.text()
        data_path = self.data_path_edit.text()
        output_folder = self.custom_output_folder
        output_filename = self.output_file_edit.text()
        output_path = os.path.join(output_folder, output_filename)

        if not model_path or not data_path or not output_filename:
            QMessageBox.warning(self, "警告", "请确保所有路径和文件名都已选择!")
            return

        try:
            # 模型参数
            input_dim = 10
            hidden_dim1 = 256
            hidden_dim2 = 64
            output_dim = 1

            # 加载模型
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = BPModel(input_dim, hidden_dim1, hidden_dim2, output_dim).to(device)
            checkpoint = torch.load(model_path, map_location=device)
            model.load_state_dict(checkpoint['model_state_dict'])
            model.eval()

            # 读取数据
            df = pd.read_excel(data_path)
            speeds = df['speed'].values

            # 标准化数据
            standardized_speeds = speeds / 100

            # 准备预测
            window_size = input_dim
            predictions = []

            for i in range(len(standardized_speeds) - window_size + 1):
                window = standardized_speeds[i:i + window_size]
                
                # 处理特殊情况：车速均为零
                if np.all(window == 0):
                    predicted_value = 0.001082  # 特殊情况的碳排放值
                else:
                    input_data = torch.tensor(window, dtype=torch.float32).unsqueeze(0).to(device)

                    with torch.no_grad():
                        prediction = model(input_data)

                    predicted_value = prediction.item() / 20  # 反标准化
                
                predictions.append(predicted_value)

            # 将预测结果与原始数据对齐
            predicted_series = np.full_like(speeds, np.nan, dtype=np.float32)
            predicted_series[window_size - 1:] = predictions

            # 创建结果数据框
            result_df = pd.DataFrame({
                'speed(km/h)': speeds,
                'emission(kg/s)': predicted_series
            })

            # 保存结果到 Excel 文件
            result_df.to_excel(output_path, index=False)
            QMessageBox.information(self, "成功", f"结果已保存到 {output_path}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModelApp()
    ex.show()
    sys.exit(app.exec_())

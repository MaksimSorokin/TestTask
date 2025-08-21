import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QListView, QPushButton, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt, QStringListModel
from .api_client import ApiClient

class ApiClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.api_client = ApiClient()
        os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("TestMAST Client")
        self.setGeometry(300, 300, 600, 500)
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Поле ввода
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введите текст для отправки...")
        layout.addWidget(QLabel("Текст для отправки:"))
        layout.addWidget(self.line_edit)
        
        # Кнопки
        self.post_button = QPushButton("Отправить данные (POST)")
        self.post_button.clicked.connect(self.send_post_request)
        layout.addWidget(self.post_button)
        
        self.get_button = QPushButton("Получить данные (GET)")
        self.get_button.clicked.connect(self.send_get_request)
        layout.addWidget(self.get_button)
        
        # Список для отображения
        layout.addWidget(QLabel("Полученные данные:"))
        self.list_view = QListView()
        self.list_model = QStringListModel()
        self.list_view.setModel(self.list_model)
        layout.addWidget(self.list_view)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def send_post_request(self):
        try:
            text = self.line_edit.text().strip()
            if not text:
                QMessageBox.warning(self, "Ошибка", "Поле ввода не может быть пустым")
                return
            
            self.click_count += 1
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            item = self.api_client.create_item(
                description=text,
                day=current_date,
                time=current_time,
                click_number=self.click_count
            )
            
            QMessageBox.information(self, "Успех", f"Данные успешно отправлены!\nID: {item.id}")
            self.line_edit.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при отправке: {str(e)}")
    
    def send_get_request(self):
        try:
            items = self.api_client.get_items()
            
            if not items:
                self.list_model.setStringList(["Нет данных для отображения"])
                return
            
            display_data = []
            for item in items:
                display_text = (
                    f"ID: {item.id} | "
                    f"Описание: {item.description} |"
                    f"Дата: {item.day} |"
                    f"Время: {item.time} |"
                    f"Номер клика: {item.click_number}"
                )
                display_data.append(display_text)
            
            self.list_model.setStringList(display_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при получении данных: {str(e)}")
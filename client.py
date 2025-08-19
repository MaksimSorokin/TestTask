import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QLineEdit, QListView, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QStringListModel
import requests
import os

class ApiClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.server_url = "http://127.0.0.1:8000"  # URL вашего сервера

        os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
        self.init_ui()
        
    def init_ui(self):
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Создаем элементы интерфейса
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введите текст для отправки")
        
        self.list_view = QListView()
        self.list_model = QStringListModel()
        self.list_view.setModel(self.list_model)
        
        self.post_button = QPushButton("Отправить данные (POST)")
        self.post_button.clicked.connect(self.send_post_request)
        
        self.get_button = QPushButton("Получить данные (GET)")
        self.get_button.clicked.connect(self.send_get_request)
        
        # Добавляем элементы в layout
        layout.addWidget(self.line_edit)
        layout.addWidget(self.list_view)
        layout.addWidget(self.post_button)
        layout.addWidget(self.get_button)
        
        # Настройка главного окна
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Клиент для API")
        self.setGeometry(300, 300, 400, 400)
        
    def send_post_request(self):
        """Отправка POST запроса на сервер"""
        self.click_count += 1
        text = self.line_edit.text()
        
        if not text:
            QMessageBox.warning(self, "Ошибка", "Поле ввода не может быть пустым")
            return
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        data = {
            "description": text,
            "day": current_date,
            "time": current_time,
            "click_number": self.click_count
        }
        
        try:
            response = requests.post(
                f"{self.server_url}/items/",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                QMessageBox.information(self, "Успех", "Данные успешно отправлены")
            else:
                QMessageBox.critical(self, "Ошибка", 
                                   f"Ошибка сервера: {response.status_code}\n{response.text}")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к серверу: {str(e)}")
            
    def send_get_request(self):
        """Отправка GET запроса на сервер и отображение результатов"""
        try:
            response = requests.get(f"{self.server_url}/items/")
            
            if response.status_code == 200:
                items = response.json()
                if not items:
                    self.list_model.setStringList(["Сервер вернул пустой список"])
                    return
                
                # Форматируем данные для отображения
                display_data = []
                for item in items:
                    display_str = (f"Текст: {item['description']}, Дата: {item['day']}, Время: {item['time']}, Номер клика: {item['click_number']}")
                    display_data.append(display_str)
                
                self.list_model.setStringList(display_data)
                
            else:
                QMessageBox.critical(self, "Ошибка", 
                                   f"Ошибка сервера: {response.status_code}\n{response.text}")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к серверу: {str(e)}")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Не удалось обработать ответ сервера")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApiClientApp()
    window.show()
    sys.exit(app.exec_())
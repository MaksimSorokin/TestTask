import pytest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from client import ApiClientApp

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def app(qapp, qtbot):
    window = ApiClientApp()
    qtbot.addWidget(window)
    yield window
    window.close()

def test_post_request(app, qtbot):
    # Отправка POST запроса
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        
        # Введение и отправка данных по клику
        qtbot.keyClicks(app.line_edit, "Test")
        qtbot.mouseClick(app.post_button, Qt.LeftButton)
        
        assert mock_post.called
        assert "Test" in str(mock_post.call_args)

def test_successful_get_request(app, qtbot):
    """Тестируем получение и отображение данных"""
    # Подготавливаем тестовые данные
    test_data = [
        {
            "description": "Test", 
            "day": "15.08.2025", 
            "time": "15:43", 
            "click_number": 1
        },
        {
            "description": "Test2", 
            "day": "15.08.2025", 
            "time": "15:44", 
            "click_number": 2
        }
    ]
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = test_data
        
        # Имитируем клик на кнопке GET
        qtbot.mouseClick(app.get_button, Qt.LeftButton)
        
        # Проверяем вызов API
        mock_get.assert_called_once_with(f"{app.server_url}/items/")
        
        # Проверяем отображение данных в QListView
        displayed_items = app.list_model.stringList()
        assert len(displayed_items) == 2
        assert "Test" in displayed_items[0]
        assert "15:43" in displayed_items[0]
        assert "Test2" in displayed_items[1]
        assert "15:44" in displayed_items[1]


def test_empty_post_request(app, qtbot):
    """ Отправка POST запроса """
        
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_msgbox:
        # Выполняем действия
        qtbot.mouseClick(app.post_button, Qt.LeftButton)
        
        # Проверяем вызов message box
        assert mock_msgbox.called
        args, _ = mock_msgbox.call_args
        assert "Ошибка" in args[1]  # Проверяем заголовок
        assert "Поле ввода не может быть пустым" in args[2]  # Проверяем текст ошибки
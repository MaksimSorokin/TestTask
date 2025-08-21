import pytest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.client.main import ApiClientApp

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
    """Тестируем отправку POST запроса"""
    with patch('src.client.api_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "id": 1,
            "description": "Test", 
            "day": "15.08.2025",
            "time": "15:45",
            "click_number": 1
        }
        
        qtbot.keyClicks(app.line_edit, "Test")
        qtbot.mouseClick(app.post_button, Qt.LeftButton)
        
        assert mock_post.called
        call_args = mock_post.call_args[1]['json']
        assert call_args['description'] == "Test"

def test_get_request(app, qtbot):
    """Тестируем получение данных"""
    test_data = [
        {"id": 1, "description": "Test1", "day": "15.08.2025", "time": "14:48", "click_number": 1},
        {"id": 2, "description": "Test2", "day": "15.08.2025", "time": "14:24", "click_number": 2}
    ]
    
    # Мокаем requests в api_client
    with patch('src.client.api_client.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = test_data
        
        qtbot.mouseClick(app.get_button, Qt.LeftButton)
        qtbot.wait(100)
        
        displayed_items = app.list_model.stringList()
        assert len(displayed_items) == 2
        assert "Test1" in displayed_items[0]
        assert "Test2" in displayed_items[1]

def test_empty_post_request(app, qtbot):
    """Тестируем пустой запрос"""
    with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_msgbox:
        app.line_edit.clear()
        qtbot.mouseClick(app.post_button, Qt.LeftButton)
        
        assert mock_msgbox.called
        args, _ = mock_msgbox.call_args
        assert "Ошибка" in args[1]
        assert "Поле ввода не может быть пустым" in args[2]

def test_error_handling(app, qtbot):
    """Тестируем обработку ошибок"""
    # Мокаем requests в api_client
    with patch('src.client.api_client.requests.post') as mock_post:
        mock_post.side_effect = Exception("Connection error")
        
        with patch('PyQt5.QtWidgets.QMessageBox.critical') as mock_msgbox:
            qtbot.keyClicks(app.line_edit, "Test")
            qtbot.mouseClick(app.post_button, Qt.LeftButton)
            
            assert mock_msgbox.called
            args, _ = mock_msgbox.call_args
            assert "Ошибка" in args[1]
            assert "Connection error" in args[2]

def test_click_counter_increment(app, qtbot):
    """Тестируем увеличение счетчика кликов"""
    initial_count = app.click_count
    
    # Мокаем requests в api_client
    with patch('src.client.api_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "id": 1, "description": "Test", "day": "15.08.2025", "time": "14:48", "click_number": initial_count + 1
        }
        
        qtbot.keyClicks(app.line_edit, "Test")
        qtbot.mouseClick(app.post_button, Qt.LeftButton)
        
        assert app.click_count == initial_count + 1
        call_args = mock_post.call_args[1]['json']
        assert call_args['click_number'] == initial_count + 1
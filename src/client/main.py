import sys
from PyQt5.QtWidgets import QApplication
from .app import ApiClientApp

def main():
    app = QApplication(sys.argv)
    window = ApiClientApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
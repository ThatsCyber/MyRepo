import sys
import traceback
from PyQt6.QtWidgets import QApplication
from gui import MainWindow

def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 
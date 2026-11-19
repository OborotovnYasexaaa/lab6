import sys

from PyQt6.QtWidgets import QApplication 
from main_window import MainWindow
def main():
    app=QApplication(sys.argv)#создаёт объект графического приложения и связывает его с операционной системой передавая аргументы запуска.
    window=MainWindow()
    window.show()#окно для видимое человеком
    sys.exit(app.exec())
if __name__=="__main__":
    main()
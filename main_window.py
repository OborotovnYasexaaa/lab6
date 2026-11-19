from PyQt6.QtWidgets import (
    QComboBox,#выпадающий список (фильтр задач)
    QHBoxLayout,#как расположены по горизонтали
    QInputDialog,#диалог ввода (для редактирования задачи)
    QLabel,#текстовая подпись (просто текст, нельзя редактировать)
    QLineEdit,#однострочное поле ввода (сюда пишут название задачи)
    QListWidget,#список элементов (здесь будут храниться задачи)
    QListWidgetItem,#один элемент списка (нужен для галочки)
    QMainWindow,#главное окно
    QPushButton,#кнопка
    QVBoxLayout,#как располоджено(друг под другом)
    QWidget,#память(коробка)
    QMessageBox,#предупреждение
)
from PyQt6.QtCore import Qt#(галочка выполнено)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер задач")#для названия панельки
        self.resize(500,400)#размерность

        self.init_ui()
        self.connect_signals()


    def init_ui(self):
        self.label=QLabel("Новая задача")
        self.lEdit=QLineEdit()
        self.lEdit.setPlaceholderText("Название задачи")
        self.button_plus=QPushButton("Добавить")
        self.list=QListWidget()
        self.button_minus=QPushButton("Удалить")
        self.but_clear=QPushButton("Очистить всё")
        self.all_tasks=QLabel('Количество задач:0')
        self.filter_box=QComboBox()#выпадающий список для фильтра
        self.filter_box.addItems(['Все задачи','Активные','Выполненные'])

        central=QWidget()
        self.setCentralWidget(central)
        layout=QVBoxLayout()
        central.setLayout(layout)#кладём раскладку в коробку

        input_layout=QHBoxLayout()
        input_layout.addWidget(self.lEdit)
        input_layout.addWidget(self.button_plus)

        buttons_layout=QHBoxLayout()           
        buttons_layout.addWidget(self.button_minus)
        buttons_layout.addWidget(self.but_clear)


        layout.addWidget(self.label)
        layout.addLayout(input_layout)
        layout.addWidget(self.list)
        layout.addWidget(self.filter_box)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.all_tasks)


    def connect_signals(self):
        self.button_plus.clicked.connect(self.add_task)
        self.lEdit.returnPressed.connect(self.add_task)#ввод и через enter
        self.button_minus.clicked.connect(self.delete_task)
        self.but_clear.clicked.connect(self.clear_tasks)
        self.list.itemChanged.connect(self.done)#поставили галочку
        self.list.itemDoubleClicked.connect(self.edit_task)#правим задачу по двойному клику
        self.filter_box.currentIndexChanged.connect(self.filter_tasks)#смена фильтра
        self.update_counter()

    def add_task(self):
        text=self.lEdit.text()#получаем строку из поля(QLineEdit)
        text=text.strip()#удаляем пробелы
        if not text:
            return QMessageBox.warning(self,'ошибка','Вы не ввели название задачи')
        item=QListWidgetItem(text)#создаём элемент списка
        item.setFlags(item.flags()|Qt.ItemFlag.ItemIsUserCheckable)#разрешаем галочку
        item.setCheckState(Qt.CheckState.Unchecked)#сначала задача не выполнена
        self.list.addItem(item)#добавляем в список
        self.lEdit.clear()#очищаем поле
        self.update_counter()
        self.filter_tasks(self.filter_box.currentIndex())#новая задача сразу учитывает фильтр

    def delete_task(self):
        row=self.list.currentRow()#получаем индекс текущей строки
        if row<0:
            return QMessageBox.warning(self,'ошибка','Вы не выбрали задачу')
        answer=QMessageBox.question(self,'Удаление задачи','Вы уверены?')
        if answer==QMessageBox.StandardButton.Yes:
            self.list.takeItem(row)#удаляем строку
            self.update_counter()

    def clear_tasks(self):
        if self.list.count()==0:
            return
        answer=QMessageBox.question(self, "Очистка", "Удалить все задачи?")
        if answer==QMessageBox.StandardButton.Yes:
            self.list.clear()#удаляем все элементы
            self.update_counter()

    def update_counter(self):
        count=self.list.count()
        self.all_tasks.setText(f"Количество задач: {count}")

    def done(self,item):
        font=item.font()#берём текущий шрифт
        font.setStrikeOut(item.checkState()==Qt.CheckState.Checked)#зачёркиваем выполненные
        self.list.blockSignals(True)#отключаем сигналы, иначе setFont вызовет этот метод снова
        item.setFont(font)#применяем шрифт
        self.list.blockSignals(False)#включаем сигналы обратно

    def edit_task(self,item):
        text,ok=QInputDialog.getText(self,'Редактирование','Новое название:',text=item.text())#старое название уже вписано
        if not ok:
            return#нажали «Отмена» — ничего не меняем
        text=text.strip()#убираем пробелы по краям
        if not text:
            return QMessageBox.warning(self,'ошибка','Название не может быть пустым')
        item.setText(text)#меняем название на месте

    def filter_tasks(self,index):
        for i in range(self.list.count()):#проходим по всем задачам
            item=self.list.item(i)
            done=item.checkState()==Qt.CheckState.Checked#задача выполнена?
            if index==0:#«Все задачи» — показываем всё
                item.setHidden(False)
            elif index==1:#«Активные» — прячем выполненные
                item.setHidden(done)
            else:#«Выполненные» — прячем невыполненные
                item.setHidden(not done)

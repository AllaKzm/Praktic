import sys
from bd import Database
import random
import mysql
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QGraphicsScene, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.setWindowTitle("Эм, а как назвать-то?")


    def authoriz(self, wnd):
        dialog = DialogAutorization(wnd)
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

class DialogAutorization(QDialog):
    def __init__(self, wnd, parent = None):
        self.wnd = wnd
        super(DialogAutorization, self).__init__(parent)
        self.ui = uic.loadUi("forms/auth.ui", self)
        self.setWindowTitle("Авторизация?")
        self.scene = QGraphicsScene(0, 0, 350, 50)
        self.ui.autorization_btn.clicked.connect(self.autoriz)
        self.ui.captcha_gen.setScene(self.scene)
        self.ui.reboot_btn.clicked.connect(self.gen_captcha)
        self.gen_captcha()
        self.db = Database()
        self.enter_try = 0
        self.cur_captcha = None

    def autoriz(self):
        login = self.ui.line_log.text()
        password = self.ui.line_pas.text()

        print (login, password)
        aut = self.db.get_log(login)
        autpas=aut[0]
        role=aut[1]

        if self.ui.line_cap.text() != self.cur_captcha:
            self.wrong_captcha()
            self.enter_try += 1
        elif password == autpas:
            if role == 'Старший смены':
                self.shif_head_open()
            if role == 'Администратор':
                self.admin_open()
            if role == 'Продавец':
                self.seller_open()
        else:
            self.enter_try += 1
            self.wrong_pass_msg()
            if self.enter_try == 3:
                self.ui.autorization_btn.setEnabled(True)

    def shif_head_open(self):
        self.ui.close()
        self.ui = ShiftHeadMenu()
        self.ui.show()

    def admin_open(self):
        self.ui.close()
        self.ui = AdminMenu()
        self.ui.show()

    def seller_open(self):
        self.ui.close()
        self.ui = SellerMenu()
        self.ui.show()

    def gen_captcha(self):
        self.scene.clear()
        symb = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        s_count = 5

        cur_symb = [1, 2, 3, 4, 5]
        x, y = 30, 20
        self.scene.addLine(20, random.randint(10, 40), 300, random.randint(10, 40))
        for i in range(s_count):
            cur_symb[i] = symb[random.randint(0, 61)]
            text = self.scene.addText(f"{cur_symb[i]}")
            x += 40
            text.moveBy(x, y+random.randint(-10, 10))
        self.cur_captcha=''.join(cur_symb)

    def empty_pole(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Заполните все необходимые поля!")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def wrong_captcha(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Неверно введена капча!")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def wrong_pass_msg(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Неверно введен пароль или логин.")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

class ShiftHeadMenu(QMainWindow):
    def __init__(self):
        super(ShiftHeadMenu, self).__init__()
        self.ui = uic.loadUi("forms/shift_head.ui", self)
        self.window().setWindowTitle("ShifHead")

class AdminMenu(QMainWindow):
    def __init__(self):
        super(AdminMenu, self).__init__()
        self.ui = uic.loadUi("forms/admin2.ui", self)
        self.window().setWindowTitle("Admin")
        self.db = Database()
        self.ui.orders_btn.clicked.connect(self.orders)
        self.ui.history_btn.clicked.connect(self.history)
        self.table = self.ui.tableWidget

    def orders(self):
        self.table.clear()
        out = self.db.getRequests()
        self.table.setColumnCount(9)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'код заказа', 'дата создания','Время заказа','Код клиента','Код услуги','статус', 'дата закрытия','время аренды'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def history(self):
        self.table.clear()
        out = self.db.getHistory()
        self.table.setColumnCount(4)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Дата входа', 'Дата выхода', 'Id сотрудника'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

class SellerMenu(QMainWindow):
    def __init__(self):
        super(SellerMenu, self).__init__()
        self.ui = uic.loadUi("forms/seller.ui", self)
        self.window().setWindowTitle("Seller")
        self.db = Database()
        self.ui.order_add_btn.clicked.connect(self.orders)
        self.table = self.ui.order_table

    def orders(self):
        self.table.clear()
        out = self.db.getRequests()
        self.table.setColumnCount(9)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'код заказа', 'дата создания','Время заказа','Код клиента','Код услуги','статус', 'дата закрытия','время аренды'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

class Builder:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.wnd = MainWindow()
        self.auth()

    def auth(self):
        self.wnd.authoriz(self.wnd)
        self.app.exec()

if __name__ == '__main__':
    B = Builder()
import sys
from bd import Database
import random
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QGraphicsScene

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
        self.setWindowTitle("Эм, а как назвать-то?")

        self.ui.autorization_btn.clicked.connect(self.autoriz)
        self.db = Database()
        self.enter_try = 0

    def autoriz(self):
        login = self.ui.line_log.text()
        password = self.ui.line_pas.text()
        print (login, password)
        aut = self.db.get_log(login)
        autpas=aut[0]
        role=aut[1]
        if password == autpas:
            if role == 'Старший смены':
                self.shif_head_open()
            if role == 'Администратор':
                self.admin_open()
            if role == 'Продавец':
                self.seller_open()
        else:
            self.wrong_pass_msg()
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
        symb = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        s_count = 4
        pass

    def empty_pole(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Заполните все необходимые поля!")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def wrong_login_msg(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Данного логина не существует .")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def wrong_pass_msg(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Неверно введен пароль.")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

class ShiftHeadMenu(QMainWindow):
    def __init__(self):
        super(ShiftHeadMenu, self).__init__()
        self.ui = uic.loadUi("forms/shoft_head.ui", self)
        self.window().setWindowTitle("ShifHead")

class AdminMenu(QMainWindow):
    def __init__(self):
        super(AdminMenu, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.window().setWindowTitle("Admin")
        self.ui.orders_btn.clicked.connect(self.orders)

    def orders(self,wnd):
        dialog = DialogTable(wnd)
        dialog.setWindowTitle("Заказы")
        dialog.show()


class SellerMenu(QMainWindow):
    def __init__(self):
        super(SellerMenu, self).__init__()
        self.ui = uic.loadUi("forms/seller.ui", self)
        self.window().setWindowTitle("Seller")

class DialogTable(QDialog):
    def __init__(self, wnd, parent=None):
        self.wnd = wnd
        super(DialogAutorization, self).__init__(parent)
        self.ui = uic.loadUi("forms/table.ui", self)

    def open_table(self,):
        self.table.clear()
        self.table.setColumnCount()

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
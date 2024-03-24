import math
import sys
from datetime import date
from aifc import Error

import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow, \
    QPlainTextEdit, QTableWidget, QTableWidgetItem
# from PyQt5.QtGui import QIcon
# from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from pathlib import Path

#from notes import Note_Window


class Add_Note_Windowwww(QMainWindow):
    def __init__(self, email, name):
        super().__init__()
        self.email = email
        self.name = name
        self.today = date.today()
        self.date_format = self.today.strftime("%B %d, %Y")
        # window properties
        self.note_window = None

        self.setWindowTitle("Стоянки")
        self.resize(975, 500)
        self.setStyleSheet("background-color: #ffffff;")


        self.add_label = QLabel(self)
        self.add_label.move(200, 15)
        self.add_label.setText("стоянки")
        self.add_label.setStyleSheet("font-size:24px")

        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(400, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Номер стоянки")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        #
        #
        # self.add_label = QLabel(self)
        # self.add_label.move(250, 30)
        # self.add_label.setText("Адрес")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(250, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Адрес")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        #
        #
        # self.add_label = QLabel(self)
        # self.add_label.move(100, 30)
        # self.add_label.setText("Самокаты")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(100, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Номер самокатов")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        connection = None
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(75, 50, 390, 400)
        self.tableWidget.setColumnCount(2)
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            cursor = connection.cursor()
            cursor.execute(f"SELECT id_stoynka, adres FROM stoynka;")
            records = cursor.fetchall()
            print(len(records))
            for a in range(math.ceil(len(records) / 1) + 1):
                self.tableWidget.insertRow(a)
                if a > 0:
                    if a - 1 < len(records):
                        record_1 = records[a - 1]
                        for col_index, value in enumerate(record_1[:2]):
                            item_1 = QTableWidgetItem(str(value))
                            self.tableWidget.setItem(a, col_index, item_1)

                    # if a * 2 - 3 < len(records):
                    #     record_2 = records[a * 2 - 3]
                    #     for col_index, value in enumerate(record_2[1:6], start=6):
                    #         item_2 = QTableWidgetItem(str(value))
                    #         self.tableWidget.setItem(a, col_index, item_2)

            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.horizontalHeader().setVisible(False)

            # Добавление заголовков и объединение ячеек
            self.tableWidget.setSpan(0, 1, 0, 2)

            new_item = QTableWidgetItem("Номер стоянки")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("Адрес")
            self.tableWidget.setItem(0, 1, new_item)


            # Выравнивание столбцов по содержимому
            self.tableWidget.resizeColumnsToContents()
            # self.tableWidget.itemChanged.connect(self.save_date)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

        self.button_1 = QPushButton("Назад", self) #действует как add пока что
        self.button_1.move(25, 450)
        self.button_1.resize(190, 40)
        self.button_1.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_1.clicked.connect(self.close)

        self.button_add = QPushButton("Добавить", self)
        self.button_add.move(825, 15)
        self.button_add.resize(190, 40)
        self.button_add.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_add.clicked.connect(self.dobavit)

        # -------------------------------------------------------------добовление

        self.abox1 = QLineEdit(self)
        self.abox1.move(800, 75)
        self.abox1.resize(75, 25)

        self.abox2 = QLineEdit(self)
        self.abox2.move(875, 75)
        self.abox2.resize(75, 25)

        # self.abox3 = QLineEdit(self)
        # self.abox3.move(950, 75)
        # self.abox3.resize(75, 25)
        #
        # self.abox4 = QLineEdit(self)
        # self.abox4.move(1025, 75)
        # self.abox4.resize(75, 25)
        #
        # self.abox5 = QLineEdit(self)
        # self.abox5.move(1100, 75)
        # self.abox5.resize(75, 25)

        self.show()

        self.alert_message = QMessageBox()

    def create_note_action(self):
        if Path("notes.txt").exists():
            self.note_value = self.text_input.toPlainText()
            self.note_value = self.note_value.strip()
            if self.note_value == "":
                self.alert_message.setText("Please enter something")
                self.alert_message.setWindowTitle("Error")
                self.alert_message.exec()
            else:
                self.append_file = open('notes.txt', 'a')
                self.append_file.write(
                    self.note_value + ',,,,' + self.date_format + ';;;;')
                self.append_file.close()
                self.alert_message.setText("Your note has been added. Please click the refresh button.")
                self.alert_message.setWindowTitle("Success")
                self.alert_message.exec()
                self.close()

    def dobavit(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            c="insert into stoynka (id_stoynka, adres) values ("+self.abox1.text()+",  '"+self.abox2.text()+"');"
            cursor = connection.cursor()
            # cursor.execute(f"insert into glavnay (id_samokat, sostoynie, polzovatel, tarif, zarad) values (%s,%s,%s,%s,%s);", (int(self.abox1.toPlainText()), int(self.abox2.toPlainText()), int(self.abox3.toPlainText()), int(self.abox4.toPlainText()), int(self.abox5.toPlainText()))
            # records = cursor.fetchall()
            # print(len(records))
            cursor.execute(c)
            connection.commit()
            self.tableWidget.clear()
            connection.commit()

            cursor.execute(f"SELECT id_stoynka, adres FROM stoynka;")
            records = cursor.fetchall()
            print(len(records))
            for a in range(math.ceil(len(records) / 1) + 1):
                self.tableWidget.insertRow(a)
                if a > 0:
                    if a - 1 < len(records):
                        record_1 = records[a - 1]
                        for col_index, value in enumerate(record_1[:2]):
                            item_1 = QTableWidgetItem(str(value))
                            self.tableWidget.setItem(a, col_index, item_1)

                    # if a * 2 - 3 < len(records):
                    #     record_2 = records[a * 2 - 3]
                    #     for col_index, value in enumerate(record_2[1:6], start=6):
                    #         item_2 = QTableWidgetItem(str(value))
                    #         self.tableWidget.setItem(a, col_index, item_2)

            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.horizontalHeader().setVisible(False)

            # Добавление заголовков и объединение ячеек
            self.tableWidget.setSpan(0, 1, 0, 1)

            new_item = QTableWidgetItem("Номер стоянки")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("Адрес")
            self.tableWidget.setItem(0, 1, new_item)
            # new_item = QTableWidgetItem("Пользователь")
            # self.tableWidget.setItem(0, 2, new_item)
            # new_item = QTableWidgetItem("Тариф")
            # self.tableWidget.setItem(0, 3, new_item)
            # new_item = QTableWidgetItem("заряд")
            # self.tableWidget.setItem(0, 4, new_item)

            # Выравнивание столбцов по содержимому
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.itemChanged.connect(self.save_date)






        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Add_Note_Windowwww("f", "g")
    app.exec_()
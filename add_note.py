import math
import sys
from aifc import Error
from datetime import date

import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow, \
    QPlainTextEdit, QTableWidget, QTableWidgetItem
# from PyQt5.QtGui import QIcon
# from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from pathlib import Path

#from notes import Note_Window


class Add_Note_Window(QMainWindow):
    def __init__(self, email, name):
        super().__init__()
        self.email = email
        self.name = name
        self.today = date.today()
        self.date_format = self.today.strftime("%B %d, %Y")
        # window properties
        self.note_window = None

        self.setWindowTitle("История")
        self.resize(1400, 500)
        self.setStyleSheet("background-color: #ffffff;")


        # self.add_label = QLabel(self)
        # self.add_label.move(550, 30)
        # self.add_label.setText("сумма")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(550, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("сумма")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        #
        #
        # self.add_label = QLabel(self)
        # self.add_label.move(400, 30)
        # self.add_label.setText("Время")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(400, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Время")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        #
        #
        # self.add_label = QLabel(self)
        # self.add_label.move(250, 30)
        # self.add_label.setText("Самокат")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(250, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Самокат")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        #
        #
        # self.add_label = QLabel(self)
        # self.add_label.move(100, 30)
        # self.add_label.setText("Клиент")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(100, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Клиент")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()

        connection = None
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(25, 50, 590, 400)
        self.tableWidget.setColumnCount(7)
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            cursor = connection.cursor()
            cursor.execute(f"SELECT id_histori, polzovatel, data, samokat, tarif, interval, summa FROM histori;")
            records = cursor.fetchall()
            print(len(records))
            for a in range(math.ceil(len(records) / 1) + 1):
                self.tableWidget.insertRow(a)
                if a > 0:
                    if a - 1 < len(records):
                        record_1 = records[a - 1]
                        for col_index, value in enumerate(record_1[:7]):
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
            self.tableWidget.setSpan(0, 1, 0, 7)

            new_item = QTableWidgetItem("Номер аренды")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("Клиент")
            self.tableWidget.setItem(0, 1, new_item)
            new_item = QTableWidgetItem("Дата")
            self.tableWidget.setItem(0, 2, new_item)
            new_item = QTableWidgetItem("Самокат")
            self.tableWidget.setItem(0, 3, new_item)
            new_item = QTableWidgetItem("Тариф")
            self.tableWidget.setItem(0, 4, new_item)
            new_item = QTableWidgetItem("Время")
            self.tableWidget.setItem(0, 5, new_item)
            new_item = QTableWidgetItem("Сумма")
            self.tableWidget.setItem(0, 6, new_item)


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
        self.button_1.move(15, 450)
        self.button_1.resize(190, 40)
        self.button_1.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_1.clicked.connect(self.close)

        self.button_add = QPushButton("Добавить", self)
        self.button_add.move(825, 15)
        self.button_add.resize(190, 40)
        self.button_add.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_add.clicked.connect(self.dobavit)

        self.abox1 = QLineEdit(self)
        self.abox1.move(800, 75)
        self.abox1.resize(75, 25)

        self.abox2 = QLineEdit(self)
        self.abox2.move(875, 75)
        self.abox2.resize(75, 25)

        self.abox3 = QLineEdit(self)
        self.abox3.move(950, 75)
        self.abox3.resize(75, 25)

        self.abox4 = QLineEdit(self)
        self.abox4.move(1025, 75)
        self.abox4.resize(75, 25)

        self.abox5 = QLineEdit(self)
        self.abox5.move(1100, 75)
        self.abox5.resize(75, 25)

        self.abox6 = QLineEdit(self)
        self.abox6.move(1175, 75)
        self.abox6.resize(75, 25)

        self.abox7 = QLineEdit(self)
        self.abox7.move(1250, 75)
        self.abox7.resize(75, 25)


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
            c="insert into histori (id_histori, polzovatel, data, samokat, tarif, interval, summa) values ("+self.abox1.text()+",  "+self.abox2.text()+", '"+self.abox3.text()+"', "+self.abox4.text()+", "+self.abox5.text()+", "+self.abox6.text()+", "+self.abox7.text()+");"
            cursor = connection.cursor()
            # cursor.execute(f"insert into glavnay (id_samokat, sostoynie, polzovatel, tarif, zarad) values (%s,%s,%s,%s,%s);", (int(self.abox1.toPlainText()), int(self.abox2.toPlainText()), int(self.abox3.toPlainText()), int(self.abox4.toPlainText()), int(self.abox5.toPlainText()))
            # records = cursor.fetchall()
            # print(len(records))
            cursor.execute(c)
            self.tableWidget.clear()
            connection.commit()

            cursor.execute(f"SELECT id_histori, polzovatel, data, samokat, tarif, interval, summa FROM histori;")
            records = cursor.fetchall()
            print(len(records))
            for a in range(math.ceil(len(records) / 1) + 1):
                self.tableWidget.insertRow(a)
                if a > 0:
                    if a - 1 < len(records):
                        record_1 = records[a - 1]
                        for col_index, value in enumerate(record_1[:7]):
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
            self.tableWidget.setSpan(0, 1, 0, 6)

            new_item = QTableWidgetItem("Номер истории")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("Пользователь")
            self.tableWidget.setItem(0, 1, new_item)
            new_item = QTableWidgetItem("дата")
            self.tableWidget.setItem(0, 2, new_item)
            new_item = QTableWidgetItem("Самокат")
            self.tableWidget.setItem(0, 3, new_item)
            new_item = QTableWidgetItem("Тариф")
            self.tableWidget.setItem(0, 4, new_item)
            new_item = QTableWidgetItem("Время проката")
            self.tableWidget.setItem(0, 5, new_item)
            new_item = QTableWidgetItem("Сумма")
            self.tableWidget.setItem(0, 6, new_item)

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
    gui = Add_Note_Window("f", "g")
    app.exec_()


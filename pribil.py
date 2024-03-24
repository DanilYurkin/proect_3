import math
import sys
from aifc import Error
from datetime import date

import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow, \
    QPlainTextEdit, QTableWidgetItem, QTableWidget
# from PyQt5.QtGui import QIcon
# from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from pathlib import Path

#from notes import Note_Window


class Add_Note_Windowww(QMainWindow):
    def __init__(self, email, name):
        super().__init__()
        self.email = email
        self.name = name
        self.today = date.today()
        self.date_format = self.today.strftime("%B %d, %Y")
        # window properties
        self.note_window = None

        self.setWindowTitle("Прибыль")
        self.resize(1000, 500)
        self.setStyleSheet("background-color: #ffffff;")


        # self.add_label = QLabel(self)
        # self.add_label.move(100, 30)
        # self.add_label.setText("Прибыль")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(100, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Прибыль")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()
        #
        #
        # self.add_label = QLabel(self)
        # self.add_label.move(250, 30)
        # self.add_label.setText("Промежуток времени")
        # self.add_label.setStyleSheet("font-size:24px")
        #
        # self.text_input = QPlainTextEdit(self)
        # self.text_input.move(250, 80)
        # self.text_input.resize(100, 300)
        # self.text_input.setPlaceholderText("Промежуток времени")
        # self.text_input.setStyleSheet(
        #     "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:16px;")
        # self.text_input.setFocus()

        connection = None
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(250, 50, 490, 400)
        self.tableWidget.setColumnCount(2)
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            cursor = connection.cursor()
            cursor.execute(f"SELECT SUM(histori.summa) AS total_summ FROM histori where data >= date_trunc('month', current_date) and data < date_trunc('month', current_date)+interval '1 month';")
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

            new_item = QTableWidgetItem("Прибыль")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("За месяц")
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
        self.button_1.move(15, 450)
        self.button_1.resize(190, 40)
        self.button_1.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_1.clicked.connect(self.close)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Add_Note_Windowww("f", "g")
    app.exec_()

import os
from aifc import Error
from pathlib import Path

import psycopg2
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QPlainTextEdit, QTableWidgetItem, QTableWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
import sys
import psycopg2
import requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math

from add_note import Add_Note_Window
from Klient import Add_Note_Windoww
from pribil import Add_Note_Windowww
from stoinki import Add_Note_Windowwww


class Note_Window(QMainWindow):
    def __init__(self, email, name):
        super().__init__()
        self.email = email
        self.name = name
        self.notes_text = ""
        self.add_note_window = None
        # get notes
        # if Path("notes.txt").exists():
        # with open(Path("notes.txt"), 'r') as self.read_file:
        # self.read_file_data = self.read_file.read().replace('\n', '')
        # self.file_data = self.read_file_data.split(';;;;')
        # self.file_data = self.file_data[:-1]
        # self.length = len(self.file_data)
        # for self.counter_one in self.file_data:
        # self.data_line_split = self.file_data[self.length-1].split(',,,,')
        # self.counter_one.split(',,,,')
        # self.notes_text = self.notes_text + self.data_line_split[0] + '\n' + self.data_line_split[1] + '\n\n\n'
        # self.length = self.length - 1
        # if self.read_file_data.strip() == "":
        # self.notes_text = "You have not created any notes"

        # else:
        # self.create_file = open("notes.txt", "w")
        # self.create_file.write("")
        # self.notes_text = "You have not created any notes"
        self.initUI()

    # set ui
    def initUI(self):
        self.setWindowTitle(self.name + "Главная страница")
        self.resize(1250, 500)
        self.setStyleSheet("background-color:#ffffff;")

        self.label = QLabel(self)
        self.label.setGeometry(30, 30, 500, 30)
        self.label.setText(self.name + "Главная страница")
        self.label.setStyleSheet("font-size:20px;")

        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(16, 60, 530, 560)
        self.scroll.setStyleSheet("border: 0.5px solid #ffffff;")
        self.widget = QWidget(self)
        self.vbox = QVBoxLayout()
        # self.vbox.setGeometry(550, 500)

        object = QtWidgets.QTextBrowser(self)
        object.setStyleSheet("background:#ffffff; border: 0px solid #fffff;font-size:16px; line-height:19px;")
        object.setStyleSheet("margin-right:25px;font-size:15px;")
        object.setText(self.notes_text)
        self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        # scroll area properties
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        # ------------------------------------------------------------------------------------------------------
        connection = None
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(250, 50, 490, 400)
        self.tableWidget.setColumnCount(5)
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost", 
                                          port="5433",
                                          database="prokat_samokat")
            cursor = connection.cursor()
            cursor.execute(f"SELECT id_samokat, sostoynie, polzovatel, tarif, zarad FROM glavnay;")
            records = cursor.fetchall()
            print(len(records))
            for a in range(math.ceil(len(records) / 1) + 1):
                self.tableWidget.insertRow(a)
                if a > 0:
                    if a - 1 < len(records):
                        record_1 = records[a - 1]
                        for col_index, value in enumerate(record_1[:5]):
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
            self.tableWidget.setSpan(0, 1, 0, 4)

            new_item = QTableWidgetItem("Номер самоката")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("Состояние")
            self.tableWidget.setItem(0, 1, new_item)
            new_item = QTableWidgetItem("Пользователь")
            self.tableWidget.setItem(0, 2, new_item)
            new_item = QTableWidgetItem("Тариф")
            self.tableWidget.setItem(0, 3, new_item)
            new_item = QTableWidgetItem("заряд")
            self.tableWidget.setItem(0, 4, new_item)


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

        self.button_add = QPushButton("История", self)
        self.button_add.move(30, 100)
        self.button_add.resize(190, 40)
        self.button_add.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_add.clicked.connect(self.add_note_action)

        self.button_refresh = QPushButton("Клиент", self)
        self.button_refresh.move(30, 150)
        self.button_refresh.resize(190, 40)
        self.button_refresh.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_refresh.clicked.connect(self.ref_window)

        self.button_refresh = QPushButton("Прибыль", self)
        self.button_refresh.move(30, 200)
        self.button_refresh.resize(190, 40)
        self.button_refresh.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_refresh.clicked.connect(self.pribill)

        self.button_refresh = QPushButton("Стоянки", self)
        self.button_refresh.move(30, 250)
        self.button_refresh.resize(190, 40)
        self.button_refresh.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_refresh.clicked.connect(self.stoinkii)

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

        self.abox3 = QLineEdit(self)
        self.abox3.move(950, 75)
        self.abox3.resize(75, 25)

        self.abox4 = QLineEdit(self)
        self.abox4.move(1025, 75)
        self.abox4.resize(75, 25)

        self.abox5 = QLineEdit(self)
        self.abox5.move(1100, 75)
        self.abox5.resize(75, 25)



        self.show()

    def save_date(self,item):
        row=item.row()
        col=item.column()
        value=item.text()
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            if item is not None and item.text() is not None:
                cursor = connection.cursor()
                self.header_item = self.tableWidget.horizontalHeaderItem(col)
                update_sql=f"UPDATE glavnay set {self.header_item.text()}=%s WHERE id=%s"
                cursor.execute(update_sql, (value,self.tableWidget.item(row,0).text()))
                connection.commit()
            #safe = cursor.fetchall()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")


    def add_note_action(self):
        self.add_note_window = Add_Note_Window(self.email, self.name)
        self.add_note_window.show()

    def ref_window(self):
        # close old window and open a new window
        self.Klient = Add_Note_Windoww(self.email, self.name)
        # self.ref_window = Note_Window(self.email, self.name)
        self.Klient.show()

    def pribill(self):
        self.pribil = Add_Note_Windowww(self.email, self.name)
        self.pribil.show()

    def stoinkii(self):
        self.stoinki = Add_Note_Windowwww(self.email, self.name)
        self.stoinki.show()

    def dobavit(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            c="insert into glavnay (id_samokat, sostoynie, polzovatel, tarif, zarad) values ("+self.abox1.text()+",  "+self.abox2.text()+", "+self.abox3.text()+", "+self.abox4.text()+", "+self.abox5.text()+");"
            cursor = connection.cursor()
            # cursor.execute(f"insert into glavnay (id_samokat, sostoynie, polzovatel, tarif, zarad) values (%s,%s,%s,%s,%s);", (int(self.abox1.toPlainText()), int(self.abox2.toPlainText()), int(self.abox3.toPlainText()), int(self.abox4.toPlainText()), int(self.abox5.toPlainText()))
            # records = cursor.fetchall()
            # print(len(records))
            cursor.execute(c)
            self.tableWidget.clear()
            # for i in range(self.tableWidget.rowCount()):
            #     self.tableWidget.removeRow(i)
            connection.commit()
            #
            cursor.execute(f"SELECT id_samokat, sostoynie, polzovatel, tarif, zarad FROM glavnay;")
            records = cursor.fetchall()
            print(len(records))
            for a in range(math.ceil(len(records) / 1) + 1):
                self.tableWidget.insertRow(a)
                if a > 0:
                    if a - 1 < len(records):
                        record_1 = records[a - 1]
                        for col_index, value in enumerate(record_1[:5]):
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
            self.tableWidget.setSpan(0, 1, 0, 4)

            new_item = QTableWidgetItem("Номер самоката")
            self.tableWidget.setItem(0, 0, new_item)
            new_item = QTableWidgetItem("Состояние")
            self.tableWidget.setItem(0, 1, new_item)
            new_item = QTableWidgetItem("Пользователь")
            self.tableWidget.setItem(0, 2, new_item)
            new_item = QTableWidgetItem("Тариф")
            self.tableWidget.setItem(0, 3, new_item)
            new_item = QTableWidgetItem("заряд")
            self.tableWidget.setItem(0, 4, new_item)

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
    window = Note_Window("","")
    window.show()
    app.exec_()



import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.uic.properties import QtWidgets, QtCore, QtGui
from pathlib import Path
from notes import Note_Window
from signup import Signup_Window
from forgot_password import Forgo_Pass_Window
import psycopg2

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.new_signup_window = None
        self.new_forgo_pass_window = None
        self.note_window = None

        # window properties
        self.setWindowTitle("Вход")
        self.resize(710, 632)
        self.setStyleSheet("background-color:#ffffff;")

        self.login_label = QLabel(self)
        self.login_label.move(100, 100)
        self.login_label.setText("Вход")
        self.login_label.setStyleSheet("font-size:24px")

        self.email_input = QLineEdit(self)
        self.email_input.move(100, 170)
        self.email_input.resize(260, 45)
        self.email_input.setPlaceholderText("id_администратора")
        self.email_input.setStyleSheet(
            "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:18px;")
        self.email_input.setFocus()

        self.password_input = QLineEdit(self)
        self.password_input.move(100, 250)
        self.password_input.resize(260, 45)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet(
            "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:18px;")
        self.password_input.setFocus()

        self.button_1 = QPushButton("Войти", self)
        self.button_1.move(100, 330)
        self.button_1.resize(190, 40)
        self.button_1.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff; border-radius:3px;")
        self.button_1.clicked.connect(self.authenticate)

        self.button_2 = QPushButton("Зарегестрироваться", self)
        self.button_2.move(360, 330)
        self.button_2.resize(190, 40)
        self.button_2.setStyleSheet("background:#008b8b; font-size:19px;color:#ffffff; border-radius:3px;")
        self.button_2.clicked.connect(self.create_signup_window)

        # self.button_3 = QPushButton("Forgot Password", self)
        # self.button_3.move(100, 410)
        # self.button_3.resize(190, 40)
        # self.button_3.setStyleSheet("background:#008b8b; font-size:19px;color:#ffffff; border-radius:3px;")
        # self.button_3.clicked.connect(self.create_forgot_password_window)

        self.alert_message = QMessageBox()

        self.email_input_value = ""
        self.password_input_value = ""

    def create_signup_window(self):
        self.new_signup_window = Signup_Window()
        self.new_signup_window.show()

    def create_forgot_password_window(self):
        self.new_forgo_pass_window = Forgo_Pass_Window()
        self.new_forgo_pass_window.show()

    def authenticate(self):
        username = self.email_input.text()
        password = self.password_input.text()

        try:
            # Establish a connection to the PostgreSQL database
            self.connection = psycopg2.connect(
                                                user="postgres",
                                                password="0000",
                                                host="localhost",
                                                port="5433",
                                                database="prokat_samokat"
                                            )

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM profil WHERE id_profil=%s AND porol=%s", (username, password))
            user_data = cursor.fetchone()

            if user_data:
                # Authentication successful
                self.close()
                self.note_window = Note_Window(username,password)
                self.note_window.show()
            else:
                # Authentication failed
                QMessageBox.warning(self, 'Error', 'Incorrect login or password.')
        except Exception as error:
            # Handle database connection errors
            QMessageBox.critical(self, 'Error', f'Error connecting to the database: {error}')
        finally:
        # Close the database connection
            if self.connection:
                self.connection.close()

    # def login_action(self):
    #     email_input_value = self.email_input.text()
    #     password_input_value = self.password_input.text()
    #
    #     try:
    #         conn = psycopg2.connect(user="postgres",
    #                                 password="0000",
    #                                 host="localhost",
    #                                 port="5433",
    #                                 database="prokat_samokat")
    #         cursor = conn.cursor()
    #
    #         cursor.execute("SELECT * FROM profil WHERE id_profil = %s AND porol=%s", (email_input_value, password_input_value))
    #         user_data = cursor.fetchone()
    #
    #         if user_data:
    #             stored_email, stored_password = user_data
    #             if stored_password == self.password_input_value:
    #                 self.authentication_error = False
    #                 self.user_email = stored_email
    #                 #self.user_name = stored_name
    #             else:
    #                 self.authentication_error = True
    #         else:
    #             self.authentication_error = True
    #
    #     except psycopg2.Error as e:
    #         print("Error connecting to PostgreSQL database:", e)
    #         self.authentication_error = True
    #
    #     finally:
    #         if conn:
    #             cursor.close()
    #             conn.close()
    #
    #     if not self.authentication_error:
    #         self.alert_message.setText("Welcome " + self.user_name)
    #         self.alert_message.setWindowTitle("Success")
    #         self.close()
    #         self.note_window = Note_Window(self.user_email, self.user_name)
    #         self.note_window.show()
    #     else:
    #         self.alert_message.setText("Incorrect email or password. Please try again.")
    #         self.alert_message.setWindowTitle("Error")
    #         self.alert_message.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Window()
    gui.show()
    app.exec_()

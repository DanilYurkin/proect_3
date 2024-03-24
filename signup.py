import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow
import psycopg2

class Signup_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # window properties
        self.setWindowTitle("Регистрация")
        self.resize(610, 532)
        self.setStyleSheet("background-color: #ffffff")

        self.signup_label = QLabel(self)
        self.signup_label.move(100, 70)
        self.signup_label.setText("Регистрация")
        self.signup_label.setStyleSheet("font-size:24px")

        # email and password input
        self.email_input = QLineEdit(self)
        self.email_input.move(100, 140)
        self.email_input.resize(260, 45)
        self.email_input.setPlaceholderText("Логин")
        self.email_input.setStyleSheet(
            "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:18px;")
        self.email_input.setFocus()

        self.password_input = QLineEdit(self)
        self.password_input.move(100, 300)
        self.password_input.resize(260, 45)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet(
            "background:#ffffff; border:1px solid #a9a9a9;border-radius:3px;font-size:18px;")
        self.password_input.setFocus()

        self.button_1 = QPushButton("Регистрация", self)
        self.button_1.move(100, 370)
        self.button_1.resize(190, 40)
        self.button_1.setStyleSheet("background:#008b8b; font-size:19px; color:#ffffff;border-radius:3px;")
        self.button_1.clicked.connect(self.create_account)

        # alert message box
        self.alert_message = QMessageBox()

    def create_account(self):
        # get input values
        email_input_value = self.email_input.text()
        int(email_input_value)
        password_input_value = self.password_input.text()

        # connect to the database
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="0000",
                                          host="localhost",
                                          port="5433",
                                          database="prokat_samokat")
            cursor = connection.cursor()

            # execute the SQL query
            sql_amd="INSERT INTO admin(id_admin) VALUES (%s)"
            cursor.execute(sql_amd, (email_input_value,))
            connection.commit()
            sql="INSERT INTO profil(id_profil,porol) VALUES (%s,%s)"
            cursor.execute(sql, (email_input_value, password_input_value,))
            connection.commit()

            # if user_data:
            #     # successful authentication
            #     self.alert_message.setText("Добро пожаловать, " + user_data[2] + "!")
            #     self.alert_message.setWindowTitle("Успешная аутентификация")
            # else:
            #     # authentication failed
            #     self.alert_message.setText("Логин или пароль введены неверно.")
            #     self.alert_message.setWindowTitle("Ошибка аутентификации")
            #
            # # close the database connection
            # cursor.close()
            # connection.close()

        except Exception as error:
            self.alert_message.setText("Ошибка при подключении к БД: " + str(error))
            self.alert_message.setWindowTitle("Ошибка подключения к БД")

        self.alert_message.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Signup_Window()
    window.show()
    app.exec_()


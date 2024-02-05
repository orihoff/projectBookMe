from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QTabBar, QGridLayout,
    QComboBox, QHBoxLayout, QDialog, QMessageBox, QSpacerItem, QSizePolicy, QCheckBox, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QBrush, QIcon
from PyQt5.QtCore import Qt, QDateTime
import socket
import json
import sys
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListWidget

class ClientUI(QMainWindow):
    def __init__(self):
        super(ClientUI, self).__init__()
        
        self.server_address = ('localhost', 5000)

        self.setWindowTitle("BookMe")
        self.setGeometry(550, 100, 800, 550)

        # Central widget and notebook
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.notebook = QTabWidget(self.central_widget)

        # Tabs
        self.login_tab = QWidget()
        self.notebook.addTab(self.login_tab, "Login")
        self.register_tab = QWidget()
        self.notebook.addTab(self.register_tab, "Register")
        self.main_tab = QWidget()
        self.notebook.addTab(self.main_tab, "Main Page")
        self.buy_book_page = QWidget()
        self.notebook.addTab(self.buy_book_page, "Buy book Page")
        self.sell_book_page = QWidget()
        self.notebook.addTab(self.sell_book_page, "Sell book Page")
        

        # Main window
        self.main_window = QMainWindow(self)
        self.main_window.hide()

        # Setup tabs
        self.setup_login_tab()
        self.setup_register_tab()
        self.setup_main_tab()
        self.setup_buy_book_page()
        self.setup_sell_book_page()


        # Overall layout
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.notebook)

        # Set background color and image for all tabs
        background_image_path = 'background.png'
        self.set_all_background_color(QColor(0, 200, 255), background_image_path)

        # Hide tab bar
        self.notebook.tabBar().hide()

    def set_background_color(self, element, color, background_image=None):
        element.setAutoFillBackground(True)
        palette = element.palette()
        palette.setColor(QPalette.Window, color)

        # Set background image if provided
        if background_image:
            palette.setBrush(QPalette.Window, QBrush(QPixmap(background_image)))

        element.setPalette(palette)


    def set_all_background_color(self, color, background_image=None):
        self.set_background_color(self.central_widget, color, background_image)
        self.set_background_color(self.login_tab, color, background_image)
        self.set_background_color(self.register_tab, color, background_image)
        self.set_background_color(self.main_tab, color, background_image)
        self.set_background_color(self.buy_book_page, color, background_image)
        self.set_background_color(self.sell_book_page, color, background_image)


        self.set_sizes()

    def show_pages(self):
        num_pages = self.notebook.count()

        if num_pages > 0:
            print("Existing pages:")
            for i in range(num_pages):
                page_name = self.notebook.tabText(i)
                print(f"Page {i + 1}: {page_name}")
        else:
            print("No pages found.")

    def set_sizes(self):
        # Login Tab
        self.login_button.setFixedHeight(39)
        self.login_button.setFixedWidth(130)
        self.login_username_entry.setFixedHeight(35)
        self.login_username_entry.setFixedWidth(220)
        self.login_password_entry.setFixedHeight(35)
        self.login_password_entry.setFixedWidth(220)

        # Register Tab
        self.register_button.setFixedHeight(39)
        self.register_button.setFixedWidth(130)
        self.register_username_entry.setFixedHeight(35)
        self.register_username_entry.setFixedWidth(220)
        self.register_city_combobox.setFixedHeight(35)
        self.register_city_combobox.setFixedWidth(220)
        self.register_email_entry.setFixedHeight(35)
        self.register_email_entry.setFixedWidth(220)
        self.register_phone_entry.setFixedHeight(35)
        self.register_phone_entry.setFixedWidth(220)
        self.register_password_entry.setFixedHeight(34)
        self.register_password_entry.setFixedWidth(220)
        self.register_confirm_password_entry.setFixedHeight(34)
        self.register_confirm_password_entry.setFixedWidth(220)

        # Main Tab
        self.buy_button.setFixedHeight(35)
        self.buy_button.setFixedWidth(120)
        self.sell_button.setFixedHeight(35)
        self.sell_button.setFixedWidth(120)

        #sell book page
        self.book_name_entry.setFixedHeight(34)
        self.book_name_entry.setFixedWidth(220)
        

    def set_window_height(self):
        logo_height = 500  # גובה הלוגו (שנקבע על ידי המספר המתאים)
        self.setFixedHeight(logo_height + self.notebook.height() + self.notebook.tabBar().height())
        self.notebook.setCurrentIndex(0)  # בכדי להראות את העמוד הרלוונטי בתחילה


    
        
    def setup_login_tab(self):
        # Create main label
        self.login_label = QLabel(" Login  ", self.login_tab)
        self.login_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.login_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Load logo for login page
        logo_label = QLabel(self.login_tab)
        pixmap_login = QPixmap('logo.png')
        pixmap_login = pixmap_login.scaledToHeight(300, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap_login)
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the top-center

        self.login_username_entry = QLineEdit(self.login_tab)
        self.login_username_entry.setPlaceholderText("Username")
        self.login_username_entry.setStyleSheet("border: 1px solid blue; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Password
        self.login_password_entry = QLineEdit(self.login_tab)
        self.login_password_entry.setEchoMode(QLineEdit.Password)
        self.login_password_entry.setPlaceholderText("Password")
        self.login_password_entry.setStyleSheet("border: 1px solid blue; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Login button
        self.login_button = QPushButton("Login", self.login_tab)
        self.login_button.setStyleSheet(
            "background-color: #07a310; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;")
        self.login_button.clicked.connect(self.login)

        # Forgot Password? button
        forgot_password_button = QPushButton("Forget Password?", self.login_tab)
        forgot_password_button.setStyleSheet(
            "color: blue; border: none; text-decoration: underline; background-color: transparent; text-align: center; font-size: 16px;")
        forgot_password_button.setFont(QFont("Arial", 12, QFont.Bold))
        forgot_password_button.clicked.connect(self.show_forgot_password_window)

        # Remove the close button on the Login tab
        self.notebook.tabBar().setTabButton(0, QTabBar.LeftSide, None)

        # Error message
        self.login_error_label = QLabel("                        ", self.login_tab)
        self.login_error_label.setStyleSheet("font-weight: bold;")

        # Layouts
        main_layout = QHBoxLayout(self.login_tab)

        # Left side (logo)
        left_layout = QVBoxLayout()
        left_layout.addWidget(logo_label, alignment=Qt.AlignCenter)  # Align the logo to the top-center

        # Right side (form)
        right_layout = QVBoxLayout()

        # Set the login label alignment to be in the middle
        self.login_label.setAlignment(Qt.AlignHCenter)

        # Add the login label to the top with extra space on the bottom
        right_layout.addWidget(self.login_label)
        right_layout.addStretch()  # Add stretch to push elements to the top

        # Add the username, password, login button, and error label with center alignment
        right_layout.addWidget(self.login_username_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(10)  # Adjust the spacing value as needed
        right_layout.addWidget(self.login_password_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(10)  # Adjust the spacing value as needed
        right_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        right_layout.addSpacing(10)  # Adjust the spacing value as needed
        right_layout.addWidget(forgot_password_button, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.login_error_label, alignment=Qt.AlignCenter)

        # Add spacing between the login button and the "Don’t have an account?" label
        right_layout.addSpacing(60)  # Adjust the spacing value as needed

        # Add the "Don’t have an account?" label and Register button to the right layout
        switch_to_register_label = QLabel("Don’t have an account?   ", self.login_tab)
        switch_to_register_label.setStyleSheet("color: black; border: none; text-align: center; font-size: 17px;")  # Align center

        switch_to_register_button = QPushButton("Register", self.login_tab)
        switch_to_register_button.setStyleSheet(
            "color: black; border: none; text-decoration: underline; background-color: transparent; text-align: center;")
        switch_to_register_button.setFont(QFont("Arial", 9, QFont.Bold))
        switch_to_register_button.clicked.connect(self.show_registration_window)
        switch_to_register_button.setFixedWidth(120)

        right_layout.addWidget(switch_to_register_label, alignment=Qt.AlignCenter)  # Align center
        right_layout.addWidget(switch_to_register_button, alignment=Qt.AlignCenter)  # Align center
        right_layout.addStretch()  # Add stretch to push elements to the top

        # Add the left and right layouts to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Add the main layout to the main window
        self.login_tab.setLayout(main_layout)

        # Remove the close button on the Login tab
        self.notebook.tabBar().setTabButton(0, QTabBar.LeftSide, None)

    def setup_forgot_password_tab(self):
        self.forgot_password_tab = QWidget()
        self.notebook.addTab(self.forgot_password_tab, "Forgot Password")

        # Create main label
        forgot_password_label = QLabel(" Forgot Password  ", self.forgot_password_tab)
        forgot_password_label.setFont(QFont("Arial", 24, QFont.Bold))
        forgot_password_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Email entry
        self.forgot_password_email_entry = QLineEdit(self.forgot_password_tab)
        self.forgot_password_email_entry.setPlaceholderText("Enter your email")
        self.forgot_password_email_entry.setStyleSheet(
            "border: 1px solid blue; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Request Code button
        request_code_button = QPushButton("Request Code", self.forgot_password_tab)
        request_code_button.setStyleSheet(
            "background-color: blue; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;")
        request_code_button.clicked.connect(self.request_reset_code)

        # Code entry
        self.reset_code_entry = QLineEdit(self.forgot_password_tab)
        self.reset_code_entry.setPlaceholderText("Enter the code")
        self.reset_code_entry.setStyleSheet(
            "border: 1px solid blue; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Reset Password button
        reset_password_button = QPushButton("Reset Password", self.forgot_password_tab)
        reset_password_button.setStyleSheet(
            "background-color: blue; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;")
        reset_password_button.clicked.connect(self.reset_password)

        # Layouts
        main_layout = QVBoxLayout(self.forgot_password_tab)

        main_layout.addWidget(forgot_password_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.forgot_password_email_entry, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(request_code_button, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.reset_code_entry, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(reset_password_button, alignment=Qt.AlignCenter)

        self.forgot_password_tab.setLayout(main_layout)

    def request_reset_code(self):
        print("this is all the pages", self.show_pages())
        email = self.forgot_password_email_entry.text()
        # Validate email
        if not email:
            QMessageBox.warning(self, "Error", "Please enter your email.", QMessageBox.Ok)
            return

        data = {
            'request_reset_code': True,
            'email': email
        }

        print(f"Sending request for reset code. Data: {data}")
        response = self.send_request(data)
        print(f"Received response: {response}")

        message = response['message']
        if message == 'Code sent successfully.':
            QMessageBox.information(self, "Code Sent", "A reset code has been sent to your email.", QMessageBox.Ok)
            return True
        else:
            QMessageBox.warning(self, "Error", f"Failed to send reset code. Error: {message}", QMessageBox.Ok)
            return False

   

    def reset_password(self):
        code = self.reset_code_entry.text()
        print("the code is ", code)
        # Additional validation if needed
        if not code:
            QMessageBox.warning(self, "Error", "Please enter the reset code.", QMessageBox.Ok)
            return
        print("there is a code")
        # Validate the code (replace with your actual validation logic)
        
        if not self.validate_reset_code(code):
            print(4)
            QMessageBox.warning(self, "Error", "Invalid reset code.", QMessageBox.Ok)
            return
        else:
            print("there is a valid code")
            self.show_change_password_window()

            print("Code verification successful!") 



    def setup_change_password_tab(self):
        # Change Password tab
        self.change_password_tab = QWidget()
        self.notebook.addTab(self.change_password_tab, "Change Password")

        # Create main label
        change_password_label = QLabel(" Change Password  ", self.change_password_tab)
        change_password_label.setFont(QFont("Arial", 24, QFont.Bold))
        change_password_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # New Password entry
        self.new_password_entry = QLineEdit(self.change_password_tab)
        self.new_password_entry.setPlaceholderText("Enter your new password")
        self.new_password_entry.setStyleSheet(
            "border: 1px solid blue; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Confirm Password entry
        self.confirm_password_entry = QLineEdit(self.change_password_tab)
        self.confirm_password_entry.setPlaceholderText("Confirm your new password")
        self.confirm_password_entry.setStyleSheet(
            "border: 1px solid blue; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Change Password button
        change_password_button = QPushButton("Change Password", self.change_password_tab)
        change_password_button.setStyleSheet(
            "background-color: blue; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;")
        change_password_button.clicked.connect(self.verify_and_change_password)  # Connect to the new function

        # Layouts
        main_layout = QVBoxLayout(self.change_password_tab)

        main_layout.addWidget(change_password_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.new_password_entry, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.confirm_password_entry, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(change_password_button, alignment=Qt.AlignCenter)

        self.change_password_tab.setLayout(main_layout)

    

    def validate_reset_code(self, code):
        data = {
            'verify_reset_code': True,
            'code': code,
            
            
        }
        print("Data being sent:", data)

        response = self.send_request(data)
        print("validate_reset_code response:", response)  # הוסף הדפסה כאן
        return response['match']

    def verify_and_change_password(self):
        # Send request to server to validate the code
        email = self.forgot_password_email_entry.text()
        code = self.reset_code_entry.text()
        new_password = self.new_password_entry.text()
        
        # Validate email and code
        if not email or not code:
            QMessageBox.warning(self, "Error", "Please enter both email and code.", QMessageBox.Ok)
            return

        change_password_data = {
            'reset_password': True,
            'email': email,
            'code': code,
            'new_password': new_password
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(self.server_address)
                client_socket.send(json.dumps(change_password_data).encode('utf-8'))
                
                # Receive response from the server
                response = b''
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    response += chunk

                response_text = response.decode('utf-8')
                print(f"Server response (text): {response_text}")

                try:
                    change_password_response = json.loads(response_text)
                    print("verify_and_change_password response:", change_password_response)

                    if change_password_response and isinstance(change_password_response, dict) and 'match' in change_password_response:
                        if change_password_response['match']:
                            QMessageBox.information(self, "Success", "Password changed successfully.", QMessageBox.Ok)
                            self.notebook.setCurrentIndex(0)  # Switch to the Login tab
                        else:
                            QMessageBox.warning(self, "Error", "Invalid reset code.", QMessageBox.Ok)
                    else:
                        QMessageBox.warning(self, "Error", "Invalid response from server.", QMessageBox.Ok)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON response: {e}")
                    QMessageBox.warning(self, "Error", "Invalid JSON response from server.", QMessageBox.Ok)

        except Exception as e:
            print(f"Error sending request to server: {e}")
            QMessageBox.warning(self, "Error", "Failed to connect to the server.", QMessageBox.Ok)


    def change_password(self):
        new_password = self.new_password_entry.text()
        confirm_password = self.confirm_password_entry.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.", QMessageBox.Ok)
            return

        data = {
            'change_password': True,
            'new_password': new_password
        }

        print(f"Sending request to change password. Data: {data}")
        response = self.send_request(data)
        print(f"Received response: {response}")

        message = response['message']
        if message == 'Password changed successfully.':
            QMessageBox.information(self, "Success", "Password changed successfully.", QMessageBox.Ok)
            self.notebook.setCurrentIndex(0)  # Switch to the Login tab
        else:
            QMessageBox.warning(self, "Error", f"Failed to change password. Error: {message}", QMessageBox.Ok)

    def setup_register_tab(self):
        # Create main label
        self.register_label = QLabel("Register ", self.register_tab)
        self.register_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.register_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Load logo for login page
        logo_label = QLabel(self.register_tab)
        pixmap_login = QPixmap('logo.png')
        pixmap_login = pixmap_login.scaledToHeight(300, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap_login)
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the top-center

        # Username
        self.register_username_entry = QLineEdit(self.register_tab)
        self.register_username_entry.setPlaceholderText("Username")
        self.register_username_entry.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 16px;")

        # Email
        self.register_email_entry = QLineEdit(self.register_tab)
        self.register_email_entry.setPlaceholderText("Email")
        self.register_email_entry.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 16px;")

        # Phone
        self.register_phone_entry = QLineEdit(self.register_tab)
        self.register_phone_entry.setPlaceholderText("Phone")
        self.register_phone_entry.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 16px;")
        
        # City
        self.register_city_combobox = QComboBox(self.register_tab)
        self.register_city_combobox.addItems(
            ["Choose City", "Petah Tikva", "Givat Shmuel", "Or Yehuda", "Rishon LeZion", "Tel Aviv", "Ramat Gan"])
        self.register_city_combobox.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 16px;")
        
        # Password
        self.register_password_entry = QLineEdit(self.register_tab)
        self.register_password_entry.setEchoMode(QLineEdit.Password)
        self.register_password_entry.setPlaceholderText("Password")
        self.register_password_entry.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 16px;")

        # Confirm Password
        self.register_confirm_password_entry = QLineEdit(self.register_tab)
        self.register_confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.register_confirm_password_entry.setPlaceholderText("Confirm Password")
        self.register_confirm_password_entry.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 16px;")

        # Register button
        self.register_button = QPushButton("Register", self.register_tab)
        self.register_button.setStyleSheet(
            "background-color: #07a310; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;")
        self.register_button.clicked.connect(self.register)

        # Create an empty label with spaces for padding
        padding_label = QLabel("   ", self.register_tab)

        # Success message
        self.register_success_label = QLabel("                        ", self.register_tab)
        self.register_success_label.setStyleSheet("color: green; font-weight: bold;")
        
        # Layouts
        main_layout = QHBoxLayout(self.register_tab)

        # Left side (logo)
        left_layout = QVBoxLayout()
        left_layout.addWidget(logo_label, alignment=Qt.AlignCenter)  # Align the logo to the top-center

        # Right side (form)
        right_layout = QVBoxLayout()

        # Set the register label alignment to be in the middle
        self.register_label.setAlignment(Qt.AlignHCenter)

        # Add the register label to the top with extra space on the bottom
        right_layout.addWidget(self.register_label)
        right_layout.addStretch()  # Add stretch to push elements to the top

        # Add the username, city, phone, password, register button, and success label with center alignment
        right_layout.addWidget(self.register_username_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)  # Adjust the spacing value as needed
        right_layout.addWidget(self.register_email_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)  # Adjust the spacing value as needed
        right_layout.addWidget(self.register_phone_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)  # Adjust the spacing value as needed
        right_layout.addWidget(self.register_city_combobox, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)  # Adjust the spacing value as needed
        right_layout.addWidget(self.register_password_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)  # Adjust the spacing value as needed
        right_layout.addWidget(self.register_confirm_password_entry, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)  # Adjust the spacing value as needed
        right_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.register_success_label, alignment=Qt.AlignCenter)
        right_layout.addSpacing(5)
        # Add the "Already have an account?" label and Login button to the right layout
        switch_to_login_label = QLabel("Already have an account?", self.register_tab)
        switch_to_login_label.setStyleSheet("color: black; border: none; text-align: center; font-size: 17px;")  # Align center

        switch_to_login_button = QPushButton("Login", self.register_tab)
        switch_to_login_button.setStyleSheet(
            "color: black; border: none; text-decoration: underline; background-color: transparent; text-align: center;")
        switch_to_login_button.setFont(QFont("Arial", 9, QFont.Bold))
        switch_to_login_button.clicked.connect(self.show_login_window)
        switch_to_login_button.setFixedWidth(120)

        right_layout.addWidget(switch_to_login_label, alignment=Qt.AlignCenter)  # Align center
        right_layout.addWidget(switch_to_login_button, alignment=Qt.AlignCenter)  # Align center
        

        # Add the left and right layouts to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.set_window_height()

        # Add the main layout to the main window
        self.register_tab.setLayout(main_layout)

        # Remove the close button on the Register tab
        self.notebook.tabBar().setTabButton(1, QTabBar.LeftSide, None)



    def setup_main_tab(self):
        # Main tab layout
        layout = QVBoxLayout(self.main_tab)
        layout.setContentsMargins(35, 30, 35, 40)  

        # Welcome label
        welcome_label = QLabel(" Welcome to BookMe     ", self.main_tab)
        welcome_label.setFont(QFont("Times", 20, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(welcome_label)

        # Main buttons (Buy and Sell)
        buttons_layout = QHBoxLayout()

        # Buy button
        buy_button_layout = QVBoxLayout()
        buy_button_layout.setAlignment(Qt.AlignLeft)

        buy_image_label = QLabel(self.main_tab)
        buy_image_label.setPixmap(QPixmap('buy_image.png'))

        self.buy_button = QPushButton("Buy Book", self.main_tab)
        self.buy_button.setStyleSheet("background-color: #3498db; color: white; border: 2px solid #2980b9; padding: 45px 20px; border-radius: 5px;")
        self.buy_button.clicked.connect(self.show_buy_book_page)

        # Create a QHBoxLayout for the label and button
        label_button_layout = QHBoxLayout()

        # Add the image label
        buy_button_layout.addWidget(buy_image_label, alignment=Qt.AlignLeft)

        # Add the label and button layout
        label_button_layout.addWidget(QLabel("           ", self.main_tab), alignment=Qt.AlignLeft)
        label_button_layout.addWidget(self.buy_button, alignment=Qt.AlignLeft)
        label_button_layout.addStretch()

        # Add the label and button layout
        buy_button_layout.addLayout(label_button_layout)

        buttons_layout.addLayout(buy_button_layout)

        # Sell button
        sell_button_layout = QVBoxLayout()
        sell_button_layout.setAlignment(Qt.AlignCenter)
        sell_image_label = QLabel(self.main_tab)
        sell_image_label.setPixmap(QPixmap('sell_image.png'))

        self.sell_button = QPushButton("Sell Book", self.main_tab)
        self.sell_button.setStyleSheet("background-color: #e74c3c; color: white; border: 2px solid #c0392b; padding: 45px 20px; border-radius: 5px;")
        self.sell_button.clicked.connect(self.show_sell_book_page)

        sell_button_layout.addWidget(sell_image_label, alignment=Qt.AlignCenter)
        sell_button_layout.addWidget(self.sell_button, alignment=Qt.AlignCenter)
        buttons_layout.addLayout(sell_button_layout)

        layout.addLayout(buttons_layout)

        # Set layout for the Main tab
        self.main_tab.setLayout(layout)

        # Remove the close button on the Main tab
        self.notebook.tabBar().setTabButton(2, QTabBar.LeftSide, None)


    def setup_buy_book_page(self):
        buy_book_page = QWidget()
        layout = QVBoxLayout(buy_book_page)

        label = QLabel("Buy Books Page", buy_book_page)
        label.setFont(QFont("Times", 20, QFont.Bold))
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(label)

        # Add more components as needed for the "Buy Books" page

        # Example: Book search functionality
        search_label = QLabel("Search for a Book:", buy_book_page)
        search_entry = QLineEdit(buy_book_page)
        search_button = QPushButton("Search", buy_book_page)
        search_result_label = QLabel("", buy_book_page)

        # Connect the search button to a function (replace connect method with the actual function)
        # search_button.clicked.connect(##)

        # Example: List to display search results
        search_results_list = QListWidget(buy_book_page)

        # Add components to the layout
        layout.addWidget(search_label)
        layout.addWidget(search_entry)
        layout.addWidget(search_button)
        layout.addWidget(search_result_label)
        layout.addWidget(search_results_list)

        # Add the "Buy Books" page to the notebook
        self.notebook.addTab(buy_book_page, "Buy a Book")

    def setup_sell_book_page(self):
        self.sell_book_page = QWidget()  # Corrected to use self.sell_book_page

        layout = QVBoxLayout(self.sell_book_page)  # Corrected to use self.sell_book_page

        label = QLabel("Sell Books Page", self.sell_book_page)  # Corrected to use self.sell_book_page
        label.setFont(QFont("Times", 20, QFont.Bold))
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        layout.addWidget(label)

        # Book name
        self.book_name_entry = QLineEdit(self.sell_book_page)  # Corrected to use self.sell_book_page
        self.book_name_entry.setPlaceholderText("Book name")
        self.book_name_entry.setStyleSheet("border: 1px solid blue; background-color: white; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Author name
        self.author_name_entry = QLineEdit(self.sell_book_page)  # Corrected to use self.sell_book_page
        self.author_name_entry.setPlaceholderText("Author name")
        self.author_name_entry.setStyleSheet("border: 1px solid blue; background-color: white; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Class
        self.class_combobox = QComboBox(self.sell_book_page)  # Corrected to use self.sell_book_page
        self.class_combobox.addItems(["Choose Class", "'ז", "'ח", "'ט", "'י", "'יא", "'יב"])
        self.class_combobox.setStyleSheet("border: 1px solid blue; background-color: white; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Book status
        self.book_status_combobox = QComboBox(self.sell_book_page)  # Corrected to use self.sell_book_page
        self.book_status_combobox.addItems(["Book Status", "New", "Like New", "Used"])
        self.book_status_combobox.setStyleSheet("border: 1px solid blue; background-color: white; border-radius: 10px; padding: 5px; font-size: 16px;")

        # Upload image button
        self.upload_image_button = QPushButton("Upload Book Image", self.sell_book_page)  # Corrected to use self.sell_book_page
        self.upload_image_button.setStyleSheet("border: 1px solid blue; background-color: white; border-radius: 10px; padding: 5px; font-size: 16px;")
        self.upload_image_button.clicked.connect(self.upload_image)

        # File name label to display the selected file name
        self.file_name_label = QLabel("No file selected", self.sell_book_page)  # Corrected to use self.sell_book_page
        self.file_name_label.setAlignment(Qt.AlignCenter)
        self.file_name_label.setStyleSheet("font-size: 12px; color: gray;")  # Set initial style for the label

        # Indicator label for file upload
        self.upload_indicator_label = QLabel(self.sell_book_page)  # Corrected to use self.sell_book_page
        self.upload_indicator_label.setAlignment(Qt.AlignCenter)
        self.upload_indicator_label.setStyleSheet("font-size: 20px; color: red;")  # Set style for the indicator
        self.upload_indicator_label.setPixmap(QIcon.fromTheme("document-save").pixmap(QSize(24, 24)))  # Set the document-save icon
        self.upload_indicator_label.hide()

        # Put the book up for sale button
        self.up_for_sale_button = QPushButton("Put the book up for sale", self.sell_book_page)  # Corrected to use self.sell_book_page
        self.up_for_sale_button.setStyleSheet("border: 1px solid blue; background-color: white; border-radius: 10px; padding: 5px; font-size: 16px;")
        # self.up_for_sale_button.clicked.connect(##)

        # Error message
        self.register_error_label = QLabel("", self.sell_book_page)  # Corrected to use self.sell_book_page
        self.register_error_label.setStyleSheet("color: red; font-weight: bold;")  # Bold text

        

        # Add widgets to the layout
        layout.addWidget(self.book_name_entry, alignment=Qt.AlignCenter)
        layout.addWidget(self.author_name_entry, alignment=Qt.AlignCenter)
        layout.addWidget(self.class_combobox, alignment=Qt.AlignCenter)
        layout.addWidget(self.book_status_combobox, alignment=Qt.AlignCenter)
        layout.addWidget(self.upload_image_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.file_name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.upload_indicator_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.up_for_sale_button, alignment=Qt.AlignCenter)
        

        self.notebook.addTab(self.sell_book_page, "Sell a Book")

    # Function to handle image upload
    def upload_image(self):  
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload File", "", "Files (*.txt *.pdf *.docx)", options=options)
        
        if file_name:
            self.file_name_label.setText(f"Selected File: {file_name}")
            self.file_name_label.setStyleSheet("font-size: 12px; color: black;")  # Change style after selecting a file
            self.upload_indicator_label.show()
            print("Selected File:", file_name)
            
    def show_login_window(self):
        self.notebook.setCurrentIndex(0)

    def show_forgot_password_window(self):
        # Check if the forgot password tab is already created
        if not hasattr(self, 'forgot_password_tab'):
            self.setup_forgot_password_tab()

        # Switch to the Forgot Password tab
        self.notebook.setCurrentWidget(self.forgot_password_tab)
        
    def show_change_password_window(self):
        # Check if the change password tab is already created
        if not hasattr(self, 'change_password_tab'):
            self.setup_change_password_tab()

        # Switch to the Change Password tab
        self.notebook.setCurrentWidget(self.change_password_tab)

        
    def show_registration_window(self):
        self.notebook.setCurrentIndex(1)
        
    def show_buy_book_page(self):
        self.notebook.setCurrentIndex(3)

    def show_sell_book_page(self):
        self.notebook.setCurrentIndex(4)

    def login(self):
        username = self.login_username_entry.text()
        password = self.login_password_entry.text()

        data = {
            'login': True,
            'username': username,
            'password': password
        }

        response = self.send_request(data)
        message = response['message']

        if message == f'Hello, {username}!':
            self.login_error_label.clear()  # Clear previous error messages
            self.login_username_entry.clear()  # Clear the username field
            self.login_password_entry.clear()  # Clear the password field
            self.notebook.removeTab(0)  # Remove the Login tab
            self.notebook.removeTab(0)  # Remove the Register tab
            self.setup_main_tab()
        else:
            self.login_error_label.setText("Incorrect username or password.")
            self.login_error_label.setStyleSheet("color: red; font-weight: bold;")

    def is_valid_email(self, email):
        import re
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.match(email_regex, email))

    def is_strong_password(self, password):
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isupper() for c in password) and any(c.islower() for c in password)

    def register(self):
        username = self.register_username_entry.text()
        city = self.register_city_combobox.currentText()
        phone = self.register_phone_entry.text()
        email = self.register_email_entry.text()  
        password = self.register_password_entry.text()
        confirm_password = self.register_confirm_password_entry.text()  

        if not all([username, city != "Choose City", phone, email, password, confirm_password]):
            QMessageBox.warning(self, "Incomplete Information", "Please fill in all the required fields.", QMessageBox.Ok)
            return

        # Validating email format
        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.", QMessageBox.Ok)
            return

        # Checking for a strong password
        if not self.is_strong_password(password):
            QMessageBox.warning(self, "Weak Password", "Please choose a stronger password. Ensure it is at least 8 characters long, includes both letters and numbers, and contains both uppercase and lowercase letters.", QMessageBox.Ok)
            return

        # Checking if the password confirmation matches the entered password
        if password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", "Password and confirm password do not match.", QMessageBox.Ok)
            return

        data = {
            'register': True,
            'username': username,
            'city': city,
            'phone': phone,
            'email': email,
            'password': password
        }

        response = self.send_request(data)
        message = response['message']
        self.register_success()

        


        # Clear the input fields after successful registration
        self.clear_registration_fields()

    def clear_registration_fields(self):
        self.register_username_entry.clear()
        self.register_email_entry.clear()
        self.register_city_combobox.setCurrentIndex(0)
        self.register_phone_entry.clear()
        self.register_password_entry.clear()
        self.register_confirm_password_entry.clear()
        
    def send_request(self, data):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 5000))
        client.send(json.dumps(data).encode('utf-8'))
        response = client.recv(4096)
        client.close()
        return json.loads(response.decode('utf-8'))

    
    def login_success(self):
        self.login_error_label.clear()
        self.notebook.setCurrentIndex(2)

    def register_success(self):
        self.register_success_label.setText("Registration successful. You can now log in.")


        
if __name__ == '__main__':
    app = QApplication([])
    window = ClientUI()
    window.show()
    app.exec_()

    


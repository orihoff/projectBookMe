import sqlite3
import socket
import json
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

reset_code = ""

def create_database_if_not_exists():
    try:
        conn = sqlite3.connect('bookme.db')
        cursor = conn.cursor()

        # Check if the 'users' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone()

        if not table_exists:
            # Create the 'users' table if it doesn't exist
            cursor.execute('''CREATE TABLE users
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                city TEXT,
                                phone TEXT,
                                email TEXT,
                                password TEXT)''')
            conn.commit()

        print("Database is ready.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()

# Create the database if it doesn't exist
create_database_if_not_exists()

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096)

        if not request:
            return

        data = json.loads(request.decode('utf-8'))
        print("Received data:", data)

        if 'register' in data:
            register_user(data, client_socket)
        elif 'login' in data:
            login_user(data, client_socket)
        elif 'request_reset_code' in data:
            request_reset_code(data, client_socket)
        elif 'reset_password' in data:
            reset_password(data, client_socket)
        elif 'verify_reset_code' in data:
            verify_reset_code(data, client_socket)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def register_user(data, client_socket):
    try:
        username = data['username']
        city = data['city']
        phone = data['phone']
        email = data['email']
        password = data['password']

        conn = sqlite3.connect('bookme.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, city, phone, email, password) VALUES (?, ?, ?, ?, ?)",
                       (username, city, phone, email, password))

        conn.commit()
        conn.close()

        response = {'message': 'Registration Successful!'}
        client_socket.send(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print(f"Error registering user: {e}")

def login_user(data, client_socket):
    try:
        username = data['username']
        password = data['password']

        conn = sqlite3.connect('bookme.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:
            response = {'message': f'Hello, {username}!'}
        else:
            response = {'message': 'Login Failed'}

        client_socket.send(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print(f"Error logging in user: {e}")

def request_reset_code(data, client_socket):
    global reset_code
    try:
        email = data['email']
        reset_code = str(random.randint(100000, 999999))

        sender_email = "bookme2.email@gmail.com"
        app_password = "fcmg qytj smdw jezv"
        subject = "Password Reset Code"
        body = f"Your password reset code is: {reset_code}"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, email, message.as_string())

            print(f"Reset code sent to {email}. Check your email.")
            response = {'message': 'Code sent successfully.'}
        except Exception as e:
            print(f"Error sending email: {e}")
            response = {'message': f'Failed to send reset code. Error: {str(e)}'}

        client_socket.send(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print(f"Error requesting reset code: {e}")

def verify_reset_code(data, client_socket):
    print("the code ", data['code'])
    print("the real code ", reset_code)
    verification_result = data['code'] == reset_code
    print(f"Verification result: {verification_result}")
    response = {'match': verification_result}
    client_socket.send(json.dumps(response).encode('utf-8'))

def reset_password(data, client_socket):
    try:
        email = data['email']
        code = data['code']

        # Verify the reset code
        verification_result = verify_reset_code(data, client_socket)

        if verification_result['match']:
            # Fetch the new password only after code validation
            new_password = data['new_password']

            # Reset the password (replace with your password reset logic)
            response = reset_password_in_database(email, new_password)
            client_socket.send(json.dumps(response).encode('utf-8'))
        else:
            response = {'success': False, 'message': 'Invalid reset code.'}
            client_socket.send(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print(f"Error resetting password: {e}")

def reset_password_in_database(email, new_password):
    try:
        conn = sqlite3.connect('bookme.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            # Reset the password
            cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            conn.commit()

            response = {'success': True, 'message': 'Password reset successful.'}
        else:
            response = {'success': False, 'message': 'User does not exist.'}

    except Exception as e:
        print(f"Error resetting password in database: {e}")
        response = {'success': False, 'message': 'Failed to reset password. Internal server error.'}

    finally:
        conn.close()

    return response

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(5)

    print("Server is listening...")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == '__main__':
    run_server()

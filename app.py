import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import os
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pickle

# Initialize Flask app
flask_app = Flask(__name__)

# Load shop names from a .txt file
def load_shops(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        shops = [line.strip() for line in file if line.strip()]
    return shops

# Load shop names from your uploaded file
shops = load_shops(r'O:\Whatsapp_Automation\userdata\name.txt')

@flask_app.route("/")
def home():
    # Render the HTML file located in the templates folder
    return render_template("index.html", shops=shops)

# Function to send message to a WhatsApp group
def send_message(driver, group_name, message):
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        search_box.clear()
        search_box.send_keys(group_name)

        first_result = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{group_name}']"))
        )
        first_result.click()
    except Exception as e:
        print(f"Error finding or clicking on the group: {str(e)}")
        return

    try:
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p"))
        )
        for line in message.split("\n"):
            message_box.send_keys(line)
            message_box.send_keys(Keys.SHIFT, Keys.ENTER)
        message_box.send_keys(Keys.ENTER)
        print(f"Message sent to {group_name}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")

@flask_app.route('/select_shops', methods=['POST'])
def select_shops():
    selected_shops = request.form.get('selectedShops', '').split(',')
    message = "Dear Sir/Mam \n \n Kindly place your orders for tomorrow \n if already place order means avoid this message"

    def automated_whatsapp(selected_shops, message):
        chrome_service = Service("O:/Whatsapp_Automation/Lib/chromedriver.exe")
        driver = webdriver.Chrome(service=chrome_service)

        # Load cookies if they exist
        cookies_file = r"O:\Whatsapp_Automation\userdata\whatsapp_session_cookies.pkl"
        driver.get("https://web.whatsapp.com")

        if os.path.exists(cookies_file):
            with open(cookies_file, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            driver.refresh()
        else:
            WebDriverWait(driver, 5 * 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list-search']"))
            )
            with open(cookies_file, "wb") as file:
                pickle.dump(driver.get_cookies(), file)
        time.sleep(3 * 60)

        for group in selected_shops:
            send_message(driver, group, message)
        time.sleep(3 * 60)

        driver.quit()
    
    threading.Thread(target=automated_whatsapp, args=(selected_shops, message)).start()
    return jsonify({"status": "success", "message": "Messages are being sent."})

# Start Flask in a separate thread
def run_flask():
    flask_app.run(port=5000, debug=False, use_reloader=False)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local HTML Viewer")
        self.setGeometry(100, 100, 600, 800)
        icon_path = os.path.abspath("templates/loop.png")  
        self.setWindowIcon(QIcon(icon_path))
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())

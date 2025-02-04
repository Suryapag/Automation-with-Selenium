WhatsApp Automation with Flask and Selenium
This project automates the process of sending WhatsApp messages to selected groups through the web interface. It uses Flask for the backend, PyQt5 for displaying the local HTML interface, and Selenium WebDriver for automating browser actions.

Features
View and select shops from a list to send automated WhatsApp messages.
Flask web server to serve a local HTML interface where users can select the shops.
Selenium WebDriver for automating the process of sending WhatsApp messages.
Supports saving and loading session cookies for WhatsApp Web to prevent logging in each time.
Requirements
Before running the project, make sure you have the following installed:

Python 3.x
Flask (pip install Flask)
PyQt5 (pip install PyQt5)
Selenium (pip install selenium)
Chrome WebDriver (download it from here and place it in the correct path)
Pickle for saving WhatsApp session cookies
Project Structure
bash
Copy code
├── app.py                 # Main file containing Flask app, Selenium automation, and PyQt5 UI
├── templates/
│   ├── index.html         # HTML template for Flask to render
│   └── loop.png           # App icon for PyQt5 browser window
└── userdata/
    ├── name.txt           # Shop names text file
    ├── whatsapp_session_cookies.pkl   # Saved cookies file
Setup and Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/whatsapp-automation.git
cd whatsapp-automation
Install required dependencies:

bash
Copy code
pip install -r requirements.txt
Download and place the Chrome WebDriver:

Download the appropriate version of the ChromeDriver from here.
Place the chromedriver.exe in the folder O:/Whatsapp_Automation/Lib/ (or update the path in the script).
Update name.txt with your shop names:

The file name.txt should contain the names of WhatsApp groups (one per line) that you want to automate messaging for.
Running the application:

Once everything is set up, run the following command to start the Flask server and PyQt5 browser window:
bash
Copy code
python app.py
Using the application:

Open the local HTML interface at http://127.0.0.1:5000.
Select the shops from the list and click the send message button.
The message will be sent to the selected WhatsApp groups using Selenium and WebDriver.
How It Works
Flask App:

The Flask app serves an HTML page where users can select shops from the list (name.txt file).
When shops are selected, the app triggers the sending of messages via Selenium.
Selenium WebDriver:

Automates browser actions to interact with WhatsApp Web.
It searches for a group, sends a message, and handles login (through session cookies saved after the first login).
PyQt5:

Provides a local GUI to display the HTML interface using the QWebEngineView.
Customization
You can modify the message content in the send_message() function.
Update the name.txt file with the names of the WhatsApp groups you want to target.
Change the path to the ChromeDriver if necessary.
Troubleshooting
Error: Cookies not found: If you haven't logged into WhatsApp Web before, the program will wait and log you in. Make sure your browser is open and logged into WhatsApp Web for the first time.

Error: WebDriver not found: Ensure that the chromedriver.exe is correctly placed in the specified path or update the path in the script.

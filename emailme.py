import os
import smtplib
import ssl
from datetime import datetime as dt
from email.message import EmailMessage

import netifaces
from netifaces import AF_INET


def read_dotenv(path: str):
    """
    Reads a .env file and sets in dotenv dictionary all his content
    """
    with open(path, "r") as fh:
        dotenv = dict(
            tuple(line.replace("\n", "").split("="))
            for line in fh.readlines()
            if not line.startswith("#")
        )
        fh.close()
    return dotenv


def get_wlan0_ip_address():
    """
    Extracts the wlan0 ip address
    """
    wlan0_ip = netifaces.ifaddresses("wlan0")[AF_INET][0]["addr"]
    print(wlan0_ip)
    return wlan0_ip


def create_smtp_message(subject: str, from_mail_addr: str, to_mail_addr: str, content: str):
    """
    Creates a SMTP message
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_mail_addr
    msg["To"] = to_mail_addr
    msg.set_content(content)
    return msg


def send(to_email: str, subject: str, message: str, server: str, origin: str, password: str):
    """
    Sends an email
    """
    msg = create_smtp_message(
        subject=subject, from_mail_addr=origin, to_mail_addr=to_email, content=message
    )
    server = smtplib.SMTP(server, port=587)
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.login(origin, password)
    server.send_message(msg)
    server.quit()


def main():
    config = read_dotenv(".env")
    send(
        to_email=config["TO"],
        message=f"La IP de la Raspberry pi es {get_wlan0_ip_address()} {dt.now().strftime('%d/%m/%Y %H:%M:%S')}",
        subject="[RaspberryPi] IP address",
        server="smtp.gmail.com",
        origin=config["FROM"],
        password=config["PASSWORD"],
    )


if __name__ == "__main__":
    main()


import os
from twilio.rest import Client
import smtplib

class NotificationManager:
    
    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.number = os.environ['TWILIO_NUMBER']
        self.client = Client(self.account_sid, self.auth_token)
        self.gmail = os.environ['GMAIL_ADDRESS']
        self.password = os.environ['GMAIL_PASSWORD']

    def create_notification(self, price, destination, iata, from_date, to_date): 
        return f'Low price alert! Only {price}€ to fly from Barcelona-BCN to {destination}-{iata}, from {from_date} to {to_date}'

    def send_alert(self, text):
        message = self.client.messages.create(
            body=text, 
            from_=self.number, 
            to=os.environ['PHONE_NUMBER']
        )
        return message.status

    def send_email(self, text, to_address): 
        with smtplib.SMTP('smtp.gmail.com') as connection: 
            connection.starttls()
            connection.login(self.gmail, self.password)
            connection.sendmail(
                from_addr=self.gmail, 
                to_addrs=to_address, 
                msg=text
            )
import os
from twilio.rest import Client
import smtplib

class NotificationManager:
    
    def __init__(self):
        self.account_sid = 'AC2df22e120ee546ad575c54743b48e54f'
        self.auth_token = '125685f29fba9d8e554e55f7d65b01b1'
        self.number = '+19062845121'
        self.client = Client(self.account_sid, self.auth_token)
        self.gmail = 'pythontest.msmickersgill@gmail.com'
        self.password = 'M0nty22!'

    def create_notification(self, price, destination, iata, from_date, to_date): 
        return f'Low price alert! Only {price}€ to fly from Barcelona-BCN to {destination}-{iata}, from {from_date} to {to_date}'

    def send_alert(self, text):
        message = self.client.messages.create(
            body=text, 
            from_=self.number, 
            to='+34698956127'
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
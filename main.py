from bs4 import BeautifulSoup
import os
from requests import *
from smtplib import SMTP
from twilio.rest import Client

account_sid = os.getenv('SID')
auth_token = os.getenv('AUTH')
sender_phone = os.getenv('SENDER')
receiver_phone = os.getenv('RECEIVER')
my_gmail = os.getenv('USER')  # use your email address
receiver_email = os.getenv('R_EMAIL')  # receiver's email
my_gmail_password = os.getenv('PASSWORD')  # your email password
iron_website = 'https://www.amazon.ca/Naturalife-Steam-Iron-LCD-Display/dp/B07VC2HWD2/ref=sr_1_7?keywords=pressing' \
               '+iron&qid=1660445701&sprefix=pressing+i%2Caps%2C122&sr=8-7 '
earbud_website = 'https://www.amazon.ca/Tribit-Bluetooth-Waterproof-bluetooth-headphones/dp/B088LW4JKR/ref=sr_1_1_sspa?crid=2G4NMNDP7ZARC&keywords=spy%2Bairpods%2Bfor%2Bandroid%2Bphones&qid=1660449541&sprefix=spyairpods%2Bfor%2Bandroid%2Bphones%2Caps%2C577&sr=8-1-spons&smid=A1NHS1UC1IJ9CL&th=1'
strip_light_website = 'https://www.amazon.ca/Govee-Bluetooth-Control-Bedroom-Kitchen/dp/B098QGFWVW/ref=sr_1_2_sspa?keywords=strip%2Blights&qid=1660450772&sprefix=strip%2Caps%2C664&sr=8-2-spons&th=1'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 '
                  'Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
earbud_website_data = get(earbud_website, headers=header).text
iron_website_data = get(iron_website, headers=header).text
strip_light_website_data = get(strip_light_website, headers=header).text
earbud_soup = BeautifulSoup(earbud_website_data, 'html.parser')
iron_soup = BeautifulSoup(iron_website_data, 'html.parser')
strip_light_soup = BeautifulSoup(strip_light_website_data, 'html.parser')
# get the price and remove the dollar sign and converting it to float
earbud_price = float(earbud_soup.find(name='span', class_='a-offscreen').getText()[1:])
iron_price = float(iron_soup.find(name='span', class_='a-offscreen').getText()[1:])
strip_light_price = float(strip_light_soup.find(name='span', class_='a-offscreen').getText()[1:])


def send_mail(subject, message):
    with SMTP('smtp.gmail.com') as sending:
        sending.starttls()
        sending.login(user=my_gmail, password=my_gmail_password)
        sending.sendmail(from_addr=my_gmail, to_addrs=receiver_email, msg=f'Subject:{subject}\n{message}')


def send_sms(subject, message):
    client = Client(account_sid, auth_token)
    client.messages \
        .create(
        body=f'\n{subject}\n\n{message}',
        from_=sender_phone,
        to=receiver_phone
    )


def check_iron_price(currentPrice):
    if currentPrice <= 50:
        send_mail('IRON ALERT !!!', f'Iron is now ${currentPrice}!!!\n\n{iron_website}')
        send_sms('IRON ALERT !!!', f'Iron is now ${currentPrice}!!!\n\n{iron_website}')


def check_earbud_price(currentPrice):
    if currentPrice <= 60:
        send_mail('Earbud ALERT !!!', f'Earbud is now ${currentPrice}!!!\n\n{earbud_website}')
        send_sms('Earbud ALERT !!!', f'Earbud is now ${currentPrice}!!!\n\n{earbud_website}')


def check_strip_light(currentPrice):
    if currentPrice <= 30:
        send_mail('STRIP LIGHT ALERT!!!', f'Strip Light is now ${currentPrice}!!!\n\n{strip_light_website}')
        send_sms('STRIP LIGHT ALERT!!!', f'Strip Light is now ${currentPrice}!!!\n\n{strip_light_website}')


check_iron_price(iron_price)
check_earbud_price(earbud_price)
check_strip_light(strip_light_price)


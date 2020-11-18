import requests
from bs4 import BeautifulSoup
import smtplib
import time

items = [["https://www.amazon.co.uk/gp/product/B08HK24JSD",299.00],["https://www.amazon.co.uk/gp/product/B084DWCZXZ",49.99]]

headers ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}

def checkPrice():
    print(URL)
    page = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        price = soup.find(id="priceblock_ourprice").get_text()
        title = soup.find(id="productTitle").get_text()
    except:
        price = '£' + str(origPrice)
        title = "No title"
    print("Checking price for " + title.strip())

    conv_price = float(price[1:6])
    print("Original Price {}\n Current Price: {}".format(origPrice, conv_price))

    if(conv_price < origPrice):
        #send email
        sendMail(title.strip(), URL,origPrice,conv_price)
        print("Price dropped!")
    else:
        print("No difference")



def sendMail(title, URL, original, new):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    password = "PASSWORD HERE"
    server.login('email@email.com', password)

    subject = f"Price dropped for {title}"

    body = f"Old Price: {original}\nNew Price: {new}\nDifference: {original - new}\n{URL}"

    msg = f"Subject: {subject}\n\n{body}"


    server.sendmail(
        "email@email.com",
        msg
    )
    print("Sent email")

    server.quit()



while True:
    for i in items:
        URL = i[0]
        origPrice = i[1]
        checkPrice()
    time.sleep(600)




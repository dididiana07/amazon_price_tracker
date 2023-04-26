import os
import requests
from bs4 import BeautifulSoup
import smtplib

def amazon_price(url_product, money_currency: str):
    """Returns the price of a product from amazon."""
    URL_PRODUCT = url_product
    amazon_product_content = requests.get(url=URL_PRODUCT).content
    soup = BeautifulSoup(amazon_product_content, "html.parser")

    price = float(soup.find(name="span", class_="a-offscreen").text.split(f"{money_currency}")[0].replace(",",""))
    return price

def user_price_cut_off():
    """Decide a price."""
    price_cut_off = int(input(" "))
    return price_cut_off

def main():
    YAHOO_USER = os.environ["YAHOO_EMAIL"]
    YAHOO_PASSWORD = os.environ["AUTH_YAHOO"]
    URL = "https://www.amazon.es/Instant-Pot-Crisp-el%C3%A9ctrica-m%C3%BAltiple/dp/B0979HKNRH/ref=sr_1_1?keywords=" \
          "instant%2Bpot%2Bduo%2Bcrisp%2Bair%2Bfryer&qid=1682494509&sprefix=instant%2Bpot%2Caps%2C181&sr=8-1&th=1"
    product_current_price = amazon_price(URL, money_currency="€")
    user_price = user_price_cut_off()
    its_on = True
    while its_on:
        if product_current_price <= user_price:
            with smtplib.SMTP("smtp.mail.yahoo.mail") as connection:
                connection.starttls()
                connection.login(user=YAHOO_USER,
                                 password=YAHOO_PASSWORD)
                connection.sendmail(from_addr=YAHOO_USER,
                                    to_addrs="examplemail@gmail.com",
                                    msg="Subject:Amazon Product is on discount!\n\nDon't lose your opportunity and check"
                                        f"it\n{URL}")
            its_on = False



if __name__ == "__main__":
    main()

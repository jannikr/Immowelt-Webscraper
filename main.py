from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import pync
import time
from datetime import datetime
import requests

# Telegram
chat_id = -467201633

while True:

    saved_names = []
    # insert the immowelt url with the required filters
    immowelt_url = "https://www.immowelt.de/liste/berlin/wohnungen/" \
                   "mieten?roomi=2&prima=1000&wflmi=50&sort=createdate%2Bdesc"

    try:
        with open('inserate.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                saved_names.append(row[0])
    except FileNotFoundError:
        print("Create CSV file...")

    # writing csv files
    filename = "inserate.csv"
    f = open(filename, "a")

    if len(saved_names) == 0:
        headers = "name, adresse, miete, zeit\n"
        f.write(headers)

    # opening connection, grabbing page content and closing connection
    uClient = uReq(immowelt_url)
    page_content = uClient.read()
    uClient.close()

    # html parser
    page_soup = soup(page_content, "html.parser")

    container = (page_soup.find_all("div", {"class": "list_background_wrapper"}))

    for i in container:

        namen = i.findAll("h2")
        orte = i.findAll("div", {"class": "listlocation"})
        preise = i.findAll("div", {"class": "price_rent"})
        expose = i.findAll("div", {"class": "listitem_wrap"})

        for e in range(len(namen)):
            name = (namen[e].text.strip()).replace(",", " | ")
            adresse = (orte[e].text.strip())
            preis = (preise[e].strong.text.strip())
            try:
                expose = expose[e].get('data-oid')
            except AttributeError:
                pass

            if name not in saved_names:
                zeit = datetime.now()
                # notification mac
                pync.notify('Es gibt ein neues Inserat auf Immowelt in ' + adresse)
                # notification telegram
                message = "Neues Inserat auf ImmoWelt in: " + adresse + " für " + str(preis) + " (kalt)"
                url_send_message = 'https://api.telegram.org/bot1550234744:AAHUQCqZ_9RWB_kQERMPTYyz6jRd_CZ8etY/' \
                                   'sendMessage?chat_id=' + str(chat_id) + '&text="{}"'.format(message)
                print(message)
                requests.get(url_send_message)
                offer_url = "https://www.immowelt.de/expose/" + expose
                url_send_message = 'https://api.telegram.org/bot1550234744:AAHUQCqZ_9RWB_kQERMPTYyz6jRd_CZ8etY/' \
                                   'sendMessage?chat_id=' + str(chat_id) + '&text="{}"'.format(offer_url)
                print(offer_url)
                requests.get(url_send_message)
                f.write(name + "," + adresse.replace(",", " | ") + "," + preis.replace(",", ".") + "," + str(zeit) + "\n")
                time.sleep(5)

        f.close()

    time.sleep(300)



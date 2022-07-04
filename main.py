import requests
from bs4 import BeautifulSoup
from itertools import zip_longest

price_floor = 20
price_ceiling = 50
review_cutoff = 90

# ------------------------------ SAQ BORDEAUX SCRAPE  ------------------------------ #
response = requests.get("https://www.saq.com/en/new-products/lottery/bordeaux-futures-2021",
                        headers={"Accept-Language": "en-US,en;q=0.9",
                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                                               "537.36 (KHTML, like Gecko) Chrome/99.0.4844.51"
                                               "Safari/537.36 Edg/99.0.1150.30"})
bordeaux_saq = {}
soup = BeautifulSoup(response.text, "html.parser")
name_tags = soup.find_all(class_="product-item-link")
prices = soup.find_all(class_="price")

for i, j in zip_longest(name_tags, prices):
    if float(j.string[1:].replace(",", "")) not in range(price_floor, price_ceiling):
        pass
    else:
        bordeaux_saq[i.string.replace("2021", "").replace("Grand Cru", "").replace("Cru Classé de Graves", "").replace("Classé", "").replace("Premier", "").strip()] = j.string
print(bordeaux_saq)

# ------------------------------ TASTING BOOK SCRAPE  ------------------------------ #
response = requests.get("https://tastingbook.com/pro/bordeaux_2021",
                        headers={"Accept-Language": "en-US,en;q=0.9",
                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                                               "537.36 (KHTML, like Gecko) Chrome/99.0.4844.51"
                                               "Safari/537.36 Edg/99.0.1150.30"})
bordeaux_reviews = {}
soup = BeautifulSoup(response.text, "lxml")
reviews = soup.find_all("p", string="")

for i in range(0, len(reviews)):
    if reviews[i].string is None:
        pass
    elif reviews[i].string.replace(u"\xa0", u" ").strip() in bordeaux_saq:
        label = reviews[i].string.replace(u"\xa0", u" ").strip()
        if reviews[i+1].string is None:
            pass
        else:
            score = int(reviews[i+1].string.replace(u"\xa0p", u" ").strip())
            if score >= review_cutoff:
                bordeaux_reviews[label] = [bordeaux_saq[label], score]
print(bordeaux_reviews)

import csv
import re

from bs4 import BeautifulSoup
import requests

import time

def is_valid_tag(tag):
    pattern = r"^[a-zA-Z][a-zA-Z-]*[a-zA-Z]$"
    return bool(re.match(pattern, tag))

def scrape_quotes(tag):
    BASE_URL = f"http://quotes.toscrape.com/tag/{tag}/"
    quotes = []

    while True:
        page = requests.get(BASE_URL)
        soup = BeautifulSoup(page.content, "html.parser")
        new_quotes = soup.find_all("div", class_="quote")
        quotes.extend([(quote.find("span", class_="text").text.strip(),
                        quote.find("small", class_="author").text.strip())
                       for quote in new_quotes])
        next_page = soup.find("li", class_="next")
        if next_page:
            BASE_URL = f"http://quotes.toscrape.com{next_page.find('a')['href']}"
            time.sleep(45)
        else:
            break
    return quotes

def create_csv_file(tag, quotes):
    filename = f"{tag}_quotes.csv"
    with open(filename, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for quote, author in quotes:
            writer.writerow([quote, author])
    return filename

def main():
    user_tag = input("Enter desired tag: ")
    if not is_valid_tag(user_tag):
        print("Invalid tag.")
        return

    quotes = scrape_quotes(user_tag)
    if not quotes:
        print("No quotes found for the tag.")
        return
    filename = create_csv_file(user_tag, quotes)

if __name__ == "__main__":

    
    main()

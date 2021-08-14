from typing import Generator

import requests
from bs4 import BeautifulSoup

def get_category_link(category_name: str)-> str:
    page = requests.get('http://books.toscrape.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('a'):
        if category_name == link.text.strip():
            return 'http://books.toscrape.com/' + link.attrs['href']

def books_by_link(link: str)-> Generator[str, None, None]:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    books = soup.find_all('article', class_="product_pod")
    while True:
        for book in books:
            yield book.h3.a.attrs['title']
        if soup.find('li', class_='next'):
            link_2 = link[:link.rfind('/') + 1] + soup.find('li', class_='next').find('a').attrs['href']
            page = requests.get(link_2)
            soup = BeautifulSoup(page.content, 'html.parser')
            books = soup.find_all('article', class_="product_pod")
        else:
            break

def is_in_stock(name_book:str, name_category:str)-> bool:
    link = get_category_link(name_category)
    for title in books_by_link(link):
        if title == name_book:
            return True
    return False

if __name__ == '__main__':
    assert is_in_stock('Sharp Objects', 'Mystery')
    assert is_in_stock('Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond', 'Travel')
    assert is_in_stock('dfsdf', 'Travel') == False
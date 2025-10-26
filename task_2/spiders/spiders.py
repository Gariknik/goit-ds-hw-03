import requests
from bs4 import BeautifulSoup
import lxml
from .decorator_excp import exceptions
import json

BASE_URL = 'https://quotes.toscrape.com/'


@exceptions
def get_data_quotes()->None:
    """A scraper for getting data quotes"""
    data = list()
    page = 1
    session = requests.Session()
    while True:
        url = BASE_URL if page == 1 else f"{BASE_URL}page/{page}/"
        res = session.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        quotes = [quote.text.strip() for quote in soup.find_all('span', class_='text')]
        authors = [author.text.strip() for author in soup.find_all('small', class_='author')]
        tags = [[tag.text.strip() for tag in tags.find_all('a', class_="tag")] for tags in soup.find_all('div', class_='tags')]
        for t, a, q in zip(tags, authors, quotes):
            data.append({
                'tags': t,
                'author': a,
                'quote': q
            })
        next_link = soup.find('li', class_='next')
        if not next_link:
            break    
        page += 1

    with open("quotes.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@exceptions
def get_unique_authors_links()->set[str]:
    """A scraper for getting links authors"""
    unique_authors = set()
    page = 1
    session = requests.Session()
    while True:
        url = BASE_URL if page == 1 else f"{BASE_URL}page/{page}/"
        res = session.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        authors = [author.find_next_sibling('a')["href"] for author in soup.find_all('small', class_='author')]
        for a in authors:
            a = f"{BASE_URL[:-1]}{a}"
            unique_authors.add(a)

        next_link = soup.find('li', class_='next')
        if not next_link:
            break    
        page += 1
    return unique_authors


@exceptions
def get_data_authors()->None:
    """A scraper for getting data authors"""
    unique_authors = get_unique_authors_links()
    data = list()
    session = requests.Session()
    for link in unique_authors:
        res = session.get(link)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        data.append({
            'fullname': soup.find('h3', class_='author-title').text.strip(),
            'born_date': soup.find('span', class_='author-born-date').text.strip(),
            'born_location': soup.find('span', class_='author-born-location').text.strip(),
            'description': soup.find('div', class_='author-description').text.strip()
        })
    with open("authors.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)     
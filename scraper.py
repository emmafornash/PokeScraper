from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs4
import concurrent.futures

BASE_URL = 'https://bulbapedia.bulbagarden.net'

def scrape_pokemon_page(link: str) -> dict:
    '''
    Scrapes pokemon statistics from a particular pokemon's page
    '''

    return {}

def main() -> None:
    test_link = '/wiki/Bulbasaur_(Pok%C3%A9mon)'
    scrape_pokemon_page(BASE_URL + test_link)

if __name__ == '__main__':
    main()
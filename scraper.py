from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs4
import concurrent.futures

BASE_URL = 'https://bulbapedia.bulbagarden.net'

def scrape_pokemon_page(link: str) -> dict:
    '''
    Scrapes pokemon statistics from a particular pokemon's page
    Statistics include:
    1) National Dex Number
    2) Name
    3) Type 1
    4) Type 2 (if applicable)
    5) HP
    6) Attack
    7) Defense
    8) Special Attack
    9) Special Defence
    10) Speed
    11) Total
    12) Generation
    '''
    pokemon_data = {}

    poke_request = Request(link, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"})
    poke_client = urlopen(poke_request)
    poke_html = poke_client.read()
    poke_client.close()

    print(poke_html)

    return pokemon_data

def main() -> None:
    test_link = '/wiki/Venasaur_(Pok%C3%A9mon)'
    scrape_pokemon_page(BASE_URL + test_link)

if __name__ == '__main__':
    main()
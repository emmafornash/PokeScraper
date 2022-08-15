from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs4
import concurrent.futures

BASE_URL = 'https://pokemondb.net/pokedex/'

def get_dex_number(soup: bs4) -> int:
    '''
    Grabs the national pokedex number from a pokemon's page
    '''
    entry_number = soup.find('table', class_='vitals-table').find('td').text

    return int(entry_number)

def get_name(soup: bs4) -> str:
    '''
    Grabs the pokemon's name
    '''
    name = soup.find('main').find('h1').text

    return name

def get_types(soup: bs4) -> tuple:
    '''
    Grabs the pokemon's type 1 and, if applicable, type 2
    '''
    types = tuple((t.text for t in soup.find('table', class_='vitals-table').findAll('td')[1].findAll('a')))

    return types

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

    poke_request = Request(link, headers={'User-Agent': "Mozilla/5.0"})
    poke_client = urlopen(poke_request)
    poke_html = poke_client.read()
    poke_client.close()

    poke_soup = bs4(poke_html, "html.parser")

    pokemon_data['dex#'] = get_dex_number(poke_soup)
    pokemon_data['name'] = get_name(poke_soup)

    types = get_types(poke_soup)
    pokemon_data['type1'] = types[0]
    try:
        pokemon_data['type2'] = types[1]
    except IndexError:
        pokemon_data['type2'] = 'N/A'

    return pokemon_data

def test_cases() -> None:
    test1 = BASE_URL + 'charizard'
    poke_request = Request(test1, headers={'User-Agent': "Mozilla/5.0"})
    poke_client = urlopen(poke_request)
    poke_html = poke_client.read()
    poke_client.close()

    poke_soup = bs4(poke_html, "html.parser")

    assert get_dex_number(poke_soup) == 6
    assert get_name(poke_soup) == 'Charizard'
    assert get_types(poke_soup) == ('Fire', 'Flying')

    test2 = BASE_URL + 'kubfu'
    poke_request = Request(test2, headers={'User-Agent': "Mozilla/5.0"})
    poke_client = urlopen(poke_request)
    poke_html = poke_client.read()
    poke_client.close()

    poke_soup = bs4(poke_html, "html.parser")

    assert get_dex_number(poke_soup) == 891
    assert get_name(poke_soup) == 'Kubfu'
    assert get_types(poke_soup) == ('Fighting',)

def main() -> None:
    test_cases()

    test_link = 'beautifly'
    print(scrape_pokemon_page(BASE_URL + test_link))

    test_link = 'charmander'
    print(scrape_pokemon_page(BASE_URL + test_link))

if __name__ == '__main__':
    main()
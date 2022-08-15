from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs4
import concurrent.futures
import re

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
    types = tuple([t.text for t in soup.find('table', class_='vitals-table').findAll('td')[1].findAll('a')])

    return types

def get_base_stats(soup: bs4) -> tuple:
    '''
    Grabs the pokemon's base stats
    '''
    stats = tuple([int(s.find('td').text) for s in soup.find('div', class_='resp-scroll').findAll('tr')])

    return stats

def get_generation(soup: bs4) -> int:
    '''
    Grabs the pokemon's generation
    '''

    # parses the text to find only the generation's number
    generation = int(''.join(i for i in soup.find('p').find('abbr').text if i.isdigit()))

    return generation

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

    # sents and parses request
    poke_request = Request(link, headers={'User-Agent': "Mozilla/5.0"})
    poke_client = urlopen(poke_request)
    poke_html = poke_client.read()
    poke_client.close()

    poke_soup = bs4(poke_html, "html.parser")

    # gets dex number and name
    pokemon_data['dex#'] = get_dex_number(poke_soup)
    pokemon_data['name'] = get_name(poke_soup)

    # gets types. returns type2 as 'N/A' if the pokemon only has one type
    types = get_types(poke_soup)
    pokemon_data['type1'] = types[0]
    try:
        pokemon_data['type2'] = types[1]
    except IndexError:
        pokemon_data['type2'] = 'N/A'

    hp, attack, defense, s_atk, s_def, speed, total = get_base_stats(poke_soup)
    pokemon_data['hp'] = hp
    pokemon_data['attack'] = attack
    pokemon_data['defense'] = defense
    pokemon_data['sp. atk'] = s_atk
    pokemon_data['sp. def'] = s_def
    pokemon_data['speed'] = speed
    pokemon_data['total'] = total

    pokemon_data['generation'] = get_generation(poke_soup)

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
    assert get_base_stats(poke_soup) == (78, 84, 78, 109, 85, 100, 534)
    assert get_generation(poke_soup) == 1

    test2 = BASE_URL + 'kubfu'
    poke_request = Request(test2, headers={'User-Agent': "Mozilla/5.0"})
    poke_client = urlopen(poke_request)
    poke_html = poke_client.read()
    poke_client.close()

    poke_soup = bs4(poke_html, "html.parser")

    assert get_dex_number(poke_soup) == 891
    assert get_name(poke_soup) == 'Kubfu'
    assert get_types(poke_soup) == ('Fighting',)
    assert get_base_stats(poke_soup) == (60, 90, 60, 53, 50, 72, 385)
    assert get_generation(poke_soup) == 8

def main() -> None:
    test_cases()

    test_link = 'beautifly'
    print(scrape_pokemon_page(BASE_URL + test_link))

    test_link = 'charmander'
    print(scrape_pokemon_page(BASE_URL + test_link))

if __name__ == '__main__':
    main()
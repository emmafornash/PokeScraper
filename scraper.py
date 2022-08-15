import enum
from typing import Generator
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs4
import concurrent.futures
from progress_bar import printProgressBar
from time import perf_counter

BASE_URL = 'https://pokemondb.net'

def gather_pokemon_links() -> set:
    dex_url = BASE_URL + '/pokedex/all'

    # request connection and grab page
    dex_request = Request(dex_url, headers={'User-Agent': "Mozilla/5.0"})
    dex_client = urlopen(dex_request)
    dex_html = dex_client.read()
    dex_client.close()

    # parse html
    soup = bs4(dex_html, "html.parser")
    pokemon_table = [p.find('a', class_='ent-name')['href'] for p in soup.find('table', id="pokedex").find('tbody').findAll('tr')]

    return set(pokemon_table)

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

    # sends and parses request
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

def scrape_pokemon_data() -> list:
    '''
    Scrapes data from all pokemon pages and returns it
    '''

    # first find all links to pokemon entries
    links = gather_pokemon_links()
    l = len(links)

    # printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)

    # formats links to include the base URL
    url = BASE_URL + '{0}'
    new_links = set(map(url.format, links))

    start = perf_counter()
    # add multithreading for scraping pokemon data
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        poke_list = executor.map(scrape_pokemon_page, new_links)
    end = perf_counter()

    print(f'Time: {end - start}')

    # for i, item in enumerate(links):
    #     # gets pokemon data from the page
    #     url = BASE_URL + item
    #     out.append(scrape_pokemon_page(url))

    return poke_list

def generator_to_string(gen: Generator) -> str:
    out = ""

    for e in gen:
        out += str(e) + '\n'

    return out[:-1]

def test_cases() -> None:
    test1 = BASE_URL + '/pokedex/charizard'
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

    test2 = BASE_URL + '/pokedex/kubfu'
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

    # test_link = '/pokedex/beautifly'
    # print(scrape_pokemon_page(BASE_URL + test_link))

    # test_link = '/pokedex/charmander'
    # print(scrape_pokemon_page(BASE_URL + test_link))

    pokemon_list = scrape_pokemon_data()

    # writes contents of list to a file
    with open('list.txt', 'w', encoding='utf-8') as f:
        f.write(generator_to_string(pokemon_list))
        f.close()

if __name__ == '__main__':
    main()
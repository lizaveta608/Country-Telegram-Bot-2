import requests
import store
from bs4 import BeautifulSoup

base_url = 'https://knoema.com/atlas'

def main():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('div',attrs={'class': 'container auto-columns'})
    #Парсим все страны на странице https://knoema.com/atlas и достаем ссылки на страницы с этими странами
    for elm in table.find_all('a'):
        res = store.initCountry(country = elm.text, atlas_href = 'https://knoema.com' + elm['href'])
        print(res.country)
        # находим iso страны и загружаем в бд
        iso = getISO(country = res.country, url = res.atlas_href)
        # store.uploadFlag(iso = iso)
        #загружаем данные о стране в бд
        getCountryInfo(country = res.country, url = res.atlas_href)

#достаем iso страны из ссылки на флаг
def getISO(country: str, url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    flag = soup.find('img', attrs={'class': 'flag'})
    iso = flag['src'][30:-4]
    res = store.setISO(country = country, iso = iso)
    return iso

#Парсим информацию о стране
def getCountryInfo(country:str, url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    facts = soup.find('div', attrs={'class': 'facts'})
    info = []
    for fact in facts.find_all('li'):
        info.append(fact.text.replace('\r\n\t\t\t\t', ''))
    capital = info[2][14:]
    population = info[6][21:].replace('\n', '')
    area = info[7][13:]
    gdp_per_capita = info[8][21:].replace('\n', '')
    gdp = info[9][26:].replace('\n', '')
    store.setCountryInfo(country = country, capital = capital, population = population, area = area, gdp_per_capita = gdp_per_capita, gdp = gdp)

main()
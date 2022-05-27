# Country Telegram Bot
## _HSE course project_
------------------
#### The project uses technology stack:

- Python 3.10.2
- Telebot library
- SQLAlchemy
- matplotlib

#### The project uses:

- [https://knoema.com/atlas](https://knoema.com/atlas) - for get data about countries
- [https://countryflagsapi.com/](https://countryflagsapi.com/) - for upload countries flags

## Installation

```sh
cd project
pip install -r requirements.txt
./configStore.sh rebuild 
```

For run the parser & populate the database:

```sh
python knoema.py
OR
./configStore.sh parsinfo
```

For run the bot:

```sh
python bot.py
```

## Project structure

```sh
.
├── bot.py
├── charts
│   └── 406149871.png
├── configStore.sh
├── db.sqlite
├── flags
│   └── ad.jpg
├── helper
│   └── dbCreate.py
├── knoema.py
├── piechart.py
├── Procfile
├── Readme.md
├── requirements.txt
└── store.py
```


| Filename / Dirname | Description |
| ------ | ------ |
| bot.py | Main telegram bot file |
| store.py | Database ORM and dbworkers functions |
| knoema.py | Parser countries list and counties data  |
| piechart.py | Create data pie charts |
| configStore.sh & helper/ db.Create.py | .sh src helper |
| Procfile | Heroku system web worker |
| flags/ | Flags dir |
| charts | Charts dir |
| requirements.txt | requirements python file |
--------------------------------------------
## Code description
### bot.py

```sh
# Welcome handler 
@bot.message_handler(commands=['start'])
def send_welcome(message)

# Menu handler
@bot.message_handler(commands=['menu'])
def menu(message)

# Handler that accepts a country name and redirects to the next function to process the incoming request via bot.register_next_step_handler()
@bot.message_handler(commands=['country_info'])
def CountryInfo(message)

# Processes an incoming user request and sends a summary of the country according to the given template
def send_country_info(message)

# Quiz handler (redirects to the next function to process the incoming request via bot.register_next_step_handler())
@bot.message_handler(commands=['quiz'])
def quiz(message)

# The logic of compiling tests and processing answers + the total number of correct answers is indicated
@bot.poll_answer_handler()
def quiz_handler(message)

# Country list handler 
# Sends a pagination list of countries in the database using telegram_bot_pagination(InlineKeyboardPaginator)
@bot.message_handler(commands=['country_list'])
def country_list(message)

# Pie chart handler (redirects to the next function to process the incoming request via bot.register_next_step_handler())
@bot.message_handler(commands=['pie_chart'])
def get_country_list(message)

# Compiles & Send pie charts from given countries by pulling data from the database
def pieChart(message)

```
### store.py

```sh
# ORM model with country information for database
class CountryInfo(db.Model)

#Unloading all countries from the database
getCountries()

#Adding a new country to the database (for the parser)
initCountry(country: str, atlas_href: str)

#Adding iso 3166-1 for the country (parser)
setISO(country: str, iso: str)

# Adding information about the country (parser)
setCountryInfo(country: str, capital: str, population: str, area: str, gdp_per_capita: str, gdp: str)


#Get iso from database corresponding to the country
getISObyCountry(country: str)

#Loading flags to the flags folder by iso codes via flagsapi
uploadFlag(country: str)

#Get information about the country from the database
getCountryFacts(country: str)
```

### Knoema.py

```sh
#get the iso of the country from the link to the flag
def getISO(country: str, url: str)

#Parse information about the country
def getCountryInfo(country:str, url: str)

main():
...
table = soup.find('div',attrs={'class': 'container auto-columns'})
    #Parse all countries on the page https://knoema.com/atlas and get links to pages with these countries
    
    for elm in table.find_all('a'):
        res = store.initCountry(country = elm.text, atlas_href = 'https://knoema.com' + elm['href'])
        
        # find the iso of the country and load it into the database
        iso = getISO(country = res.country, url = res.atlas_href)
        store.uploadFlag(iso = iso)
        
        #load country data into database
        getCountryInfo(country = res.country, url = res.atlas_href)
```

#### piechart.py
```sh
# Use python str methods & Regex for cleaning GPD data from db
lineСleaning(sample: str) 

# Compiles pie charts from given countries by pulling data from the database
pieChart(labels, chat_id)
```

#### Deployment on heroku
##### Create a Procfile and put this code in this file 

```sh
bot: python bot.py
```

```sh
git init
heroku login
heroku create appname --region eu
git add .
git commit -m 'commit'
git push heroku master
heroku ps:scale bot=1
heroku logs -t
```

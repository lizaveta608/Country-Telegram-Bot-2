from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#ORM модель с информацией о странах для бд
class CountryInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iso = db.Column(db.String(8))
    country = db.Column(db.String(64))
    atlas_href = db.Column(db.String(64))
    capital = db.Column(db.String(64))
    population = db.Column(db.String(64))
    area = db.Column(db.String(64))
    gdp_per_capita = db.Column(db.String(64))
    gdp = db.Column(db.String(64))

#Выгрузка всех стран из бд
def getCountries():
    obj = CountryInfo.query.filter(CountryInfo.country!=None).all()

    countries = []

    for i in range(len(obj)):
        countries.append(obj[i].country)

    return countries

#Добавление новой страны в бд(для парсера)
def initCountry(country: str, atlas_href: str):
    obj = CountryInfo(country = country, atlas_href = atlas_href)
  
    db.session.add(obj)
    db.session.commit()
    
    return obj

#Добавление iso 3166-1 для страны (парсер)
def setISO(country: str, iso: str):
    obj = CountryInfo.query.filter_by(country=country).first()

    obj.iso = iso

    db.session.add(obj)
    db.session.commit()
    
    return obj

#Добавление информации о стране (парсер)
def setCountryInfo(country: str, capital: str, population: str, area: str, gdp_per_capita: str, gdp: str):
    obj = CountryInfo.query.filter_by(country=country).first()

    obj.capital = capital
    obj.population = population
    obj.area = area
    obj.gdp_per_capita = gdp_per_capita
    obj.gdp = gdp

    db.session.add(obj)
    db.session.commit()
    
    return obj

#Достать iso из бд соответствующее стране
def getISObyCountry(country: str):
    obj = CountryInfo.query.filter_by(country=country).first()
    return obj.iso

#Загрузка флагов в папку flags по iso кодам через flagsapi
def uploadFlag(country: str):
    obj = CountryInfo.query.filter_by(country=country).first()
    p = requests.get('https://countryflagsapi.com/png/' + obj.iso)
    out = open(f'flags/{iso}.jpg', "wb")
    out.write(p.content)
    out.close()

#Достать информацию о стране из бд
def getCountryFacts(country: str):
    try:
        obj = CountryInfo.query.filter_by(country=country).first()

        country_dict = {
            'iso': obj.iso,
            'country': obj.country,
            'capital': obj.capital,
            'population': obj.population,
            'area': obj.area,
            'gdp_per_capita': obj.gdp_per_capita,
            'gdp': obj.gdp,
            'atlas_href': obj.atlas_href
        }
        
        return country_dict

    except Exception as e:
        return 'error'


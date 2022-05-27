import os
import telebot
from telebot import types
from dotenv import load_dotenv
import store
import difflib
import random
import piechart
from itertools import groupby
from telegram_bot_pagination import InlineKeyboardPaginator

config = load_dotenv()

bot = telebot.TeleBot(os.getenv("tgapikey"))
user_dict = {}

class UserAnswers:
    def __init__(self, user_id):
        self.user_id = user_id

        keys = [
        'correct_answer1', 'user_answer1',
        'correct_answer2', 'user_answer2',
        'correct_answer3', 'user_answer3',
        'correct_answer4', 'user_answer4',
        ]
        
        for key in keys:
            self.key = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/country_info')
        itembtn2 = types.KeyboardButton('/quiz')
        itembtn3 = types.KeyboardButton('/pie_chart')
        itembtn4 = types.KeyboardButton('/country_list')

        markup.add(itembtn1,itembtn2,itembtn3,itembtn4)

        bot.reply_to(message, "Hey! This bot will help you to study and test your knowledge in geopolitics!\n\nChoose an action!\n\n/country_info - Enter the name of the country and I will send you an up-to-date brief information about this country!\n\n/quiz - Take a short test and consolidate your knowledge!\n\n/pie_chart - Make a chart of countries' GDP percentages\n\nIf you have problems with the correct spelling of the names of countries, use the: /country_list command", reply_markup = markup, parse_mode='html')

    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

@bot.message_handler(commands=['menu'])
def menu(message):
    try:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/country_info')
        itembtn2 = types.KeyboardButton('/quiz')
        itembtn3 = types.KeyboardButton('/pie_chart')
        itembtn4 = types.KeyboardButton('/country_list')

        markup.add(itembtn1,itembtn2,itembtn3,itembtn4)

        bot.reply_to(message, 'Choose an action!', reply_markup = markup, parse_mode='MARKDOWN')

    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

@bot.message_handler(commands=['country_info'])
def CountryInfo(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, '*Input country name*', reply_markup = markup, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, send_country_info)

    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

def send_country_info(message):
    try:
        info = store.getCountryFacts(country = message.text)
        print(info)
        if info == 'error':
            res = store.getCountries()
            conjectural_options = difflib.get_close_matches(message.text, res)
            msg = 'Ivalid country name. Maybe you meant:\n'
            if len(conjectural_options) == 0:
                msg = 'Invalid country name'
            else:
                for i in range(len(conjectural_options)):
                    msg = msg + f'``` {str(conjectural_options[i])} ```' +'\n'

            retry = bot.send_message(message.chat.id, msg,parse_mode='MARKDOWN')
            bot.register_next_step_handler(retry, send_country_info)
            
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('/country_info')
            itembtn2 = types.KeyboardButton('/quiz')
            itembtn3 = types.KeyboardButton('/pie_chart')
            itembtn4 = types.KeyboardButton('/country_list')

            markup.add(itembtn1,itembtn2,itembtn3,itembtn4)

            iso = store.getISObyCountry(country = message.text)

            photo = open(f'./flags/{iso}.jpg', 'rb')

            msg = f'''
Country: *{info['country']}*
ISO 📔  (3166-1): *{info['iso']}*
Capital city: *{info['capital']}*
Population, persons: *{info['population']}*
Area, sq km: *{info['area']}*
GDP per capita, US$: *{info['gdp_per_capita']}*
GDP, billion current US$: *{info['gdp']}*

[More info about country]({info['atlas_href']})
'''

            bot.send_photo(message.chat.id, photo, caption = msg, reply_markup = markup, parse_mode='MARKDOWN')

    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

@bot.message_handler(commands=['quiz'])
def quiz(message):
    try:

        user_dict[message.chat.id] = UserAnswers(user_id = message.chat.id)

        countries = store.getCountries()
        countries = random.sample(countries, 4)
        answers = []
        correct_id = random.randint(0,3)

        answers_dict = user_dict[message.chat.id]
        answers_dict.correct_answer1 = correct_id

        answers_dict.user_answer1 = 'n/a'
        answers_dict.correct_answer2 = 'n/a'
        answers_dict.user_answer2 = 'n/a'
        answers_dict.correct_answer3 = 'n/a'
        answers_dict.user_answer3 = 'n/a'
        answers_dict.correct_answer4 = 'n/a'
        answers_dict.user_answer4 = 'n/a'

        for i in range(len(countries)):
            answers.append(store.getCountryFacts(country = countries[i])['capital'])
        
        question = f'The capital of {countries[correct_id]} is...'


        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'Question 1/4', reply_markup = markup)

        poll = bot.send_poll(message.chat.id, question, answers, is_anonymous = False, type = "quiz", correct_option_id = correct_id)

        bot.register_next_step_handler(poll, quiz_handler)

    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

@bot.poll_answer_handler()
def quiz_handler(message):
    try:
        answers_dict = user_dict[message.user.id]

        if answers_dict.user_answer1 == 'n/a':
            answers_dict.user_answer1 = message.option_ids[0]

            countries = store.getCountries()
            countries = random.sample(countries, 4)
            correct_id = random.randint(0,3)

            answers_dict.correct_answer2 = correct_id

            correct_answer_capitalcity = store.getCountryFacts(country = countries[correct_id])['capital']
            question = f'''Which country's capital is {correct_answer_capitalcity}?'''


            bot.send_message(message.user.id, 'Question 2/4')

            poll = bot.send_poll(message.user.id, question, countries, is_anonymous = False, type = "quiz", correct_option_id = correct_id)

            bot.register_next_step_handler(poll, quiz_handler)

        elif answers_dict.user_answer2 == 'n/a':
            answers_dict.user_answer2 = message.option_ids[0]

            countries = store.getCountries()
            countries = random.sample(countries, 4)
            correct_id = random.randint(0,3)

            answers_dict.correct_answer3 = correct_id
            answers = []

            for i in range(len(countries)):
                answers.append(store.getCountryFacts(country = countries[i])['population'])

            question = f'''What is the approximate population in {countries[correct_id]}?'''

            bot.send_message(message.user.id, 'Question 3/4')


            poll = bot.send_poll(message.user.id, question, answers, is_anonymous = False, type = "quiz", correct_option_id = correct_id)

            bot.register_next_step_handler(poll, quiz_handler)

        elif answers_dict.user_answer3 == 'n/a':
            answers_dict.user_answer3 = message.option_ids[0]

            countries = store.getCountries()
            countries = random.sample(countries, 4)
            correct_id = random.randint(0,3)

            answers_dict.correct_answer4 = correct_id
            answers = []

            for i in range(len(countries)):
                answers.append(store.getCountryFacts(country = countries[i])['area'])

            question = f'''What is the area of {countries[correct_id]}?'''

            bot.send_message(message.user.id, 'Question 4/4')
            
            chat_id = message.user.id
            poll = bot.send_poll(chat_id, question, answers, is_anonymous = False, type = "quiz", correct_option_id = correct_id)

            bot.register_next_step_handler(poll, quiz_handler)

        else: 
            answers_dict.user_answer4 = message.option_ids[0]
            points = 0
            if answers_dict.user_answer1 == answers_dict.correct_answer1:
                points += 1
            if answers_dict.user_answer2 == answers_dict.correct_answer2:
                points += 1
            if answers_dict.user_answer3 == answers_dict.correct_answer3:
                points += 1
            if answers_dict.user_answer4 == answers_dict.correct_answer4:
                points += 1
            
            chatid = int(message.user.id)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('/menu')

            markup.add(itembtn1)

            msg = bot.send_message(chatid, f'*You got {points} correct answers!*\n\nTo return to the menu, use the /menu command', reply_markup = markup, parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, menu)
    
    except Exception as e:
        pass

@bot.message_handler(commands=['country_list'])
def country_list(message):
    try: 
        send_countryCodeList_page(message)
    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

@bot.message_handler(commands=['pie_chart'])
def get_country_list(message):
    try: 
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Write the names of the countries separated by commas and without spaces between commas, and I will send you a pie chart comparing their GDP\nMinimum - 2 countries, Maximum - 10 countries\n\nFor example: ``` Austria,France,Japan,Poland ```', reply_markup = markup, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, pieChart)
        
    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

def pieChart(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)

        text = message.text
        country = text.split(sep=',')
        countries = [el for el, _ in groupby(country)]

        if len(countries) < 2:
            msg = bot.send_message(message.chat.id, 'Add at least 2 countries', reply_markup = markup, parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, pieChart)

        elif len(countries) > 10:
            msg = bot.send_message(message.chat.id, 'Maximum countries for the chart - 10', reply_markup = markup, parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, pieChart)

        else:
            gdpvals = piechart.pieChart(labels = countries, chat_id = message.chat.id)
            if gdpvals == 'error':
                msg = bot.send_message(message.chat.id, 'Error:( Please check the spelling of the country name and remove all spaces between commas', reply_markup = markup, parse_mode='MARKDOWN')
                bot.register_next_step_handler(msg, pieChart)
            else:
                caption = ''
                for i in range(len(countries)):
                    caption += f'{countries[i]}: {gdpvals[i]} (billion US$)\n'
                photo = open(f'./charts/{message.chat.id}.png', 'rb')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                itembtn1 = types.KeyboardButton('/menu')
                markup.add(itembtn1)
                bot.send_photo(message.chat.id, photo, caption = caption, reply_markup = markup, parse_mode='MARKDOWN')
    except Exception as e:
        bot.reply_to(message, f'smth go wrong: {e}')

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def countryCodeList_page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_countryCodeList_page(call.message, page)

def send_countryCodeList_page(message, page=1):
    data_pages = data_page()
    paginator = InlineKeyboardPaginator(
        len(data_pages),
        current_page=page,
        data_pattern='character#{page}'
    )

    bot.send_message(
        message.chat.id,
        data_pages[page-1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )

def data_page(): 
    output = store.getCountries()

    data_pages = []
    i = 0
    sample = ' '
    for j in range(len(output)):
        i += 1
        sample = sample + f' ``` {output[j]} ``` \n'
        if i % 20 == 0:
            data_pages.append(sample)
            sample = ' '
            
    return data_pages

bot.polling()

import store
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
mpl.use('Agg')

def lineСleaning(sample: str):
        text = sample.replace('(', '<')
        text = text.replace(')', '>')
        symbol = ' '.join(re.findall(r'<([^<>]+)>', text))
        text = text.replace(symbol, '')
        text = text.replace('<', '')
        text = text.replace('>', '')
        text = text.replace(',', '')
        return text

def pieChart(labels, chat_id):
    try:
        vals = []
        for i in range(len(labels)):
            gdp = store.getCountryFacts(country = labels[i])['gdp']
            gdp = lineСleaning(sample = gdp)
            vals.append(gdp)
        fig, ax = plt.subplots()
        plt.switch_backend('agg')
        ax.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True, wedgeprops={'lw':1, 'ls':'--','edgecolor':"k"}, rotatelabels=True)
        ax.axis("equal")
        fig.savefig(f'./charts/{chat_id}.png')
        return vals

    except Exception as e:
        return 'error'

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


MAIN_WEBSITE_URL = 'https://www.worlddata.info/'
ROOT_URL = 'https://www.worlddata.info/cost-of-living.php'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def preprocess_overall_table(df):
    df['Country'] = df.Country.apply(lambda x: (x.replace('*', '')).strip())
    df['Monthly_Income_Unit'] = df['Ø Monthly income'].apply(lambda x: (x.split()[-1]).strip())
    df['Ø Monthly income'] = df['Ø Monthly income'].apply(lambda x: ''.join((char for char in x if char.isdigit() or char=='.'))).astype('float')
    return df

def find_overall_table():
    global ROOT_URL
    main_df = pd.read_html(ROOT_URL)[0]
    main_df = preprocess_overall_table(main_df)
    return main_df

def get_all_country_links():
    global ROOT_URL, HEADERS, MAIN_WEBSITE_URL

    req = requests.get(ROOT_URL, headers=HEADERS)
    soup = BeautifulSoup(req.text, 'html.parser')

    main_table = soup.find('table', attrs={'class':'std100 hover'})
    all_url_tags = main_table.find_all('a')

    all_urls = [MAIN_WEBSITE_URL + url['href'] for url in all_url_tags]

    return all_urls

def fetch_all_tables(url):
    table_dict = {}

    tables = pd.read_html(url)
    
    table_dict['Languages'] = tables[0]
    table_dict['Religions'] = tables[1]
    table_dict['Economy'] = tables[2]
    table_dict['Land use'] = tables[3]
    table_dict['Transport'] = tables[4]
    table_dict['Most important cities'] = tables[5]

    return table_dict

def fetch_political_indicators(soup):

    indicators, values = [], []

    indicator_chart = soup.find('table', attrs={'id':'indic'})
    all_tds = indicator_chart.find_all('td')
    
    for i, td in enumerate(all_tds):
        if i%2==0:
            indicators.append(td.text.replace(':', '').strip())
        else:
            indidot = td.find('div', attrs={'class':'indidot'})['style']
            values.append(indidot.split(':')[1].replace('%;', '').strip())
    
    political_indicator_df = pd.DataFrame({'Indicator':indicators, 'Value':values})

    return political_indicator_df


# def get_intro_1(soup):

#     intro = soup.find('div', attrs={'id':'intro3'})
#     i1 = intro.find('div', attrs={'class':'i1'})

#     country_name = i1.find('h1').text.strip()

#     flag_img_url = f"https:{intro.find('img')['src']}"


links = get_all_country_links()
req = requests.get(links[0], headers=HEADERS)
soup = BeautifulSoup(req.text, 'html.parser')
# get_intro_1(soup)

print(fetch_political_indicators(soup))

# fetch_all_tables(links[0])









# all_urls = [main_website + url['href'] for url in all_url_tags]

# print(all_urls)



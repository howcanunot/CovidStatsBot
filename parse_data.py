import pandas as pd
from bs4 import BeautifulSoup
import requests
import statistics
import json
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt


def df_columns(dataframe, columns):
    df1 = pd.DataFrame(enumerate(columns))
    dataframe = dataframe.reset_index()
    df1.rename(columns = {1: 'Countries'}, inplace=True)
    df = df1.set_index('Countries').join(dataframe.set_index('Countries'))
    return df


def regression_week(country):
    data = df_m[df_m.index == country].T.tail(8)
    nums = list(data.values)
    try:
        rt = statistics.median(nums[:7])
        if rt != 0:
            rt = nums[-1]/rt
    except:
        return 'No data available. Try later.'
    try:
        rtn = int(statistics.median(nums[1:]) * rt)
        return (rtn)
    except:
        return 'No data available. Try later.'


def stats_week(country):
    global df_m
    info = df_m[df_m.index==country]
    print(info)
    a = info.T.tail(7)
    try:
        graph=a.plot(fontsize=10,rot=-45,figsize=(12, 8));
        plt.savefig('saved_figure1.png')
    except:
        return 'No data available. Try later.'


def max_cases(df):
    global current_df
    df = current_df
    dfd = df[df['New_cases'] != 'NaN']
    try:
        dfd['New_cases'].astype('int64')
    except:
        pass
    max_case = dfd.sort_values(by= 'New_cases', ascending = False).head(1)
    cases = str(max_case['New_cases']).split('\n')[1].split()
    return cases


def get_info(country):
    global current_df
    transp = current_df.T
    t = transp[country]
    info = {'Country':country,
            'Total cases': t['Total_cases'],
            'Active cases': t['Active_cases'],
            'New cases': t['New_cases'],
            'New deaths': t['New_deaths'],
            'New recovered': t['New_recovered']}
    st = ''
    for i in info.keys():
        st += i
        st += ': '
        if info[i] != 'NaN':
            st += str(info[i])
        else:
            st += 'No data'
        st += '\n'
    return st


def parse():  # чтобы работал код в папке кода должен быть файл 'countries.json'

    def adding(i, column, cd, k):
        try:
            cd[column] = int(k.find_all('td')[i].get_text().replace(',', '').strip('+'))
        except:
            cd[column] = 'NaN'

    def fulfilling_the_dict(f):
        cd = dict()

        columns = 'Country,Total_cases,New_cases,Total_deaths,New_deaths,Total_recovered,New_recovered,Active_cases,' \
                  'Critical_cases,Cases_1M_ratio,Deaths_1M_ratio,Total_tests,Tests_1m_ratio,Population,Continent'
        columns = list(enumerate(columns.split(','), start=1))

        cd['Country'] = f.find_all('td')[1].get_text()
        cd['Continent'] = f.find_all('td')[15].get_text()

        for k in range(1, len(columns) - 1):
            adding(columns[k][0], columns[k][1], cd, f)
        return (cd)

    countries_dict = dict()
    url = 'https://www.worldometers.info/coronavirus/#main_table'

    responce = requests.get(url)
    soup = BeautifulSoup(responce.content, 'html.parser')
    content = soup.find_all('div', {'class': 'tab-content'})[2]
    countries = content.find_all('tr', {'style': ''})[2:-1]

    s = set()
    for i in range(len(countries)):
        try:
            name = countries[i].find_all('td')[1].get_text()
            if name not in s:
                countries_dict[i] = fulfilling_the_dict(countries[i])
                s.add(name)
        except:
            pass

    import pandas as pd
    df = pd.DataFrame(countries_dict).T.iloc[:-2, :]
    df.rename(columns={'Country': 'Countries'}, inplace=True)
    import json
    name = 'countries.json'
    with open(name) as f:
        countries = json.load(f)

    def df_columns(dataframe, columns):
        df1 = pd.DataFrame(enumerate(columns))
        dataframe = dataframe.reset_index()
        df1.rename(columns={1: 'Countries'}, inplace=True)
        df11 = df1.set_index('Countries').join(dataframe.set_index('Countries'))
        return df11

    df = df_columns(df, countries).iloc[:, 2:]
    df.to_excel('output11.xlsx')

    return df


current_df = parse()
last_update_time = datetime.now()
df_m = pd.read_excel('main.xlsx')
df_m.index = df_m['Countries']
del df_m['Countries']
df_m = df_m.dropna(axis=1, how='all')



def get_current_df():
    global current_df, last_update_time, df_m
    current_df = parse()
    column_name = datetime.now().date()# нужно реализовать чтобы здесь был актуальный день
    df_m[column_name] = current_df['New_cases']
    df_m.to_excel("main.xlsx")
    last_update_time = datetime.now()


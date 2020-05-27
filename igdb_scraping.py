from bs4 import BeautifulSoup
import logging
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import pandas as pd
from selenium import webdriver


def is_good_response(resp):  # Функция возвращает True, если ответ HTML; в другом случае False
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):  # Лог ошибок
    print(e)


def simple_get(url):  # Функция для извлечения HTML кода, заданной web-страницы
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                df = pd.DataFrame(
                    {'title': titles1[0:len(release_dates)], 'release_dates': release_dates, 'publisher': publisher,
                     'dev': dev,
                     'support_dev': support_dev, 'genres': genre, 'game_modes': game_modes, 'themes': themes,
                     'mult_modes': mult_modes, 'game_eng': game_engine, 'series': series, 'perspective': persp})
                df.to_csv(r'C:\Users\Admin\Desktop\info4.csv', header=True)
                print('Results saved')
                return simple_get(url)

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        df = pd.DataFrame(
            {'title': titles1[0:len(release_dates)], 'release_dates': release_dates, 'publisher': publisher, 'dev': dev,
             'support_dev': support_dev, 'genres': genre, 'game_modes': game_modes, 'themes': themes,
             'mult_modes': mult_modes, 'game_eng': game_engine, 'series': series, 'perspective': persp})
        df.to_csv(r'C:\Users\Admin\Desktop\info14.csv', header=True)
        print('Results saved')
        return simple_get(url)


# raw_html = simple_get("https://www.metacritic.com/browse/games/score/metascore/all/all/filtered")

maininfo = []  # Список для наименований продуктов
extrainfo1 = []  # Список для цен
extrainfo2 = []  # Список для url изображений продуктов
release_dates = []
publisher = []
support_dev = []
game_modes = []
mult_modes = []
genre = []
themes = []
series = []
persp = []
game_engine = []
alt_titles = []
dev = []
titles_df = pd.read_csv(r"C:\Users\Admin\Desktop\titles.csv")
titles1 = titles_df['title'].values.tolist()
# driver = webdriver.Chrome(executable_path='C:/Users/Admin/Desktop/chromedriver_win32/chromedriver.exe')
# driver.get("https://www.igdb.com/games/"+str(titles1[0]))
for i in range (8827,len(titles1)):
    raw_html = simple_get("https://www.igdb.com/games/" + str(titles1[i]))
    soup = BeautifulSoup(raw_html, 'html.parser')  # Преобразование HTML кода в объект BeautifulSoup
    dates = ''
    devel = ''
    publ = ''
    sup_dev = ''
    for div in soup.findAll('div', attrs={'class': 'optimisly-game-maininfo'}):
        name = div
        for div in name.findAll('div', attrs={
            'class': 'text-muted release-date'}):  # Извелечение наименований продуктов; в данном случае,
            # они заключены в метки div, у которых class=name
            name1 = div.text
            dates = dates + name1 + '; '

        dates = dates[0:len(dates) - 2]
        release_dates.append(dates)

        for div in soup.findAll('div', attrs={'itemprop': "author"}):
            name1 = div.text
            devel = devel + name1 + ', '

        devel = devel[0:len(devel) - 2]
        dev.append(devel)

        for span in name.findAll('span', attrs={'itemprop': 'publisher'}):
            name1 = span.text
            publ = publ + name1 + ', '

        publ = publ[0:len(publ) - 2]
        publisher.append(publ)

    gen = ''
    g_modes = ''
    multim = ''
    for div in soup.findAll('div', attrs={
        'class': 'optimisly-game-extrainfo1'}):  # Извелечение наименований продуктов; в данном случае,
        # они заключены в метки div, у которых class=name
        name = div
        for a in name.findAll('a', attrs={'itemprop': 'playMode'}):
            name1 = a.text
            g_modes = g_modes + name1 + ', '

        for a in name.findAll('a', attrs={'itemprop': 'genre'}):
            name1 = a.text
            gen = gen + name1 + ', '

        for span in name.findAll('span', attrs={'itemprop': 'author'}):
            name1 = span.text
            sup_dev = sup_dev + name1 + ', '

        sup_dev = sup_dev[0:len(sup_dev) - 2]
        support_dev.append(sup_dev)
        extrainfo2.append(name)
        gen = gen[0:len(gen) - 2]
        g_modes = g_modes[0:len(g_modes) - 2]
        genre.append(gen)
        game_modes.append(g_modes)
        if str(name).find('Multiplayer Modes:') != -1:
            plat = str(name)[str(name).find('<br/>'):str(name).rfind('</ul') + 5]
            multim = multim + plat[5:plat.find('<ul')]
            plat = plat[plat.find('</ul>'):]
            for ul in name.findAll('ul', attrs={'class': 'nomar'}):
                name1 = ul
                for li in name1.findAll('li'):
                    name2 = li
                    if str(name2).find('fa fa-close') != -1:
                        multim = multim + li.text + ' no, '
                    elif str(name2).find('fa fa-check') != -1:
                        multim = multim + li.text + ' yes, '
                    else:
                        multim = multim + li.text + ', '
                multim = multim[0:len(multim) - 2] + '; ' + plat[plat.find('</ul>') + 5:plat.find('<ul')]
                plat = plat[plat.rfind('</ul>'):]

        multim = multim[0:len(multim) - 2]
        mult_modes.append(multim)

    theme = ''
    collect = ''
    perspect = ''
    eng = ''
    alt = ''

    for div in soup.findAll('div', attrs={
        'class': 'optimisly-game-extrainfo2'}):  # Извелечение наименований продуктов; в данном случае,
        # они заключены в метки div, у которых class=name
        name = div
        for a in name.select('a[href*=themes]'):
            name1 = a.text
            theme = theme + name1 + ', '

        theme = theme[0:len(theme) - 2]
        themes.append(theme)
        for a in name.select('a[href*=collections]'):
            name1 = a.text
            collect = collect + name1 + ', '

        collect = collect[0:len(collect) - 2]
        series.append(collect)
        for a in name.select('a[href*=player_perspectives]'):
            name1 = a.text
            perspect = perspect + name1 + ', '

        perspect = perspect[0:len(perspect) - 2]
        persp.append(perspect)
        for a in name.select('a[href*=game_engines]'):
            name1 = a.text
            eng = eng + name1 + ', '
        eng = eng[0:len(eng) - 2]
        game_engine.append(eng)
        for div in name.findAll('div', attrs={'class': 'block text-muted'}):
            name1 = div.text
            alt = alt + name1 + ', '
        alt = alt[0:len(alt) - 2]
        alt_titles.append(alt)
        # print(name)

    names = [release_dates, publisher, support_dev, game_modes, mult_modes, genre, themes, series, persp, game_engine,
         alt_titles, dev]
    if str(soup).find("We couldn't find")!=-1:
        for r in names:
            r.append("Try Again")
    for j in names:
        print(len(j))
    print(i)
    if len(release_dates)%1000==0:
        df = pd.DataFrame(
            {'title': titles1[0:len(release_dates)], 'release_dates': release_dates, 'publisher': publisher, 'dev': dev,
             'support_dev': support_dev, 'genres': genre, 'game_modes': game_modes, 'themes': themes,
             'mult_modes': mult_modes, 'game_eng': game_engine, 'series': series, 'perspective': persp})
        df.to_csv(r'C:\Users\Admin\Desktop\info'+str(i)+'.csv', header=True)
    if i==len(titles1)-1:
        df = pd.DataFrame({'title': titles1[0:len(release_dates)], 'release_dates': release_dates, 'publisher': publisher, 'dev': dev,
                           'support_dev': support_dev, 'genres': genre, 'game_modes': game_modes, 'themes': themes,
                           'mult_modes': mult_modes, 'game_eng': game_engine, 'series': series, 'perspective': persp})
        df.to_csv(r'C:\Users\Admin\Desktop\infofinal.csv', header=True)

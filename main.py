from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

urls = ['https://ru.investing.com/equities/rosneft_rts-ratios',
        'https://ru.investing.com/equities/lukoil_rts-ratios',
        'https://ru.investing.com/equities/gazprom_rts-ratios']

def parse(url):
    info=[]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="lxml")
    infoName = soup.find('div', {'class': 'instrumentHead'}).find('h1').text[:-1]
    tables = soup.find_all('table', {'class': 'genTbl reportTbl'})
    i = 0
    for table in tables:
        if (i != 1) and (i != 3) and (i != 4) and (i != 6):
            rows = table.find_all('tr', {'class': 'child'})
            i += 1
        else:
            i += 1
            continue
        for row in rows:
            value = row.find_all('td')
            try:
                if value[0].find("span").text != 'Уровень роста дивидендов ANN':
                    rowInfo = [value[0].find("span").text, value[1].text]
                    info.append(rowInfo)
            except:
                pass
    return infoName, info

def main_process(url):
    infoName, info = parse(url)
    name = []
    value = []
    d={}

    for i in info:
        name.append(i[0])
        value.append(i[1])

    d['info']=value

    df = pd.DataFrame(d, name)
    df.to_excel(f'{infoName}.xlsx')
def main(urls):
    for url in urls:
        main_process(url)

if __name__ == '__main__':
    main(urls)
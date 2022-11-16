import os

import requests
from lxml import etree
from lxml import html
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


def get_content(url):
    res = requests.get(url=url, headers=headers)
    return res.text


def parse_content(year, content):
    xml = etree.HTML(content)
    title_list = []
    titles = xml.xpath('//table[@class="table table-condensed"]/tr/td[2]/a')  # ['ISSTA Technical Papers']
    for i in range(len(titles)):
        title_list.append([year, titles[i].xpath('string(.)')])
    return title_list


def saveTocsv(listAll):
    name = ['year', 'title']
    test = pd.DataFrame(columns=name, data=listAll)
    if not os.path.exists("papers.csv"):
        test.to_csv('./papers.csv', encoding='gbk', index=None)
    else:
        test.to_csv('./papers.csv', encoding='gbk', index=None, mode='a', header=False)


years = [2018, 2019, 2020, 2021, 2022]
# https://conf.researchr.org/track/issta-2020/issta-2020-papers#event-overview
for year in years:
    url = "https://conf.researchr.org/track/issta-{0}/issta-{0}-Technical-Papers#event-overview".format(year)
    data = get_content(url)
    title_list = parse_content(year,data)
    saveTocsv(title_list)

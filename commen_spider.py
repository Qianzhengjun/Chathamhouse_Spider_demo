import requests
from lxml import etree
import csv

content = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}
url = 'https://www.chathamhouse.org/expert/comment/together-african-countries-have-enough-fight-covid-19'

response = requests.get(url=url, headers=headers)

html = etree.HTML(response.content.decode('utf-8'))

# title
title = str.strip(html.xpath('/html/body/section/section[1]/section/header/h1/text()')[0])
print(title)

# country
country = 'UK'
# print(country)

# classification
classification = html.xpath('/html/body/section/section[1]/section/header/div/span[3]/a/text()')[0]
# print(classification)

# author
author = html.xpath('//h3[@class = "author__heading"]/a/text()')[0]

# media
media = 'Chatham House'

# content done
content = content + str.strip(
    html.xpath('/html/body/section/section[1]/section/section/section[2]/div/article/header/div[2]/text()')[0]) + '\n'
uls = html.xpath('/html/body/section/section[1]/section/section/section[2]/div/article/section/div[1]/p')
for ul in uls:
    for p in range(0, 20):
        try:
            content = content + ul.xpath('./text()')[p]
            p = p + 1
        except:
            content = content + '\n'
            break

# publish_date
year = html.xpath('//span[@class = "date__year"]/text()')[0]
day_month = html.xpath('//span[@class = "date__date-month date__action"]/text()')[0]
day = day_month.split()[0]
print(day)
emonth = day_month.split()[1]
print(emonth)
month = ''
if emonth == 'January':
    month = '1'
elif emonth == 'February':
    month = '2'
elif emonth == 'March':
    month = '3'
elif emonth == 'April':
    month = '4'
elif emonth == 'May':
    month = '5'
elif emonth == 'June':
    month = '6'
elif emonth == 'July':
    month = '7'
elif emonth == 'August':
    month = '8'
elif emonth == 'September':
    month = '9'
elif emonth == 'October':
    month = '10'
elif emonth == 'November':
    month = '11'
elif emonth == 'December':
    month = '12'
publish_date = year + '/' + month + '/' + day


with open('data_May.csv','a+',encoding='utf-8',newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow([title, country, url, classification, content, publish_date, author, media, '', '', title, content])

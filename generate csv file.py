import csv

headers = ['title', 'country', 'url', 'classification', 'content', 'publish_date', 'author', 'media', 'chinese_title',
           'chinese_content', 'english_title', 'english_content']

with open('data_May.csv','w',newline='',encoding='utf-8') as fp:
    writer = csv.writer(fp)
    writer.writerow(headers)

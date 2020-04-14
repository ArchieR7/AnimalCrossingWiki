# -*- coding: UTF-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import threading

def parse_fish_table(table):
    bodys = list()
    threads = list()
    for fish in table.find_all('tr'):
        column = fish.find_all('td')
        if len(column):
            name = column[0].text.replace('\n', '').strip()
            image = column[1].find('a')['href']
            price = int(column[2].text.replace('\n', ''))
            location = column[3].text.replace('\n', '').replace(' ', '')
            shadow_size = column[4].text.replace('\n', '').replace(' ', '')
            times = column[5].text.replace('\n', '').replace(' ', '')
            time_results = list()
            for time in times.split('&'):
                value = time.split('-')
                if len(value) == 2:
                    time_results += [{'startTime': value[0], 'endTime': value[1]}]
                else:
                    time_results += [{'startTime': '00:00', 'endTime': '23:59'}]
            month = list()
            for i in range(6, 18):
                if '✓' in column[i].text:
                    month += [i - 5]
            body = {
                'name': name,
                'image': image,
                'price': price,
                'location': location,
                'shadowSize': shadow_size,
                'times': time_results,
                'month': month
            }
            thread = threading.Thread(target=localized, args=(name, body))
            threads.append(thread)
            thread.start()
            bodys += [body]
    for thread in threads:
        thread.join()
    return bodys

def parse_bug_table(table):
    bodys = list()
    threads = list()
    for fish in table.find_all('tr'):
        column = fish.find_all('td')
        if len(column):
            name = column[0].text.replace('\n', '').strip()
            image = column[1].find('a')['href']
            price = int(column[2].text.replace('\n', ''))
            location = column[3].text.replace('\n', '').replace(' ', '')
            times = column[4].text.replace('\n', '').replace(' ', '')
            time_results = list()
            for time in times.split('&'):
                value = time.split('-')
                if len(value) == 2:
                    time_results += [{'startTime': value[0], 'endTime': value[1]}]
                else:
                    time_results += [{'startTime': '00:00', 'endTime': '23:59'}]
            month = list()
            for i in range(5, 17):
                if '✓' in column[i].text:
                    month += [i - 4]
            body = {
                'name': name,
                'image': image,
                'price': price,
                'location': location,
                'times': time_results,
                'month': month
            }
            thread = threading.Thread(target=localized_bug, args=(name, body))
            threads.append(thread)
            thread.start()
            bodys += [body]
    for thread in threads:
        thread.join()
    return bodys
    
def bugs():
    url = 'https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table', {'style': 'margin: 0 auto; width: 100%; background:#92B05A; text-align:center; solid #92B05A; border-radius: 20px; -moz-border-radius: 20px; -webkit-border-radius: 20px; -khtml-border-radius: 20px; -icab-border-radius: 20px; -o-border-radius: 20px;'})
    northern = parse_bug_table(tables[0])
    southern = parse_bug_table(tables[1])
    fp = open('Northern bug.json', 'w+')
    fp.write(json.dumps(northern, indent=4, sort_keys=True))
    fp.close()
    fp = open('Southern bug.json', 'w+')
    fp.write(json.dumps(southern, indent=4, sort_keys=True))
    fp.close()

def fish():
    url = 'https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table', {'style': 'width:100%; background:#76acda; text-align:center;'})
    northern = parse_fish_table(tables[0])
    southern = parse_fish_table(tables[1])
    fp = open('Northern fish.json', 'w+')
    fp.write(json.dumps(northern, indent=4, sort_keys=True))
    fp.close()
    fp = open('Southern fish.json', 'w+')
    fp.write(json.dumps(southern, indent=4, sort_keys=True))
    fp.close()

def localized(name, body):
    url = 'https://animalcrossing.fandom.com/wiki/%s' % name.replace(' ', '_')
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table', {'style': 'width:100%; background:#76acda; text-align:center;'})
    for table in tables:
        tr = table.find_all('tr')
        if len(tr) == 9:
            for row in tr:
                value = row.find_all('td')
                if len(value):
                    result = value[1].text.replace('\n', '').replace(' ', '')
                    if len(value[1].find_all('i')):
                        result = result.replace(value[1].find_all('i')[0].text, '')
                    body[value[0].text.replace('\n', '').replace(' ', '')] = result   
            return 

def localized_bug(name, body):
    url = 'https://animalcrossing.fandom.com/wiki/%s' % name.replace(' ', '_')
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table', {'style': 'width:100%; background:#92B05A; text-align:center;'})
    for table in tables:
        tr = table.find_all('tr')
        if len(tr) == 9:
            for row in tr:
                value = row.find_all('td')
                if len(value):
                    result = value[1].text.replace('\n', '').replace(' ', '')
                    if len(value[1].find_all('i')):
                        result = result.replace(value[1].find_all('i')[0].text, '')
                    body[value[0].text.replace('\n', '').replace(' ', '')] = result   
            return 
    
fish()
bugs()
# body = {}
# localized('bitterling', body)
# print(json.dumps(body, ensure_ascii=False))
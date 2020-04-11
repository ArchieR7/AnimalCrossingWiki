# -*- coding: UTF-8 -*-
import requests
import json
from bs4 import BeautifulSoup

def parse_fish_table(table):
    bodys = list()
    for fish in table.find_all('tr'):
        column = fish.find_all('td')
        if len(column) > 0:
            name = column[0].text.replace('\n', '')
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
            bodys += [body]
    return bodys

def parse_bug_table(table):
    bodys = list()
    for fish in table.find_all('tr'):
        column = fish.find_all('td')
        if len(column) > 0:
            name = column[0].text.replace('\n', '')
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
            bodys += [body]
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
    
bugs()
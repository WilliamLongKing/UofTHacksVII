import requests
from bs4 import BeautifulSoup
import time
#import pdb

#if year divisible by 4, it's a leap year -> feb + 1
DAYS_IN_MONTH =[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WEEK = 7

year = 2020
month = 1
day = 17

# {
#     JAN = 31
#     FEB = 28
#     MAR = 31
#     APR = 30
#     MAY = 31
#     JUN = 30
#     JUL = 31
#     AUG = 31
#     SEP = 30
#     OCT = 31
#     NOV = 30
#     DEC = 31
# }

#TODO: figure out how to store this data
#TODO: get song data from spotify

while year >= 2019:     #adjust this value to extend the history of data retrieval
    URL = 'https://www.billboard.com/charts/hot-100/'+str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2) 
    print(URL)

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='chart-list container')
    #pdb.set_trace()
    chart_elems = results.find_all(class_='chart-list__element display--flex')

    for chart_elem in chart_elems:
        ranking = chart_elem.find('span', class_='chart-element__rank__number')
        artist = chart_elem.find('span', class_='chart-element__information__artist text--truncate color--secondary')
        song_title = chart_elem.find('span', class_='chart-element__information__song text--truncate color--primary')

        if ranking.text == '1' :
            print(ranking.text + ". " + song_title.text + " - " + artist.text)

        #TODO: check if song exists in db already

        #TODO: if not, add song to db
        
        # print(ranking.text)
        # print(artist.text)
        # print(song_title.text)
    day -= WEEK
    if day < 1:
        month -= 1;
        if month < 1: 
            year -= 1
            month=12
        day = DAYS_IN_MONTH[month-1] + day
    time.sleep(20)

        

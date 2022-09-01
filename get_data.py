
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unicodedata

'''
get_nba_teams() scrapes the Wikipedia page for the NBA for a current list of teams.  
get_nba_players() then iterates over this list going to each team's Wikipedia page to scrape the current roster,
returning a raw list of data in dataframe format.  
'''

def get_nba_teams():
    '''
    Get NBA team names and put them in a list format
    '''
    nba_tables = pd.read_html('https://en.wikipedia.org/wiki/National_Basketball_Association#Teams', index_col=0, header=0)
    teams = nba_tables[3]

    teams.reset_index(inplace=True)
    teams = teams[teams.Team != 'Western Conference']
    teams = teams[teams.Team != 'Eastern Conference']

    teams_list = list(teams.Team)
    clean_teams = [team.replace(' ', '_') for team in teams_list]

    return clean_teams

def get_nba_players(list_of_teams):
    '''
    Get roster table from each team's wiki page
    '''
    nba_players = []
    for team in list_of_teams:
        url = f'https://en.wikipedia.org/wiki/{team}'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('table', {"class": "toccolours"})
        table = tables[0]
        tbody = table.find_all('tbody')[0]
        actualtable = tbody.find_all('table')[0]
        actualrows = actualtable.find_all('tr')[1:]
        for tr in actualrows:
            td = tr.find_all('td')
            row = [unicodedata.normalize('NFKD', i.text.strip()) for i in td]   # gets rid of the weird \x0 spaces
            row.append(team.replace('_', ' '))          # add column for team.  may just want to use 2nd index later 
            nba_players.append(row)
    return nba_players





import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata
from urllib.request import urlopen

'''
Get NBA team names and put them in a list format
'''
nba_tables = pd.read_html('https://en.wikipedia.org/wiki/National_Basketball_Association#Teams', index_col=0, header=0)
teams = nba_tables[3]
teams.reset_index(inplace=True)
teams = teams[teams.Team != 'Western Conference']
teams = teams.iloc[1:, 1:-1]
teams_list = list(teams.Team)
clean_teams = [team.replace(' ', '_') for team in teams_list]

'''
Get the roster from an individual team's wiki page
'''

nba_players = list()

for team in clean_teams:
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
		row = [unicodedata.normalize('NFKD', i.text.strip()) for i in td]
		row.append(team.replace('_', ' '))
		nba_players.append(row)

headers = ['position', 'number', 'name', 'height', 'weight', 'dob', 'college', 'team']
nba_df = pd.DataFrame(data=nba_players, columns=headers)

nba_df.dob = nba_df.dob.str.replace('–', '-')
nba_df.dob = pd.to_datetime(nba_df.dob)
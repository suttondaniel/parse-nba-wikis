import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata
from urllib.request import urlopen
import numpy as np
import datetime as dt

def scrape_team_names(url):
	'''
	Get NBA team names from the NBA wiki and returns a cleaned list
	'''
	nba_tables = pd.read_html(url, index_col=0, header=0)
	teams = nba_tables[3]
	teams.reset_index(inplace=True)
	teams = teams[teams.Team != 'Western Conference']
	teams = teams.iloc[1:, 1:-1]
	teams_list = list(teams.Team)
	clean_teams = [team.replace(' ', '_') for team in teams_list]

	return clean_teams

def scrape_team_page(team, list_to_append_to):
	'''
	Get the roster from an individual team's wiki page
	'''
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
		list_to_append_to.append(row)

nba_players = list()

url = 'https://en.wikipedia.org/wiki/National_Basketball_Association#Teams'

nba_teams = scrape_team_names(url)

for team in nba_teams:
	scrape_team_page(team, nba_players)

headers = ['position', 'number', 'name', 'height', 'weight', 'dob', 'college', 'team']
nba_df = pd.DataFrame(data=nba_players, columns=headers)

nba_df.dob = nba_df.dob.str.replace('–', '-')       # need to find a way around those long hyphens besides manually
nba_df.dob = pd.to_datetime(nba_df.dob)

nba_df['height_in'] = nba_df['height'].apply(lambda x: x.split('(')[0])
nba_df.height_in = nba_df['height'].apply(lambda x: (int(x.split(' ')[0]) * 12) + (int(x.split(' ')[2])))
nba_df['weight_int'] = nba_df['weight'].apply(lambda x: int(x.split(' ')[0]))
nba_df['bmi'] = (703 * nba_df.weight_int) / (nba_df.height_in**2)

'''
YOUNGEST TEAM IN NBA - METHOD #1: 
convert date of birth to nanoseconds in order to run the mean, then convert back to dt
'''
nba_df['dob_ns'] = nba_df.dob.values.astype(np.int64)
pd.to_datetime(nba_df.groupby(by='team')['dob_ns'].mean()).sort_values(ascending=False)

'''
YOUNGEST TEAM IN NBA - METHOD #2: 
subtracts each player's DoB from right now which creates a timedelta object, then calculate a year figure in int format
'''
nba_df['current_age'] = nba_df.dob.apply(lambda x: (dt.datetime.now() - x).days / 365.25)

nba_df.to_csv('nba_df2.csv')
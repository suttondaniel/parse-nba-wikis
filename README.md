---
slug: scraping-nba-wikipedia-pages
title: Scraping NBA Wikipedia Pages
authors: dan
tags: [webscraping, python, pandas, BeautifulSoup]
--- 

#### Scraping NBA Wikipedia pages

Who is the youngest team in the NBA at this very moment?  What about the oldest?  How can we go about answering this?!

![alt](./images/scrape_nba_wikis/blazers_roster.png)

Luckily, the "Current Roster" section of an NBA team's Wikipedia page has all the information we need and then some, as we can see above.  My hometown Blazers are rolling several guys out that were born in the 2000s, so surely they must be up there for the youngest?  Right?  (feeling old yet?)

Here is the URL for the Blazers' current roster: 

#### *https://en.wikipedia.org/wiki/Portland_Trail_Blazers#Current_roster*

To get the data, all we will need is a list of current NBA teams and some Python libraries, namely pandas, BeautifulSoup, and requests.  Let's start by importing our libraries and invoking the **read_html** method in pandas to get a list of teams:

~~~python
import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import unicodedata
import datetime as dt
import lxml
from urllib.request import urlopen

'''
Get NBA team names and put them in a list format
'''
nba_tables = pd.read_html('https://en.wikipedia.org/wiki/National_Basketball_Association#Teams', index_col=0, header=0)
teams = nba_tables[3]
~~~

**pd.read_html** returns a list of all HTML tables in dataframe format for the entire NBA league Wikipedia, from which we select table number 4.  We get a nice output of teams, their division, location, among other things: 

![alt](./images/scrape_nba_wikis/teams_output.png)

Let's clean up that Team column: 

~~~python
teams.reset_index(inplace=True)
teams = teams[teams.Team != 'Western Conference']
teams = teams[teams.Team != 'Eastern Conference']

teams_list = list(teams.Team)
clean_teams = [team.replace(' ', '_') for team in teams_list]
~~~

Now that we have our list of NBA teams in a URL-friendly format, we can iterate through each team and pull out the current rosters: 

~~~python
nba_players = []

for team in clean_teams:
    url = f'https://en.wikipedia.org/wiki/{team}'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table', {"class": "toccolours"})
    table = tables[0]
    tbody = table.find_all('tbody')[0]
    roster_table = tbody.find_all('table')[0]
    roster_rows = roster_table.find_all('tr')[1:]
    for tr in roster_rows:
        td = tr.find_all('td')
        row = [unicodedata.normalize('NFKD', i.text.strip()) for i in td]   # gets rid of the weird \x0 spaces
        row.append(team.replace('_', ' '))          # add column for team.  may just want to use 2nd index later 
        nba_players.append(row)
~~~

This step was a tad more involved than simply feeding the link to pd.read_html.  Some of the results came back in unicode format which we had to normalize via the **unicodedata** library.  Otherwise it was just a matter of honing in to the table we wanted.  

Now that we have a full list of players on current NBA rosters, we can create our dataframe and do some cleaning: 

~~~python
headers = ['position', 'number', 'name', 'height', 'weight', 'dob', 'college', 'team']
nba_df = pd.DataFrame(data=nba_players, columns=headers)
nba_df.dob = nba_df.dob.str.replace('–', '-')       # need to find a way around those long hyphens besides manually
nba_df.dob = pd.to_datetime(nba_df.dob)
~~~

We now have a date-of-birth column in datetime format.  So which team has the youngest average roster?  Let's subtract each player's date of birth from this current moment in time to create a timedelta object then calculate a year figure in int format: 

~~~python
nba_df['current_age'] = nba_df.dob.apply(lambda x: round((dt.datetime.now() - x).days / 365.25, 2))
nba_df.groupby('team')['current_age'].mean().sort_values(ascending=True).head()
~~~

And the 

### REPLACE THIS WITH THE ROUNDED STUFF: 
| team                  |      dob_ns |
|:----------------------|------------:|
| Oklahoma City Thunder | 9.23845e+17 |
| San Antonio Spurs     | 9.10374e+17 |
| Orlando Magic         | 9.06307e+17 |
| Indiana Pacers        | 8.98105e+17 |
| Houston Rockets       | 8.91841e+17 |
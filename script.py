#import re
#import time
#import tabulate

#import pandas as pd
#import requests
#import urllib.request
#from bs4 import BeautifulSoup
#import numpy as np
#import unicodedata
#import datetime as dt
#import lxml
#from urllib.request import urlopen

from get_data import get_nba_teams, get_nba_players
from clean_data import add_and_adjust_cols

nba_teams = get_nba_teams()
nba_teams_clean = add_and_adjust_cols(nba_teams)



#nba_teams_clean.to_csv('nba_df.csv', index=False)


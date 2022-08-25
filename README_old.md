## Parsing NBA player data from Wikipedia

Which NBA team has the youngest roster?  What about the tallest?  Which college is the most well-represented in today's NBA?  These are all questions that can be answered by comparing the player rosters found on each NBA team's wikipedia page.  Luckily, Wikipedia has an easily parsable HTML format, so getting the data is just a matter of looping over a list of teams, and for each team creating pulling the player data out in list format.  From there we can simply append each player to a master list and convert to a pandas dataframe once the loop is complete.  More specifically, here are the steps we need to take: 

1) Get list of NBA teams from the main NBA Wikipedia page. 
   * This can be done with the pandas read_html function, which generates a list of DataFrame objects. 
2) Within our list of teams, replace spaces with underscores so we can loop over the list and simply place each team in the Wikipedia url
   * e.g. url = f'https://en.wikipedia.org/wiki/{team}'
3) Create an empty list.  At the end of the scraping process, this will be a list of lists, each of which representing an NBA player
4) For each team in the teams list:
   1) Create a BeautifulSoup object from the team's Wikipedia page data
   2) Through some trial and error, dig your way into the table that houses all the roster data we're looking for
   3) For each row within this roster table:
      1) Pull the text from each 'td' (i.e. table data) object, stripping the whitespace and normalizing the unicode encodings along the way, and create a list out of this information
      2) Add an element to the end of the list for the player's team
5) Manually create a list of column headers to be used in our pandas dataframe. 
6) Create the dataframe from the master list of players and headers we just created.  

## Scraping data from BBREF

1) The BBREF player code isn't scraping properly anymore.....it was working before



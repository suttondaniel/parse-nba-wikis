from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import pprint

#2004 - 2020
#hasleud01 - haslem
#jamesle01 - lebron
#duranke01 - KD
#curryst01 - curry
#willima01 - mo williams

def getSeasonHigh(season):
	seasonHigh = client.regular_season_player_box_scores(
  		player_identifier="cartevi01",
  		season_end_year=season,
	)

	gameTotals = [dict_item['points_scored'] for dict_item in seasonHigh] 

	return max(gameTotals)

def getCareerHigh(rookieYr, recentYr):
	seasonHighs = []
	for yr in range(rookieYr, recentYr):
		seasonHighs.append(getSeasonHigh(yr))
	return max(seasonHighs)

print(getCareerHigh(2001, 2020))






# klaySzn = client.regular_season_player_box_scores(
#   player_identifier="thompkl01",
#   season_end_year=2019,
# )


# gameTotals = [dict_item['points_scored'] for dict_item in klaySzn]
# print(max(gameTotals))

# for dict_item in klaySzn:
# 		print(dict_item['points_scored'])

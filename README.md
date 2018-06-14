A Python GUI Application predicting the winner of ODI Cricket matches at 80% accuracy taking into account every player’s affinity to ground, recent form and performances against opposition.

## Objective -
The very interest towards the cricket matches and the anticipation towards knowing the result beforehand to avoid edge-seating situations triggered us to come up with a Win Predictor model for ODI matches.

## Tools used -
- BeautifulSoup – Used for souping webpage (ESPNCricinfo in our case)
- TKinter – Used for front-end GUI

**Website Resource to scrap data:**
[ESPN-Cricinfo - Statsguru](http://stats.espncricinfo.com/ci/engine/stats/index.html)

## Prediction Factors -
- **Recent Form** – The Statistics of the latest 10 matches of players is used to depict his current form
- **Ground Form** – The Statistics of the players on that particular ground(venue of the match), indicates how effectively will he be able adapt himself to the specific ground.
- **Opposition score** – The Statistics of batsmen pitted against the bowling unit of the opposition gives an insight of the ability of players to score runs or take wickets against the opposition

_**Batsman Score(Recent Form & Ground Score)**_
```
SR = (Runs/Balls Faced)*100
runs = (Runs*100)/(Total team score/10)
wkts = (1-((Number of Dismissals)/(Number of matches)))*100
score50 = (Number of 50s/Number of matches)*50
score100 = (Number of 100s/Number of matches)*100
score150 = (Number of 150s/Number of matches)*150
score200 = (Number of 200s/Number of matches)*200
```
> SCORE = SR + runs + wkts + score50 + score100+ score150 + score200

_**Bowler Score(Recent Form & Ground Score)**_
```
Hauls = ((37.5*Number of 3Ws) + (62.5*Number of 5Ws)) / Number of matches 
wkts = (Wickets taken / Number of matches)*100
maidens = Maidens / int(Balls/6)*100*5
overs = int(Balls/6) + float((int(Balls)%6))/10
economy = (1-((Runs given)/(10*overs)))*100
```
> SCORE = hauls + wkts + maidens + economy

_**Opposition Score**_
```
SR = (Runs/BallsFaced)*100
if(Wickets != 0):
 	runs_per_wkt = Runs/Wickets
 else:
	runs_per_wkt = Runs
additional = Number of 4s + 1.5*(Number of 6s)
wkts = Wickets*(-5)
```
> SCORE = SR + runs_per_wkt + additional + wkts

**_The Application is designed to work on Linux Based Distributions and requires python 2 installed_**

## Packages Required - 
_All the packages mentioned below are meant to be installed apart from the basic pythonic import files_
```	
1. TKinter
2. urllib
3. pandas
4. bs4
```

## To run the Application -
_Upon proper installation of above specified packages, run the python(2.x) file in terminal as:_
> python PredictTheOutComeUI.py

## Working
**Upon successful start of applications, to predict a match's outcome**
1. Give the date of the match, playing teams and the Venue Code (indicated by ESPNCricinfo) and Click 'Next'

![Unable to load image](SCREENSHOTS/Initial_Detail.png?raw=true "Teams")

2. Enter the 11 players you are expecting to play along with thier roles in the team. (Both the batting and bowling statistics is used for the All-Rounder)

![Unable to load image](SCREENSHOTS/Player_Detail.png?raw=true "Players")

3. Click 'Scrap' to get details from the website (This may take some time and requires active internet connection)

![Unable to load image](SCREENSHOTS/Result.png?raw=true "Result")

## Future Work
- Designing Learning Algorithms(Classifier and Regressor models) on top of scrapped data to come-up with robust, effective and better results
- Usage of python's 'multiprocessing' capabilities along with 'asyncio' yields to quicken the process of scrapping.
- Replacing the venue code in GUI with country and ground names.
- Better GUI Design

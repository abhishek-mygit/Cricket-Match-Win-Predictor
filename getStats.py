from urllib import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

teamNumbers = {"Australia":2,"Bangladesh":25,"England":1,"India":6,"New Zealand":5,"Pakistan":7,"South Africa":3,"Sri Lanka":8,"West Indies":4,"Zimbabwe":9}
path = "./Web_Mining/Project/"

def players(teamName):
    url = "http://www.espncricinfo.com/ci/content/player/index.html?country="+str(teamNumbers[teamName])
    page = urlopen(url)
    soup = BeautifulSoup(page,"html.parser")

    tables=soup.find_all('table', class_='playersTable')
    rows = (tables[0]).find_all("tr")

    arrayOfPlayers = {}
    for element in rows:
        cell = element.find_all('td')
        if(len(cell)):
            arrayOfPlayers[cell[0].find(text=True)] = (cell[0].find("a").get("href"))[19:-5]
            arrayOfPlayers[cell[1].find(text=True)] = (cell[1].find("a").get("href"))[19:-5]
            arrayOfPlayers[cell[2].find(text=True)] = (cell[2].find("a").get("href"))[19:-5]
    return arrayOfPlayers

def init(url): #Returns an object of BeautifulSoup to scrap the URL passed as argument
    page = urlopen(url)
    soup = BeautifulSoup(page,"html.parser")
    return soup

#Returns the DataFrame with data scraped from internet for Batsman
def MakeDataFrameBatsman(url,ground=1): #ground is made 0 to get recentform stats
    soup = init(url)
    isNextPagePresent = 1
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    TeamScore=[]
    TeamScore=str(TeamScore)

    if(ground):
        while(isNextPagePresent):
            engineTables=soup.find_all('table', class_='engineTable')
            print "_",
            if(len(engineTables) >= 5):
                statsTable  = (engineTables[3].find_all("tbody"))[0]
                for row in statsTable.find_all("tr"):
                    cells = row.find_all('td')
                    runs = cells[0].find(text=True)
                    if(runs!="DNB" and runs!="TDNB"):
                        runs = runs.split('*')
                        runs = runs[0]
                        runs = float(runs)
                        A.append(runs)
                        B.append(float(cells[2].find(text=True)))
                        if((cells[7].find(text=True)) == "not out"):
                            C.append(0)
                        else:
                            C.append(1)
                        Link_of_the_match = cells[13].find('a').get("href")
                        url_of_match = "http://stats.espncricinfo.com" + Link_of_the_match
                        soup_match = init(url_of_match)

                        if(int(cells[8].find(text=True))==1):
                            for row in soup_match.find_all('div',class_ = "score icon-font-after"):
                                TeamScore=row.text
                        elif(int(cells[8].find(text=True))==2):
                            for row in soup_match.find_all('div',class_ = "score icon-font-before"):
                                TeamScore=row.text
                        TeamScore=re.split(' |/',TeamScore)
                        TeamScore=TeamScore[0]

                        D.append(float(TeamScore))
                        E.append(float(cells[8].find(text=True)))

                isNextPagePresent = 0

                links = soup.find_all('a',class_="PaginationLink")
                for eachLink in links:
                    if "Next" in str(eachLink):
                        url = eachLink.get("href")
                        url = "http://stats.espncricinfo.com" + url
                        isNextPagePresent = 1
                        soup = init(url)
                        break
            else:
                break
    else:
        engineTables=soup.find_all('table', class_='engineTable')
        print "_",
        if(len(engineTables) >= 5):
            statsTable  = (engineTables[3].find_all("tbody"))[0]
            limit = min(len(statsTable.find_all("tr")),9)
            counter = 0

            for row in statsTable.find_all("tr"):
                cells = row.find_all('td')
                runs = cells[0].find(text=True)
                if(runs!="DNB" and runs!="TDNB"):
                    counter = counter + 1
                    runs = runs.split('*')
                    runs = runs[0]
                    runs = float(runs)
                    A.append(runs)
                    B.append(float(cells[2].find(text=True)))
                    if((cells[7].find(text=True)) == "not out"):
                        C.append(0)
                    else:
                        C.append(1)
                    Link_of_the_match = cells[13].find('a').get("href")
                    url_of_match = "http://stats.espncricinfo.com" + Link_of_the_match
                    soup_match = init(url_of_match)
                    if(int(cells[8].find(text=True))==1):
                        for row in soup_match.find_all('div',class_ = "score icon-font-after"):
                            TeamScore=row.text
                    elif(int(cells[8].find(text=True))==2):
                        for row in soup_match.find_all('div',class_ = "score icon-font-before"):
                            TeamScore=row.text
                    TeamScore=re.split(' |/',TeamScore)
                    TeamScore=TeamScore[0]

                    D.append(float(TeamScore))
                    E.append(float(cells[8].find(text=True)))

                if(counter>limit):
                    break

    df=pd.DataFrame(A,columns=['Runs'])
    df['Balls Faced']=B
    df['Dismissal']=C
    df['TeamScore']=D
    df['Innings']=E

    return df

#Returns the DataFrame with data scraped from internet for Bowler
def MakeDataFrameBowler(url,ground=1): #ground is made 0 to get recentform stats

    soup = init(url)
    isNextPagePresent = 1
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]

    if(ground):
        while(isNextPagePresent):
            engineTables=soup.find_all('table', class_='engineTable')
            print "_",
            if(len(engineTables) >= 5):
                statsTable  = (engineTables[3].find_all("tbody"))[0]
                for row in statsTable.find_all("tr"):
                    cells = row.find_all('td')
                    overs = cells[0].find(text=True)
                    if(overs!="DNB" and overs!="TDNB"):
                        overs = float(overs)
                        balls = float(int(overs)*6 + (overs - int(overs))*10)
                        A.append(balls)
                        B.append(float(cells[1].find(text=True)))
                        C.append(float(cells[2].find(text=True)))
                        D.append(float(cells[3].find(text=True)))
                        E.append(float(cells[6].find(text=True)))

                isNextPagePresent = 0
                links = soup.find_all('a',class_="PaginationLink")
                for eachLink in links:
                    if "Next" in str(eachLink):
                        url = eachLink.get("href")
                        url = "http://stats.espncricinfo.com" + url
                        isNextPagePresent = 1
                        soup = init(url)
                        break
            else:
                break
    else:
        engineTables=soup.find_all('table', class_='engineTable')
        print "_",
        if(len(engineTables) >= 5):
            statsTable  = (engineTables[3].find_all("tbody"))[0]
            limit = min(len(statsTable.find_all("tr")),9)
            counter = 0
            for row in statsTable.find_all("tr"):
                cells = row.find_all('td')
                overs = cells[0].find(text=True)
                if(overs!="DNB" and overs!="TDNB"):
                    counter = counter + 1
                    overs = float(overs)
                    balls = float(int(overs)*6 + (overs - int(overs))*10)
                    A.append(balls)
                    B.append(float(cells[1].find(text=True)))
                    C.append(float(cells[2].find(text=True)))
                    D.append(float(cells[3].find(text=True)))
                    E.append(float(cells[6].find(text=True)))

                if(counter>limit):
                    break

    df=pd.DataFrame(A,columns=['Balls'])
    df['Maidens']=B
    df['Runs given']=C
    df['Wickets Taken']=D
    df['Innings']=E

    return df

# Returns the ground stats of a Batsman
def SingleBatsman(PlayerName,Playerid,Groundid,date):

  url = "http://stats.espncricinfo.com/ci/engine/player/"
  if(Groundid != "0"):
      url = url + Playerid + ".html?class=2;ground=" + Groundid + ";orderby=default;orderbyad=reverse;spanmax1=" + date + ";spanval1=span;template=results;type=batting;view=innings"
  else:
      url = url + Playerid + ".html?class=2;orderby=default;orderbyad=reverse;spanmax1=" + date + ";spanval1=span;template=results;type=batting;view=innings"

  soupObject = init(url)

  if(Groundid != "0"):
      Mined_Single_Player_Stats = MakeDataFrameBatsman(url)  #Stats Mined from Web
  else:
      Mined_Single_Player_Stats = MakeDataFrameBatsman(url,0)  #Stats Mined from Web

  #Player stats
  Single_Player_Stats = pd.DataFrame(index = range(1), columns = ["Player Name","Player id","Number of matches","Runs","Balls Faced","Number of Dismissals","50s","100s","150s","200s","Total Team Score"])

  Single_Player_Stats.loc[0,"Player Name"] = PlayerName
  Single_Player_Stats.loc[0,"Player id"] = Playerid
  Single_Player_Stats.loc[0,"Number of matches"] = len(Mined_Single_Player_Stats)
  Single_Player_Stats.loc[0,"Runs"],Single_Player_Stats.loc[0,"Balls Faced"],Single_Player_Stats.loc[0,"Number of Dismissals"],Single_Player_Stats.loc[0,"Total Team Score"] = Mined_Single_Player_Stats.loc[:,"Runs"].sum(),Mined_Single_Player_Stats.loc[:,"Balls Faced"].sum(),Mined_Single_Player_Stats.loc[:,"Dismissal"].sum(),Mined_Single_Player_Stats.loc[:,"TeamScore"].sum()
  Single_Player_Stats.loc[0,"50s":"200s"] = 0

  for i in range(len(Mined_Single_Player_Stats)):
      if(Mined_Single_Player_Stats.loc[i,"Runs"]>200):
          Single_Player_Stats.loc[0,"200s"] = Single_Player_Stats.loc[0,"200s"] + 1
      elif(Mined_Single_Player_Stats.loc[i,"Runs"]>150):
          Single_Player_Stats.loc[0,"150s"] = Single_Player_Stats.loc[0,"150s"] + 1
      elif(Mined_Single_Player_Stats.loc[i,"Runs"]>100):
          Single_Player_Stats.loc[0,"100s"] = Single_Player_Stats.loc[0,"100s"] + 1
      elif(Mined_Single_Player_Stats.loc[i,"Runs"]>50):
          Single_Player_Stats.loc[0,"50s"] = Single_Player_Stats.loc[0,"50s"] + 1
  return Single_Player_Stats

# returns the ground stats of a Bowler
def SingleBowler(PlayerName,Playerid,Groundid,date):

    url = "http://stats.espncricinfo.com/ci/engine/player/"
    if(Groundid!="0"):
        url = url + Playerid + ".html?class=2;ground=" + Groundid + ";orderby=default;orderbyad=reverse;spanmax1=" + date + ";spanval1=span;template=results;type=bowling;view=innings"
    else:
        url = url + Playerid + ".html?class=2;orderby=default;orderbyad=reverse;spanmax1=" + date + ";spanval1=span;template=results;type=bowling;view=innings"


    if(Groundid!="0"):
        Mined_Single_Player_Stats = MakeDataFrameBowler(url)  #Stats Mined from Web
    else:
        Mined_Single_Player_Stats = MakeDataFrameBowler(url,0)  #Stats Mined from Web

    #Player stats
    Single_Player_Stats = pd.DataFrame(index = range(1), columns = ["Player Name","Player id","Number of matches","Balls","Maidens","Runs given","Wickets Taken","3Ws","5Ws"])

    Single_Player_Stats.loc[0,"Player Name"] = PlayerName
    Single_Player_Stats.loc[0,"Player id"] = Playerid
    Single_Player_Stats.loc[0,"Number of matches"] = len(Mined_Single_Player_Stats)
    Single_Player_Stats.loc[0,"Balls"],Single_Player_Stats.loc[0,"Maidens"],Single_Player_Stats.loc[0,"Runs given"],Single_Player_Stats.loc[0,"Wickets Taken"] = Mined_Single_Player_Stats.loc[:,"Balls"].sum(),Mined_Single_Player_Stats.loc[:,"Maidens"].sum(),Mined_Single_Player_Stats.loc[:,"Runs given"].sum(),Mined_Single_Player_Stats.loc[:,"Wickets Taken"].sum()
    Single_Player_Stats.loc[0,"3Ws":"5Ws"] = 0

    for i in range(len(Mined_Single_Player_Stats)):
        if(Mined_Single_Player_Stats.loc[i,"Wickets Taken"]>=5):
            Single_Player_Stats.loc[0,"5Ws"] = Single_Player_Stats.loc[0,"5Ws"] + 1
        elif(Mined_Single_Player_Stats.loc[i,"Wickets Taken"]>=3):
            Single_Player_Stats.loc[0,"3Ws"] = Single_Player_Stats.loc[0,"3Ws"] + 1

    return Single_Player_Stats

def stats(team, ground_id, date):
  countBatsman = 1    # to check if dataframe needed to be initiated or appended
  countBowler = 1     # to check if dataframe needed to be initiated or appended

  for i in range(len(team)):
      if(team[i][2] == "Batsman"):
          if(countBatsman == 1):
              team_Batsman = SingleBatsman(team[i][0],team[i][1],ground_id,date)
              countBatsman = countBatsman + 1
          else:
              team_Batsman = team_Batsman.append(SingleBatsman(team[i][0],team[i][1],ground_id,date),ignore_index=True)
              countBatsman = countBatsman + 1
      elif(team[i][2] == "Bowler"):
          if(countBowler == 1):
              team_Bowler = SingleBowler(team[i][0],team[i][1],ground_id,date)
              countBowler = countBowler + 1
          else:
              team_Bowler = team_Bowler.append(SingleBowler(team[i][0],team[i][1],ground_id,date),ignore_index=True)
              countBowler = countBowler + 1
      elif(team[i][2] == "Allrounder"):
          if(countBatsman == 1):
              team_Batsman = SingleBatsman(team[i][0],team[i][1],ground_id,date)
              countBatsman = countBatsman + 1
          else:
              team_Batsman = team_Batsman.append(SingleBatsman(team[i][0],team[i][1],ground_id,date),ignore_index=True)
              countBatsman = countBatsman + 1
          if(countBowler == 1):
              team_Bowler = SingleBowler(team[i][0],team[i][1],ground_id,date)
              countBowler = countBowler + 1
          else:
              team_Bowler = team_Bowler.append(SingleBowler(team[i][0],team[i][1],ground_id,date),ignore_index=True)
              countBowler = countBowler + 1
      print i,"...",
  return team_Batsman,team_Bowler

def scrappedDataFrame(batsmen,bowler):
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]
    H=[]
    for bat in batsmen:
        for bowl in bowler:
            url = "http://www.cricmetric.com/matchup.py?batsman="+bat+"&bowler="+bowl
            soup = init(url)
            div=(soup.find_all('div', class_='col-lg-8'))[0]
            divODIHeading = div.find_all('div',class_='panel-heading')#Heading are Tests,T20,ODI
            divODIBody = div.find_all('div',class_='panel-body')#The contents of the coresponding headers

            isOdiRecordPresent = 0
            for head,body in zip(divODIHeading,divODIBody):
                string = head.find(text=True)

                if "vs" in string:
                    names = string.split("vs")
                    A.append(bat)
                    B.append(bowl)
                    continue;

                if(string=="ODI"):
                    runs = 0
                    balls = 0
                    outs = 0
                    dots = 0
                    fours = 0
                    sixes = 0
                    statsTable  = (body.find_all("tr"))
                    for i in range(1,len(statsTable)-1):
                        cells = statsTable[i].find_all('td')
                        if(int(cells[0].find(text=True)) != 2017):
                            runs = runs + float(cells[1].find(text=True))
                            balls = balls + float(cells[2].find(text=True))
                            outs = outs + float(cells[3].find(text=True))
                            dots = dots + float(cells[4].find(text=True))
                            fours = fours + float(cells[5].find(text=True))
                            sixes = sixes + float(cells[6].find(text=True))
                    C.append(runs)
                    D.append(balls)
                    E.append(outs)
                    F.append(dots)
                    G.append(fours)
                    H.append(sixes)
                    isOdiRecordPresent = 1
                    break

            if(isOdiRecordPresent == 0):
                C.append(0)
                D.append(0)
                E.append(0)
                F.append(0)
                G.append(0)
                H.append(0)
    df=pd.DataFrame(A,columns=['Batsman'])
    df['Bowler']=B
    df['Runs']=C
    df['BallsFaced']=D
    df['Wickets']=E
    df['Dots']=F
    df['4s']=G
    df['6s']=H

    df = df[df.BallsFaced > 10]
    df = df.reset_index(drop=True)
    return df

def opposition(batsmen,df):
    #creating a new data frame for the final output
    oppositionStats = pd.DataFrame(columns = ["Batsman","Runs","BallsFaced","Wickets","Dots","4s","6s","BowlersFaced"])
    #To find overall Stats of a batsman
    for bat in batsmen:
        temp = (df[df.Batsman == bat]).loc[:,["Runs","BallsFaced","Wickets","Dots","4s","6s"]].sum()
        length = len(oppositionStats)
        oppositionStats.loc[length,"Batsman"] = bat
        oppositionStats.loc[length,"Runs"] = temp[0]
        oppositionStats.loc[length,"BallsFaced"] = temp[1]
        oppositionStats.loc[length,"Wickets"] = temp[2]
        oppositionStats.loc[length,"Dots"] = temp[3]
        oppositionStats.loc[length,"4s"] = temp[4]
        oppositionStats.loc[length,"6s"] = temp[5]
        oppositionStats.loc[length,"BowlersFaced"] = len(df[df.Batsman == bat])
        print bat,",",
    print(" ")
    return oppositionStats

def team1_v_team2(team1,team2):
    bat1 = []
    ball1 = []
    bat2 = []
    ball2 = []

    for player in team1:
        if(player[2]=="Batsman" or player[2]=="Allrounder"):
            bat1.append(player[0])
        if(player[2]=="Bowler" or player[2]=="Allrounder"):
            ball1.append(player[0])

    for player in team2:
        if(player[2]=="Batsman" or player[2]=="Allrounder"):
            bat2.append(player[0])
        if(player[2]=="Bowler" or player[2]=="Allrounder"):
            ball2.append(player[0])

    df = scrappedDataFrame(bat1,ball2)
    bat1_v_ball2 = opposition(bat1,df)

    df = scrappedDataFrame(bat2,ball1)
    bat2_v_ball1 = opposition(bat2,df)

    return bat1_v_ball2, bat2_v_ball1

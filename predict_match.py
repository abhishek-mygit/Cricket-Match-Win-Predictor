import pandas as pd

def oposition_score(df):
    df_score = 0
    for i in range(len(df)):
        if(df.loc[i,"BowlersFaced"] != 0):
            SR = (df.loc[i,"Runs"]/df.loc[i,"BallsFaced"])*100
            if(df.loc[i,"Wickets"] != 0):
                runs_per_wkt = df.loc[i,"Runs"]/df.loc[i,"Wickets"]
            else:
                runs_per_wkt = df.loc[i,"Runs"]
            additional = df.loc[i,"4s"] + 1.5*df.loc[i,"6s"]
            wkts = df.loc[i,"Wickets"]*(-5)

            score = SR + runs_per_wkt + additional + wkts
            df_score += score

    return df_score

def ball_score(df):
    df_score = 0
    for i in range(len(df)):
        if(df.loc[i,"Number of matches"] != 0):
            hauls = (df.loc[i,"3Ws"]*37.5 + df.loc[i,"5Ws"]*62.5)/df.loc[i,"Number of matches"]
            wkts = df.loc[i,"Wickets Taken"]/df.loc[i,"Number of matches"]*100
            maidens = df.loc[i,"Maidens"]/int(df.loc[i,"Balls"]/6)*100*5
            overs = int(df.loc[i,"Balls"]/6) + float((int(df.loc[i,"Balls"])%6))/10
            economy = (1-((df.loc[i,"Runs given"])/(10*overs)))*100

            score = hauls + wkts + maidens + economy

            df_score += score

    return df_score

def bat_score(df):
    df_score = 0
    for i in range(len(df)):
        if(df.loc[i,"Number of matches"] != 0):
            SR = (df.loc[i,"Runs"]/df.loc[i,"Balls Faced"])*100
            runs = (df.loc[i,"Runs"]/(df.loc[i,"Total Team Score"]/10))*100
            wkts = (1-((df.loc[i,"Number of Dismissals"])/(df.loc[i,"Number of matches"])))*100
            score50 = (df.loc[i,"50s"]/df.loc[i,"Number of matches"])*50
            score100 = ((df.loc[i,"100s"]/df.loc[i,"Number of matches"])*100)
            score150 = ((df.loc[i,"150s"]/df.loc[i,"Number of matches"])*150)
            score200 = ((df.loc[i,"200s"]/df.loc[i,"Number of matches"])*200)

            score = SR + runs + wkts + score50 + score100 + score150 + score200

            df_score += score
    return df_score

    

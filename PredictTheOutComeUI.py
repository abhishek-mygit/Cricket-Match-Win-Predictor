import Tkinter as tk
import tkMessageBox

from urllib import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import re

import getStats
import predict_match

#teamNumbers = {"Australia":2,"Bangladesh":25,"England":1,"India":6,"New Zealand":5,"Pakistan":7,"South Africa":3,"Sri Lanka":8,"West Indies":4,"Zimbabwe":9}
path = "./Web_Mining/Project/trial/"

class getMatchDetails(tk.Frame):

    def __init__(self,root):

        self.dummy = root
        self.teamNames = ["Australia","Bangladesh","England","India","New Zealand","Pakistan","South Africa","Sri Lanka","West Indies","Zimbabwe"]
        self.dateArray = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        self.monthArray = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.yearArray = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']

        #initializing the list to display for team 1, team 2, day, month, year
        self.variable1 = tk.StringVar(root)
        self.variable1.set(self.teamNames[0]) # default value
        self.variable2 = tk.StringVar(root)
        self.variable2.set(self.teamNames[3]) # default value
        self.variable3 = tk.StringVar(root)
        self.variable3.set(self.dateArray[0]) # default value
        self.variable4 = tk.StringVar(root)
        self.variable4.set(self.monthArray[0]) # default value
        self.variable5 = tk.StringVar(root)
        self.variable5.set(self.yearArray[0]) # default value

        self.topic = tk.Label(root, text="Give Details To Scrap")
        self.topic.config(font = "Helvetica 20 bold")
        self.topic.pack()

        #Getting Team 1 name as input
        self.team1Name = tk.OptionMenu(root, self.variable1, *(self.teamNames))
        self.team1Name.place(relx=.1, rely=.2)
        self.team1Name.config(height=2, width=10)

        self.V = tk.Label(root, text="Vs")
        self.V.config(font = "Helvetica 20 bold")
        self.V.place(relx=.45, rely=.2)

        #Getting Team 2 name as input
        self.team2Name = tk.OptionMenu(root, self.variable2, *(self.teamNames))
        self.team2Name.place(relx=.6, rely=.2)
        self.team2Name.config(height=2, width=10)

        self.matchDate = tk.Label(root, text="Enter the date of the Match")
        self.matchDate.config(font = "Helvetica 11 bold")
        self.matchDate.place(relx=0.01, rely=.425)

        #Getting date as input
        self.dateOfMatch = tk.OptionMenu(root, self.variable3, *(self.dateArray))
        self.dateOfMatch.place(relx=.4, rely=.4)
        self.dateOfMatch.config(height=2, width=3)

        #Getting month as input
        self.monthOfMatch = tk.OptionMenu(root, self.variable4, *(self.monthArray))
        self.monthOfMatch.place(relx=.55, rely=.4)
        self.monthOfMatch.config(height=2, width=3)

        #Getting year as input
        self.yearOfMatch = tk.OptionMenu(root, self.variable5, *(self.yearArray))
        self.yearOfMatch.place(relx=.7, rely=.4)
        self.yearOfMatch.config(height=2, width=3)

        self.grnd = tk.Label(root, text="Enter the ground ID of the Match")
        self.grnd.config(font = "Helvetica 11 bold")
        self.grnd.place(relx=0.01, rely=.625)

        #To get ground ID as input
        self.groundID = tk.Text(root, height=1.25, width=13)
        self.groundID.place(relx=.5, rely=.630)

        #nextButton
        self.nextButton = tk.Button(root, text="Next", command=self.getDetails)
        self.nextButton.place(relx=.2, rely=.8, height=40, width=250)

    def getDetails(self):
        global country1, country2, ground, date
        country1 = self.variable1.get()
        country2 = self.variable2.get()
        day = int(self.variable3.get())
        month = self.variable4.get()
        year = self.variable5.get()
        ground = self.groundID.get("1.0","end-1c")

        if(day > 1):
            day -= 1

        elif(month != "Jan" and day == 1):
            if(month=="Feb" or month=="Apr" or month=="Jun" or month=="Sep" or month=="Nov"):
                day = 31
            elif(month=="Mar"):
                day = 28
            else:
                day = 30

            for i in range(len(self.monthArray)):
                if(self.monthArray[i] == month):
                    break;
            i=i-1
            month = self.monthArray[i]

        elif(month=="Jan" and day == 1):
            day = 31
            month = "Dec"
            for i in range(len(self.yearArray)):
                if(self.yearArray[i] == year):
                    break;
            i=i-1
            if(i==-1):
                year = "1999"
            else:
                year = self.yearArray[i]

        date = str(day) + "+" + month + "+" + year
        print("Team Name1: ",country1)
        print("Team Name2: ",country2)
        print("Date till which to scrap: ",date)
        print("Ground ID: ",ground)

        if(country1 == country2):
            tkMessageBox.showinfo("Error", "Both Team Names cannot be the same")
        elif(len(ground)==0):
            tkMessageBox.showinfo("Error", "Ground ID Field cannot be empty")
        else:
            global team1Set, team2Set
            team1Set = getStats.players(country1)
            team2Set = getStats.players(country2)
            print("Moving to the next Window...")
            self.nextButton.destroy()
            self.team1Name.destroy()
            self.team2Name.destroy()
            self.groundID.destroy()
            self.dateOfMatch.destroy()
            self.monthOfMatch.destroy()
            self.yearOfMatch.destroy()
            self.grnd.destroy()
            self.V.destroy()
            self.matchDate.destroy()
            self.dummy.geometry("800x800")
            self.getPlayerInfo()


    def getPlayerInfo(self):
        self.team1Array = list(team1Set.keys())
        self.team2Array = list(team2Set.keys())
        self.type_ = ["Batsman","Allrounder","Bowler"]

        self.t1_1 = tk.StringVar(self.dummy)
        self.t1_1.set(self.team1Array[0]) # default value
        self.t1_2 = tk.StringVar(self.dummy)
        self.t1_2.set(self.team1Array[1]) # default value
        self.t1_3 = tk.StringVar(self.dummy)
        self.t1_3.set(self.team1Array[2]) # default value
        self.t1_4= tk.StringVar(self.dummy)
        self.t1_4.set(self.team1Array[3]) # default value
        self.t1_5= tk.StringVar(self.dummy)
        self.t1_5.set(self.team1Array[4]) # default value
        self.t1_6= tk.StringVar(self.dummy)
        self.t1_6.set(self.team1Array[5]) # default value
        self.t1_7= tk.StringVar(self.dummy)
        self.t1_7.set(self.team1Array[6]) # default value
        self.t1_8= tk.StringVar(self.dummy)
        self.t1_8.set(self.team1Array[7]) # default value
        self.t1_9= tk.StringVar(self.dummy)
        self.t1_9.set(self.team1Array[8]) # default value
        self.t1_10= tk.StringVar(self.dummy)
        self.t1_10.set(self.team1Array[9]) # default value
        self.t1_11= tk.StringVar(self.dummy)
        self.t1_11.set(self.team1Array[10]) # default value

        self.role1_1 = tk.StringVar(self.dummy)
        self.role1_1.set(self.type_[0]) # default value
        self.role1_2 = tk.StringVar(self.dummy)
        self.role1_2.set(self.type_[0]) # default value
        self.role1_3 = tk.StringVar(self.dummy)
        self.role1_3.set(self.type_[0]) # default value
        self.role1_4= tk.StringVar(self.dummy)
        self.role1_4.set(self.type_[0]) # default value
        self.role1_5= tk.StringVar(self.dummy)
        self.role1_5.set(self.type_[0]) # default value
        self.role1_6= tk.StringVar(self.dummy)
        self.role1_6.set(self.type_[1]) # default value
        self.role1_7= tk.StringVar(self.dummy)
        self.role1_7.set(self.type_[1]) # default value
        self.role1_8= tk.StringVar(self.dummy)
        self.role1_8.set(self.type_[1]) # default value
        self.role1_9= tk.StringVar(self.dummy)
        self.role1_9.set(self.type_[2]) # default value
        self.role1_10= tk.StringVar(self.dummy)
        self.role1_10.set(self.type_[2]) # default value
        self.role1_11= tk.StringVar(self.dummy)
        self.role1_11.set(self.type_[2]) # default value

        self.t2_1 = tk.StringVar(self.dummy)
        self.t2_1.set(self.team2Array[0]) # default value
        self.t2_2 = tk.StringVar(self.dummy)
        self.t2_2.set(self.team2Array[1]) # default value
        self.t2_3 = tk.StringVar(self.dummy)
        self.t2_3.set(self.team2Array[2]) # default value
        self.t2_4= tk.StringVar(self.dummy)
        self.t2_4.set(self.team2Array[3]) # default value
        self.t2_5= tk.StringVar(self.dummy)
        self.t2_5.set(self.team2Array[4]) # default value
        self.t2_6= tk.StringVar(self.dummy)
        self.t2_6.set(self.team2Array[5]) # default value
        self.t2_7= tk.StringVar(self.dummy)
        self.t2_7.set(self.team2Array[6]) # default value
        self.t2_8= tk.StringVar(self.dummy)
        self.t2_8.set(self.team2Array[7]) # default value
        self.t2_9= tk.StringVar(self.dummy)
        self.t2_9.set(self.team2Array[8]) # default value
        self.t2_10= tk.StringVar(self.dummy)
        self.t2_10.set(self.team2Array[9]) # default value
        self.t2_11= tk.StringVar(self.dummy)
        self.t2_11.set(self.team2Array[10]) # default value

        self.role2_1 = tk.StringVar(self.dummy)
        self.role2_1.set(self.type_[0]) # default value
        self.role2_2 = tk.StringVar(self.dummy)
        self.role2_2.set(self.type_[0]) # default value
        self.role2_3 = tk.StringVar(self.dummy)
        self.role2_3.set(self.type_[0]) # default value
        self.role2_4= tk.StringVar(self.dummy)
        self.role2_4.set(self.type_[0]) # default value
        self.role2_5= tk.StringVar(self.dummy)
        self.role2_5.set(self.type_[0]) # default value
        self.role2_6= tk.StringVar(self.dummy)
        self.role2_6.set(self.type_[1]) # default value
        self.role2_7= tk.StringVar(self.dummy)
        self.role2_7.set(self.type_[1]) # default value
        self.role2_8= tk.StringVar(self.dummy)
        self.role2_8.set(self.type_[1]) # default value
        self.role2_9= tk.StringVar(self.dummy)
        self.role2_9.set(self.type_[2]) # default value
        self.role2_10= tk.StringVar(self.dummy)
        self.role2_10.set(self.type_[2]) # default value
        self.role2_11= tk.StringVar(self.dummy)
        self.role2_11.set(self.type_[2]) # default value

        self.disp_t1_1 = tk.OptionMenu(self.dummy, self.t1_1, *(self.team1Array))
        self.disp_t1_1.place(relx=.01, rely=.0808)
        self.disp_t1_1.config(height=2, width=11)
        self.disp_role1_1 = tk.OptionMenu(self.dummy, self.role1_1, *(self.type_))
        self.disp_role1_1.place(relx=.19, rely=.0808)
        self.disp_role1_1.config(height=2, width=10)

        self.disp_t1_2 = tk.OptionMenu(self.dummy, self.t1_2, *(self.team1Array))
        self.disp_t1_2.place(relx=.01, rely=.1616)
        self.disp_t1_2.config(height=2, width=11)
        self.disp_role1_2 = tk.OptionMenu(self.dummy, self.role1_2, *(self.type_))
        self.disp_role1_2.place(relx=.19, rely=.1616)
        self.disp_role1_2.config(height=2, width=10)

        self.disp_t1_3 = tk.OptionMenu(self.dummy, self.t1_3, *(self.team1Array))
        self.disp_t1_3.place(relx=.01, rely=.2424)
        self.disp_t1_3.config(height=2, width=11)
        self.disp_role1_3 = tk.OptionMenu(self.dummy, self.role1_3, *(self.type_))
        self.disp_role1_3.place(relx=.19, rely=.2424)
        self.disp_role1_3.config(height=2, width=10)

        self.disp_t1_4 = tk.OptionMenu(self.dummy, self.t1_4, *(self.team1Array))
        self.disp_t1_4.place(relx=.01, rely=.3232)
        self.disp_t1_4.config(height=2, width=11)
        self.disp_role1_4 = tk.OptionMenu(self.dummy, self.role1_4, *(self.type_))
        self.disp_role1_4.place(relx=.19, rely=.3232)
        self.disp_role1_4.config(height=2, width=10)

        self.disp_t1_5 = tk.OptionMenu(self.dummy, self.t1_5, *(self.team1Array))
        self.disp_t1_5.place(relx=.01, rely=.4040)
        self.disp_t1_5.config(height=2, width=11)
        self.disp_role1_5 = tk.OptionMenu(self.dummy, self.role1_5, *(self.type_))
        self.disp_role1_5.place(relx=.19, rely=.4040)
        self.disp_role1_5.config(height=2, width=10)

        self.disp_t1_6 = tk.OptionMenu(self.dummy, self.t1_6, *(self.team1Array))
        self.disp_t1_6.place(relx=.01, rely=.4848)
        self.disp_t1_6.config(height=2, width=11)
        self.disp_role1_6 = tk.OptionMenu(self.dummy, self.role1_6, *(self.type_))
        self.disp_role1_6.place(relx=.19, rely=.4848)
        self.disp_role1_6.config(height=2, width=10)

        self.disp_t1_7 = tk.OptionMenu(self.dummy, self.t1_7, *(self.team1Array))
        self.disp_t1_7.place(relx=.01, rely=.5656)
        self.disp_t1_7.config(height=2, width=11)
        self.disp_role1_7 = tk.OptionMenu(self.dummy, self.role1_7, *(self.type_))
        self.disp_role1_7.place(relx=.19, rely=.5656)
        self.disp_role1_7.config(height=2, width=10)

        self.disp_t1_8 = tk.OptionMenu(self.dummy, self.t1_8, *(self.team1Array))
        self.disp_t1_8.place(relx=.01, rely=.6464)
        self.disp_t1_8.config(height=2, width=11)
        self.disp_role1_8 = tk.OptionMenu(self.dummy, self.role1_8, *(self.type_))
        self.disp_role1_8.place(relx=.19, rely=.6464)
        self.disp_role1_8.config(height=2, width=10)

        self.disp_t1_9 = tk.OptionMenu(self.dummy, self.t1_9, *(self.team1Array))
        self.disp_t1_9.place(relx=.01, rely=.7272)
        self.disp_t1_9.config(height=2, width=11)
        self.disp_role1_9 = tk.OptionMenu(self.dummy, self.role1_9, *(self.type_))
        self.disp_role1_9.place(relx=.19, rely=.7272)
        self.disp_role1_9.config(height=2, width=10)

        self.disp_t1_10 = tk.OptionMenu(self.dummy, self.t1_10, *(self.team1Array))
        self.disp_t1_10.place(relx=.01, rely=.8)
        self.disp_t1_10.config(height=2, width=11)
        self.disp_role1_10 = tk.OptionMenu(self.dummy, self.role1_10, *(self.type_))
        self.disp_role1_10.place(relx=.19, rely=.8080)
        self.disp_role1_10.config(height=2, width=10)

        self.disp_t1_11 = tk.OptionMenu(self.dummy, self.t1_11, *(self.team1Array))
        self.disp_t1_11.place(relx=.01, rely=.8888)
        self.disp_t1_11.config(height=2, width=11)
        self.disp_role1_11 = tk.OptionMenu(self.dummy, self.role1_11, *(self.type_))
        self.disp_role1_11.place(relx=.19, rely=.8888)
        self.disp_role1_11.config(height=2, width=10)

        self.disp_t2_1 = tk.OptionMenu(self.dummy, self.t2_1, *(self.team2Array))
        self.disp_t2_1.place(relx=.63, rely=.0808)
        self.disp_t2_1.config(height=2, width=11)
        self.disp_role2_1 = tk.OptionMenu(self.dummy, self.role2_1, *(self.type_))
        self.disp_role2_1.place(relx=.8, rely=.0808)
        self.disp_role2_1.config(height=2, width=10)

        self.disp_t2_2 = tk.OptionMenu(self.dummy, self.t2_2, *(self.team2Array))
        self.disp_t2_2.place(relx=.63, rely=.1616)
        self.disp_t2_2.config(height=2, width=11)
        self.disp_role2_2 = tk.OptionMenu(self.dummy, self.role2_2, *(self.type_))
        self.disp_role2_2.place(relx=.8, rely=.1616)
        self.disp_role2_2.config(height=2, width=10)

        self.disp_t2_3 = tk.OptionMenu(self.dummy, self.t2_3, *(self.team2Array))
        self.disp_t2_3.place(relx=.63, rely=.2424)
        self.disp_t2_3.config(height=2, width=11)
        self.disp_role2_3 = tk.OptionMenu(self.dummy, self.role2_3, *(self.type_))
        self.disp_role2_3.place(relx=.8, rely=.2424)
        self.disp_role2_3.config(height=2, width=10)

        self.disp_t2_4 = tk.OptionMenu(self.dummy, self.t2_4, *(self.team2Array))
        self.disp_t2_4.place(relx=.63, rely=.3232)
        self.disp_t2_4.config(height=2, width=11)
        self.disp_role2_4 = tk.OptionMenu(self.dummy, self.role2_4, *(self.type_))
        self.disp_role2_4.place(relx=.8, rely=.3232)
        self.disp_role2_4.config(height=2, width=10)

        self.disp_t2_5 = tk.OptionMenu(self.dummy, self.t2_5, *(self.team2Array))
        self.disp_t2_5.place(relx=.63, rely=.4040)
        self.disp_t2_5.config(height=2, width=11)
        self.disp_role2_5 = tk.OptionMenu(self.dummy, self.role2_5, *(self.type_))
        self.disp_role2_5.place(relx=.8, rely=.4040)
        self.disp_role2_5.config(height=2, width=10)

        self.disp_t2_6 = tk.OptionMenu(self.dummy, self.t2_6, *(self.team2Array))
        self.disp_t2_6.place(relx=.63, rely=.4848)
        self.disp_t2_6.config(height=2, width=11)
        self.disp_role2_6 = tk.OptionMenu(self.dummy, self.role2_6, *(self.type_))
        self.disp_role2_6.place(relx=.8, rely=.4848)
        self.disp_role2_6.config(height=2, width=10)

        self.disp_t2_7 = tk.OptionMenu(self.dummy, self.t2_7, *(self.team2Array))
        self.disp_t2_7.place(relx=.63, rely=.5656)
        self.disp_t2_7.config(height=2, width=11)
        self.disp_role2_7 = tk.OptionMenu(self.dummy, self.role2_7, *(self.type_))
        self.disp_role2_7.place(relx=.8, rely=.5656)
        self.disp_role2_7.config(height=2, width=10)

        self.disp_t2_8 = tk.OptionMenu(self.dummy, self.t2_8, *(self.team2Array))
        self.disp_t2_8.place(relx=.63, rely=.6464)
        self.disp_t2_8.config(height=2, width=11)
        self.disp_role2_8 = tk.OptionMenu(self.dummy, self.role2_8, *(self.type_))
        self.disp_role2_8.place(relx=.8, rely=.6464)
        self.disp_role2_8.config(height=2, width=10)

        self.disp_t2_9 = tk.OptionMenu(self.dummy, self.t2_9, *(self.team2Array))
        self.disp_t2_9.place(relx=.63, rely=.7272)
        self.disp_t2_9.config(height=2, width=11)
        self.disp_role2_9 = tk.OptionMenu(self.dummy, self.role2_9, *(self.type_))
        self.disp_role2_9.place(relx=.8, rely=.7272)
        self.disp_role2_9.config(height=2, width=10)

        self.disp_t2_10 = tk.OptionMenu(self.dummy, self.t2_10, *(self.team2Array))
        self.disp_t2_10.place(relx=.63, rely=.8080)
        self.disp_t2_10.config(height=2, width=11)
        self.disp_role2_10 = tk.OptionMenu(self.dummy, self.role2_10, *(self.type_))
        self.disp_role2_10.place(relx=.8, rely=.8080)
        self.disp_role2_10.config(height=2, width=10)

        self.disp_t2_11 = tk.OptionMenu(self.dummy, self.t2_11, *(self.team2Array))
        self.disp_t2_11.place(relx=.63, rely=.8888)
        self.disp_t2_11.config(height=2, width=11)
        self.disp_role2_11 = tk.OptionMenu(self.dummy, self.role2_11, *(self.type_))
        self.disp_role2_11.place(relx=.8, rely=.8888)
        self.disp_role2_11.config(height=2, width=10)

        self.submitButton = tk.Button(self.dummy, text="Scrap", command=self.predict)
        self.submitButton.place(relx=.4, rely=.8, height=40, width=150)

    def predict(self):

        team1 = []
        team2 = []

        team1.append([self.t1_1.get(),team1Set[self.t1_1.get()],self.role1_1.get()])
        team1.append([self.t1_2.get(),team1Set[self.t1_2.get()],self.role1_2.get()])
        team1.append([self.t1_3.get(),team1Set[self.t1_3.get()],self.role1_3.get()])
        team1.append([self.t1_4.get(),team1Set[self.t1_4.get()],self.role1_4.get()])
        team1.append([self.t1_5.get(),team1Set[self.t1_5.get()],self.role1_5.get()])
        team1.append([self.t1_6.get(),team1Set[self.t1_6.get()],self.role1_6.get()])
        team1.append([self.t1_7.get(),team1Set[self.t1_7.get()],self.role1_7.get()])
        team1.append([self.t1_8.get(),team1Set[self.t1_8.get()],self.role1_8.get()])
        team1.append([self.t1_9.get(),team1Set[self.t1_9.get()],self.role1_9.get()])
        team1.append([self.t1_10.get(),team1Set[self.t1_10.get()],self.role1_10.get()])
        team1.append([self.t1_11.get(),team1Set[self.t1_11.get()],self.role1_11.get()])

        team2.append([self.t2_1.get(),team2Set[self.t2_1.get()],self.role2_1.get()])
        team2.append([self.t2_2.get(),team2Set[self.t2_2.get()],self.role2_2.get()])
        team2.append([self.t2_3.get(),team2Set[self.t2_3.get()],self.role2_3.get()])
        team2.append([self.t2_4.get(),team2Set[self.t2_4.get()],self.role2_4.get()])
        team2.append([self.t2_5.get(),team2Set[self.t2_5.get()],self.role2_5.get()])
        team2.append([self.t2_6.get(),team2Set[self.t2_6.get()],self.role2_6.get()])
        team2.append([self.t2_7.get(),team2Set[self.t2_7.get()],self.role2_7.get()])
        team2.append([self.t2_8.get(),team2Set[self.t2_8.get()],self.role2_8.get()])
        team2.append([self.t2_9.get(),team2Set[self.t2_9.get()],self.role2_9.get()])
        team2.append([self.t2_10.get(),team2Set[self.t2_10.get()],self.role2_10.get()])
        team2.append([self.t2_11.get(),team2Set[self.t2_11.get()],self.role2_11.get()])

        print(team1)
        print()
        print(team2)

        self.dummy.geometry("500x300")

        self.scrapping = tk.Label(self.dummy, text="The Process might take 10-15 minutes.. Scrapping..")
        self.scrapping.config(font = "Helvetica 10 bold")
        self.scrapping.pack()

        self.disp_t1_1.destroy()
        self.disp_role1_1.destroy()
        self.disp_t1_2.destroy()
        self.disp_role1_2.destroy()
        self.disp_t1_3.destroy()
        self.disp_role1_3.destroy()
        self.disp_t1_4.destroy()
        self.disp_role1_4.destroy()
        self.disp_t1_5.destroy()
        self.disp_role1_5.destroy()
        self.disp_t1_6.destroy()
        self.disp_role1_6.destroy()
        self.disp_t1_7.destroy()
        self.disp_role1_7.destroy()
        self.disp_t1_8.destroy()
        self.disp_role1_8.destroy()
        self.disp_t1_9.destroy()
        self.disp_role1_9.destroy()
        self.disp_t1_10.destroy()
        self.disp_role1_10.destroy()
        self.disp_t1_11.destroy()
        self.disp_role1_11.destroy()

        self.disp_t2_1.destroy()
        self.disp_role2_1.destroy()
        self.disp_t2_2.destroy()
        self.disp_role2_2.destroy()
        self.disp_t2_3.destroy()
        self.disp_role2_3.destroy()
        self.disp_t2_4.destroy()
        self.disp_role2_4.destroy()
        self.disp_t2_5.destroy()
        self.disp_role2_5.destroy()
        self.disp_t2_6.destroy()
        self.disp_role2_6.destroy()
        self.disp_t2_7.destroy()
        self.disp_role2_7.destroy()
        self.disp_t2_8.destroy()
        self.disp_role2_8.destroy()
        self.disp_t2_9.destroy()
        self.disp_role2_9.destroy()
        self.disp_t2_10.destroy()
        self.disp_role2_10.destroy()
        self.disp_t2_11.destroy()
        self.disp_role2_11.destroy()

        self.submitButton.destroy()
        self.topic.destroy()

        bat_ground_1,ball_ground_1 = getStats.stats(team1,ground,date)
        bat_form_1,ball_form_1 = getStats.stats(team1,"0",date)

        print("bat_ground_1: ")
        print(bat_ground_1)
        print("ball_ground_1: ")
        print(ball_ground_1)
        print("bat_form_1: ")
        print(bat_form_1)
        print("ball_form_1: ")
        print(ball_form_1)

        bat_ground_2,ball_ground_2 = getStats.stats(team2,ground,date)
        bat_form_2,ball_form_2 = getStats.stats(team2,"0",date)

        print("bat_ground_2: ")
        print(bat_ground_2)
        print("ball_ground_2: ")
        print(ball_ground_2)
        print("bat_form_2: ")
        print(bat_form_2)
        print("ball_form_2: ")
        print(ball_form_2)

        bat1_v_ball2,bat2_v_ball1 = getStats.team1_v_team2(team1,team2)

        print("bat1_v_ball2: ")
        print(bat1_v_ball2)
        print("bat2_v_ball1: ")
        print(bat2_v_ball1)

        bat_form_1_score = predict_match.bat_score(bat_form_1)
        bat_form_2_score = predict_match.bat_score(bat_form_2)

        bat_ground_1_score = predict_match.bat_score(bat_ground_1)
        bat_ground_2_score = predict_match.bat_score(bat_ground_2)

        ball_form_1_score = predict_match.ball_score(ball_form_1)
        ball_form_2_score = predict_match.ball_score(ball_form_2)

        ball_ground_1_score = predict_match.ball_score(ball_ground_1)
        ball_ground_2_score = predict_match.ball_score(ball_ground_2)

        bat1_v_ball2_score = predict_match.oposition_score(bat1_v_ball2)
        bat2_v_ball1_score = predict_match.oposition_score(bat2_v_ball1)

        print("bat_form_1_score: ")
        print(bat_form_1_score)
        print("bat_form_2_score: ")
        print(bat_form_2_score)

        print("bat_ground_1_score: ")
        print(bat_ground_1_score)
        print("bat_ground_2_score: ")
        print(bat_ground_2_score)

        print("ball_form_1_score: ")
        print(ball_form_1_score)
        print("ball_form_2_score: ")
        print(ball_form_2_score)

        print("ball_ground_1_score: ")
        print(ball_ground_1_score)
        print("ball_ground_2_score: ")
        print(ball_ground_2_score)

        print("bat1_v_ball2_score: ")
        print(bat1_v_ball2_score)
        print("bat2_v_ball1_score: ")
        print(bat2_v_ball1_score)

        team1_score = bat_form_1_score + bat_ground_1_score + ball_form_1_score + ball_ground_1_score + bat1_v_ball2_score
        team2_score = bat_form_2_score + bat_ground_2_score + ball_form_2_score + ball_ground_2_score + bat1_v_ball2_score

        print("team1_score: ",team1_score)
        print("team1_score: ",team2_score)

        percent_1 = (team1_score)/(team1_score+team2_score)*100
        percent_2 = (team2_score)/(team1_score+team2_score)*100

        print("percent_1: ",percent_1)
        print("percent_2: ",percent_2)

        self.scrapping.destroy()
        verdict = "The possibility of win for team "+country1+" is "+str(percent_1)+"% and "
        verdict += "for team "+country2+" is "+str(percent_2)+"%"

        tkMessageBox.showinfo("Verdict",verdict)

rt = tk.Tk()
rt.geometry("500x300")
rt.title("Win Loss Prediction")

getMatchDetails(rt)
rt.mainloop()

#Code by Luke Farritor
#Project started on Mar 1, 2016

#Imports
from openpyxl.cell import get_column_letter, column_index_from_string
from string import Template
import openpyxl
import codecs
import os

#Variables
templateName = "Template.html"
parsedScoresName = "Parsed.xlsx"
rowsInScores = 2800
teamFileName = "Teams.html"

teamDirLine = '<p><a href="$number.html">$number</a> - Avg: $avg' #the line per team
teamDirTemplate = Template(teamDirLine) #make it into a template
teamDirectory = ""
teamDirHtmlStartFl = "TeamDirStart.html"
teamDirHtmlEndFl = "TeamDirEnd.html"
teamDirHtmlFl = "TeamDirectory.html"

#Loading Scoring Sheet
print("Loading Workbook... (This will take a moment)")
scoresFile = openpyxl.load_workbook(parsedScoresName)
print("Loading Sheet...")
scrsSht = scoresFile.get_sheet_by_name('Sheet')

#Load Team Page HTML Template
print("Loading HTML Template...")
templateHtml = codecs.open(templateName, 'r')
template = Template(templateHtml.read())
templateHtml.close()

#Load Team Directory HTML Template
print("Loading Team Page HTML...")
teamDirStartFl = codecs.open(teamDirHtmlStartFl, 'r')
teamDirectory = teamDirStartFl.read()
teamDirStartFl.close()

teamDirEndFl = codecs.open(teamDirHtmlEndFl, 'r')
teamDirEnd = teamDirEndFl.read()
teamDirEndFl.close()

totalWins = 0
totalLosses = 0

global teamAvg #stored globally
teamAvg = 0

def percentage(part, whole):
        if(part * whole != 0): #if one of them is not zero
                return 100 * float(part)/float(whole)
        else:
                return 0

def getTeamInfo(number):
        exists = False #weather the team exists
        teamAppearances = 0 #number of matches
        teamAlliance = 'r' #what allance they were on
        teamWins = 0
        teamLosses = 0
        teamTies = 0
        teamWinPercentage = 0
        teamTotalScores = 0
        teamAvgScore = 0
        teamScores = [0] * 10000000
        for row in range(1, rowsInScores): #increment through the rows of data
                if(str(scrsSht['N' + str(row)].value).find(str(number)+',') >= 0): #checks if the team competed in this row/match
                        exists = True #if we can find the team, the team exists
                        teamAppearances += 1 #add one to the amount of team matches
                        
                        if(str(scrsSht['N' + str(row)].value).find(str(number)) >= str(scrsSht['N' + str(row)].value).find('vs')): #finds if they were on red or blue
                                teamAlliance = 'r'
                        else:
                                teamAlliance = 'b'
                        if(teamAlliance == str(scrsSht['M' + str(row)].value)): #if team won
                                teamWins += 1
                        else: #the team lost
                                teamLosses += 1

                        if(teamAlliance == 'r'): #if we are on red..
                                teamTotalScores += scrsSht['H' + str(row)].value #...add the red score to the total scores
                        else:
                                teamTotalScores += scrsSht['L' + str(row)].value


        if(exists):
                teamAvgScore = int(teamTotalScores / teamAppearances)
                teamWinPercentage = int(percentage(teamWins, teamAppearances))
        else:
                print(str(number) + ' does not exist')
                return False

        htmlSubs = dict(
                teamNumber=number,
                avgScore=teamAvgScore,
                matches=teamAppearances,
                wins=teamWins,
                ties=teamTies,
                losses=teamLosses,
                matchWin=teamWinPercentage) #substitutions into team page
        
        teamPageStr = template.safe_substitute(htmlSubs)
        teamPage = codecs.open(str(number) + '.html', 'w+') #opens(or creates) team page
        if(teamPage.read() != ''):
                teamPage.close()
                os.remove(str(number) + '.html')
                teamPage = codecs.open(str(number) + '.html', 'w+')

        teamPage.write(teamPageStr)
        teamPage.close()

        
        print(number)
        return str(str(teamAvgScore) + ',')

for n in range(1000,11050):
        teamInfo = getTeamInfo(int(n)) 
        if(teamInfo):
                teamDirSubs = dict(number=n, #team number
                                   avg=teamInfo[:teamInfo.find(',')]) #find avg score 
                teamDirectory += teamDirTemplate.safe_substitute(teamDirSubs)

teamDirectory += teamDirEnd

#write to team Dir file
teamDirPage = codecs.open(teamDirHtmlFl, 'w+') #opens(or creates) team Directory page
if(teamDirPage.read() != ''):
        teamDirPage.close()
        os.remove(teamDirHtmlFl)
        teamPage = codecs.open(teamDirHtmlFl, 'w+')

teamDirPage.write(teamDirectory)
teamDirPage.close()

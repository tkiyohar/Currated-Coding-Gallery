#package installer
import pip
import subprocess

packagecheck = subprocess.run('py -m pip list', capture_output=True)
packagecheck = packagecheck.stdout.decode("utf-8")
if "gspread" not in packagecheck:
  subprocess.run('py -m pip install gspread')
if "oauth2client" not in packagecheck:
  subprocess.run('py -m pip install oauth2client')
# -----------------------------------------------------------------------------------------------------------------------------
# google sheet stuff:
# client email: labot-367@humans-lab-hours.iam.gserviceaccount.com
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('humans-lab-hours-00b010fa4155.json', scope)

gc = gspread.authorize(credentials)

# LS = actual Lab Sheet

LS = gc.open('Lab_Hours').sheet1

# reconnect function:
def connectionCheck():
    if credentials.access_token_expired:
        print('reconnecting to google drive...')
        gc.login()
# -----------------------------------------------------------------------------------------------------------------------------
# other packages and stuff
import datetime
from datetime import date
import time
import sys

emptystring = ''
# -----------------------------------------------------------------------------------------------------------------------------
# Special Functions

# "help" command (Lists available commands)
def help():
    print("\nPlease note that all commands are lowercase and begin with a \"/\".")
    print("The following is a list of commands you can execute in the program:\n")
    print("\"/endday\": Ends the current day and discounts the hours of anyone who is still signed in (make sure everyone who is here has signed out before ending the day).")
    print("\"/signedinlist\": Lists everyone who is currently signed in.")
    print("\"/help\": Lists available commands.")

# "DayZDonE" command (Turning off lab hours program)
def DayZDonE():
    NotSignedOutColumn = list(LS.row_values(3))
    NotSignedOutPeople = list()
    if NotSignedOutColumn != ['Date:']:
        NotSignedOutColumn.remove('Date:')
        y=2
        for x in NotSignedOutColumn:
            if str(x):
                NotSignedOutPeople.append(LS.cell(1, y).value)
                LS.update_cell(3, y, '')
            y += 1
    else:
        NotSignedOutPeople.append('Nobody :)')
    print('Day concluded. The following people forgot to sign out and have thus forfeited their hours:')
    for x in NotSignedOutPeople:
        print(x)
    sys.exit()

# "who is signed in?" command (gives a list of everyone who is currently signed in)
def whoIsSignedIn():
    signInTimeColumn = 2
    studentsSignedInColumns = []
    for x in NumberOfMembers:
        if LS.cell(3, signInTimeColumn).value:
            studentsSignedInColumns.append(signInTimeColumn)
        signInTimeColumn += 1
    print('the following people are currently signed in:')
    #del studentsSignedInColumns[0]  # so "Name:" isn't counted as a member
    if studentsSignedInColumns != []:
        for x in studentsSignedInColumns:
            print(LS.cell(1, x).value)
    else:
        print('Nobody :)')
# -----------------------------------------------------------------------------------------------------------------------------
# Initialization
TodayDateRow = 0
PersonNameColumn = 0
NumberOfMembers = LS.row_values(1)
del NumberOfMembers[0]  # so "Name:" isn't counted as a member
print(NumberOfMembers)

# Date Initialization
CurrentDate = str(date.today())
Date_Column = LS.col_values(1)

def date_initialization():
    global TodayDateRow
    if emptystring in Date_Column:
        sys.exit('Error: Empty row in date column')
    else:
        blankdate = 4
        datecell = LS.cell(blankdate, 1).value
        while datecell:
            if CurrentDate == datecell:
                break
            else:
                blankdate += 1
                datecell = LS.cell(blankdate, 1).value
        TodayDateRow = blankdate
        LS.update_cell(TodayDateRow, 1, CurrentDate)


date_initialization()

# Name initialization
Name_Row = LS.row_values(1)
if emptystring in Name_Row:
    sys.exit('Error: Empty column in name row')
else:
    blankname = 2
    namecell = LS.cell(1, blankname).value
    while namecell:
        blankname += 1
        namecell = LS.cell(1, blankname).value
# -----------------------------------------------------------------------------------------------------------------------------
# name sign in part
i = 0
while i == 0:
    nameinputsection = True
    while nameinputsection == True:
        while True:
            name = input("\n\n\nPlease enter your real name or type \"/help\" for a list of commands: ")
            connectionCheck()
            if name == 'Name:':
                print('Invalid, please enter your real name.')
            elif name == 'Nobody :)':
                print('Invalid, please enter your real name.')
            elif not name:
                print('Invalid, please enter your real name.')
            elif name == '/endday':
                DayZDonE()
            elif name == '/signedinlist':
                whoIsSignedIn()
            elif name == '/help':
                help()
            elif name[0] == '/':
                print('Invalid, please enter your real name.')
            else:
                break
        if name in Name_Row:
            # person has signed in before
            PersonNameColumn = int(LS.find(name).col)
            nameinputsection = False
        else:
            # person hasn't signed on before
            print('Hello ', name, ', if this is your first time signing in enter \"y\" or enter \"n\" to re-enter your name as it may be incorrect, (please note: consistent capitalization is important).')
            firstsignin = input()
            connectionCheck()
            if firstsignin == 'y':
                LS.update_cell(1, blankname, name)
                NumberOfMembers.append(name)
                print('\"', name, '\" has been added to the lab hours sheet.')
                Name_Row.append(name)
                print(Name_Row)
                PersonNameColumn = blankname
                blankname += 1
                nameinputsection = False
                break
            elif firstsignin == 'n':
                pass
            # incorrect input (returns to name entry)
            else:
                print(
                    'Invalid input, please enter either \"y\" if this is your first time signing in or \"n\" to re-enter your name')
                pass
    # -----------------------------------------------------------------------------------------------------------------------------
    Signintime = str(LS.cell(3, PersonNameColumn).value)
    CurrentTime = str(time.strftime('%X'))
    if Signintime:
        # signing out (Signintime not blank)
        SignInHours = Signintime[:2]
        SignInHours = int(SignInHours.lstrip('0'))
        SignInMinutes = Signintime[3:-3]
        SignInMinutes = SignInMinutes.lstrip('0')
        if not SignInMinutes:
            SignInMinutes = 0
        SignInMinutes = int(SignInMinutes)
        SignInSeconds = Signintime[-2:]
        SignInSeconds = SignInSeconds.lstrip('0')
        if not SignInSeconds:
            SignInSeconds = 0
        SignInSeconds = int(SignInSeconds)
        SignOutHours = CurrentTime[:2]
        SignOutHours = int(SignOutHours.lstrip('0'))
        SignOutMinutes = CurrentTime[3:-3]
        SignOutMinutes = SignOutMinutes.lstrip('0')
        if not SignOutMinutes:
            SignOutMinutes = 0
        SignOutMinutes = int(SignOutMinutes)
        SignOutSeconds = CurrentTime[-2:]
        SignOutSeconds = SignOutSeconds.lstrip('0')
        if not SignOutSeconds:
            SignOutSeconds = 0
        SignOutSeconds = int(SignOutSeconds)
        EarlierSignInTime = str(LS.cell(TodayDateRow, PersonNameColumn).value)
        if EarlierSignInTime:
            EarlierSignInTime = int(EarlierSignInTime)
        else:
            EarlierSignInTime = 0

        if SignOutHours < SignInHours:
            SignOutHours += 24
        # actual "signing out" functions with said variables
        SignInTimeInSeconds = int(3600*(SignInHours) + 60*(SignInMinutes) + (SignInSeconds))
        SignOutTimeInSeconds = int(3600*(SignOutHours) + 60*(SignOutMinutes) + (SignOutSeconds))
        if 18000 in range(SignInTimeInSeconds, SignOutTimeInSeconds):
            # Basically checking if the person's is trying to get lab hours for "working" at 5 am and if so, to discount them. (prevents getting crazy times for signing out then signing back in on a different day)
            LS.update_cell(3, PersonNameColumn, '')
            print('Sorry but it appears your forgot to sign out yesterday and thus your lab hours haven\'t been recorded. If you believe this to be an error please inform either Oscar or Trent otherwise please re-enter your name to sign in.')
        elif 104400 in range(SignInTimeInSeconds, SignOutTimeInSeconds):
            # Same as above, (checking for 5 am) but for 29 am, (5 am + 24 hours, byproduct of line 145)
            LS.update_cell(3, PersonNameColumn, '')
            print('Sorry but it appears your forgot to sign out yesterday and thus your lab hours haven\'t been recorded. If you believe this to be an error please inform either Oscar or Trent otherwise please re-enter your name to sign in.')
        else:
            TotalSignInTime = SignOutTimeInSeconds - SignInTimeInSeconds + EarlierSignInTime
            LS.update_cell(TodayDateRow, PersonNameColumn, TotalSignInTime)
            LS.update_cell(3, PersonNameColumn, '')
            print('Thanks for comming ', name, ', you have been signed out at ', CurrentTime, ' on ', date.today())
    else:
        # signing in (Signintime blank)
        LS.update_cell(3, PersonNameColumn, CurrentTime)
        print('Hello ', name, ', you have been signed in at ', CurrentTime, ' on ', date.today())
    # check that it is still the same day
    if CurrentDate != str(date.today()):
        date_initialization()
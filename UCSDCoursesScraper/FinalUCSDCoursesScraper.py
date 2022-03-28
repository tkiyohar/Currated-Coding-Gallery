# -------------------------Comments-------------------------
# None
# ------------------------------------------------------------

# -------------------------Imports--------------------------
# *********************Selinium Imports*********************
import time
import sys
import datetime
import os.path
import pickle
import pprint
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# ****************Google Calendar API Imports***************
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# ************Debugging (not used in final code)************
import pickle

# ------------------------------------------------------------

# -------------------Initialization Message-------------------
print("Welcome to the UCSD WebREG to Google calendar course conversion wizard.")
print("Initializing program. Please wait, this may take a few seconds...\n")
# ------------------------------------------------------------

# --------------Calendar Service Initialization-------------
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

service = build("calendar", "v3", credentials=creds)
# ------Google Calendar Setup (all code credit to Google)-----
SCOPES = ["https://www.googleapis.com/auth/calendar"]
# If modifying these scopes, delete the file token.json.
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())
service = build("calendar", "v3", credentials=creds)
# ------------------------------------------------------------

# ------------------Selenium Browser Setup--------------------
driverLocation = r"C:\Users\trent\Downloads\PythonProjects-20211220T222447Z-001\PythonProjects\chromedriver_win32\chromedriver.exe"
driverService = Service(driverLocation)
webdriverOptions = webdriver.ChromeOptions()
webdriverOptions.add_argument(
    "headless"
)  # causes chrome to run browser in background/invisibly
# ------------------------------------------------------------

# ---------------------Webpage Addresses----------------------
webregAddress = "https://act.ucsd.edu/webreg2/start"
redirectLoginAddress = (
    r"https://a5.ucsd.edu/tritON/profile/SAML2/Redirect/SSO?execution=e1s1"
)
# test webaddress with no redirect = https://www.google.com/
# ------------------------------------------------------------

# -----------------------Variable Setup-----------------------
redirectPage = ""  # global variable. Will always be equal to the redirected page's URL given by the most recent call
# of the function "checkRedirectFrom."
savedPage = ""  # stores current.url from most recent call of savePage(). Intended for use with checkRedirectFrom and WebDriverWait.
# *******************Calendar Variables*******************
eventTemplate = {
    "summary": "",
    "location": "",
    "description": "",
    "colorId": "",
    "start": {
        "dateTime": "",
        "timeZone": "America/Los_Angeles",
    },
    "end": {
        "dateTime": "",
        "timeZone": "America/Los_Angeles",
    },
    "recurrence": [],
    "reminders": {
        "useDefault": False,
        "overrides": [],
    },
}
# Exams
examReminderOverrides = [
    {"method": "popup", "minutes": 60 * 24 * 1},
    {"method": "email", "minutes": 60 * 24 * 1},
    {"method": "popup", "minutes": 60 * 24 * 7},
    {"method": "email", "minutes": 60 * 24 * 7},
]
examRecurence = []

# Regular Courses
regularReminderOverides = [{"method": "popup", "minutes": 10}]

webRegWeekdayToBYDAYConversions = {
    "M": "MO",
    "Tu": "TU",
    "W": "WE",
    "Th": "TH",
    "F": "FR",
    "Sa": "SA",
    "Su": "SU",
}
dateRETemplate = "\d{2}/\d{2}/\d{4}"
# see "https://datatracker.ietf.org/doc/html/rfc5545" and "https://www.nylas.com/blog/calendar-events-rrules/" for more
# info on recurrences and calendar rules

sectionStartDate = ""  # set equal to the first day of each particular section in each particular course

# Event Presets
maxAttendees = 5
sendNotifications = True
sendUpdates = "all"
supportsAttachments = True
hourAdjustment = 8  # required for countering offset of GMT time
# ------------------------------------------------------------

# ----------------------Functions Setup-----------------------]
def savePage():
    savedPage == driver.current_url


def waitForResults(NewID):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, NewID))
        )
    except:
        print(r"Error: System Timeout: Page took longer than 5 seconds to load")
        driver.quit()


def checkRedirectFrom(currentPage):
    global redirectPage
    try:
        WebDriverWait(driver, 3).until(EC.url_changes(currentPage))
        redirectPage = driver.current_url  # returns new page URL
    except:
        redirectPage = currentPage  # returns current page URL after not redirecting from current page within 3 seconds


def waitUntil(condition, timeout):
    timeoutTime = time.time() + timeout
    while time.time() < timeoutTime:
        if condition():
            return True  # note that return exits the function
        time.sleep(0.25)
    return False


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + "Z"
    return dt


yearREPattern = r"\d\d\d\d"  # used in following function
yearDayMonthREPattern = r"\d{2,4}"


def convert_mmddyyyy_to_RFC_datetime(planeDate, hour=0, minute=0):
    planeDate = str(planeDate)
    year = re.findall(yearREPattern, planeDate)[0]
    monthDay = re.findall(yearDayMonthREPattern, planeDate)
    monthDay.remove(year)
    month = monthDay[0]
    day = monthDay[1]
    return (
        convert_to_RFC_datetime(year, month, day, hour, minute),
        int(year),
        int(month),
        int(day),
    )


# ------------------------------------------------------------

# ---------------------------Code-----------------------------
pp = pprint.PrettyPrinter()
driver = webdriver.Chrome(service=driverService, options=webdriverOptions)
driver.get(webregAddress)
checkRedirectFrom(webregAddress)
try:  # used so that on an error, we can execute code to properly close the selenium driver
    if (
        redirectPage[:-1] == redirectLoginAddress[:-1]
    ):  # slice opperators neccesary because of variability in last character of same webpage
        print("Initialization complete, begining program:\n")
        print("---Credentials Required---")

        # ***************************************Credentials Login****************************************
        for signInAttempts in range(1, 4):  # 3 login attempts to sign in
            username, password = input("Please Enter Your UCSD Username: "), input(
                "Please Enter Your UCSD Password: "
            )
            driver.find_element(By.ID, "ssousername").send_keys(username)
            driver.find_element(By.ID, "ssopassword").send_keys(password)
            driver.find_element(By.NAME, "_eventId_proceed").click()
            print("loading, please wait...")
            checkRedirectFrom(redirectLoginAddress)
            try:
                if signInAttempts == 3:
                    continue
                driver.find_element(
                    By.ID, "_login_error_message"
                )  # succeeds if given incorrect credentials
                print(
                    "Failed to login due to bad credentials, please try again ("
                    + str(3 - signInAttempts)
                    + " attempts remaining)"
                )
            except:  # occurs if given correct credentials
                print("Credentials accepted, login in now...")
                break
        else:  # after three failed login attempts are made
            sys.exit("error: failed to login after 3 attempts, restart program")
        # ************************************************************************************************

        # ***************************************Duo Authentication***************************************
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "duo_iframe"))
            )  # ensures initial redirect from credentials page completes before proceeding
        except:
            sys.exit(
                "Error: Failed to proceed past WebReg login page. Check your internet connection and make sure the WebReg website is online."
            )
        checkRedirectFrom(
            driver.current_url
        )  # tests in case page redirects again and doesn't require duo authentication
        try:
            driver.find_element(By.ID, "duo_iframe")
            print(
                "Duo authentication required. Please complete duo authentification now..."
            )
            if waitUntil(
                lambda: True if driver.current_url == webregAddress else False, 60
            ):  # lambda function used to pass condition to "waitUntil" function
                print(
                    "Duo authentication verified. Successfully connected to WebReg"
                )  # only runs once we reach the webreg homepage after successful authentification)
            else:
                sys.exit(
                    "error: duo authentication time out, please restart the program"
                )
        except SystemExit:  # necessary to properly handle/raise "sys.exit"s from within try/except code
            raise
        except:
            print("Duo authentication not required. Proceeding to Webreg...")
            if waitUntil(
                lambda: True if driver.current_url == webregAddress else False, 3
            ):
                print(
                    "Successfully connected to WebReg"
                )  # only runs once we reach the webreg homepage after successful authentification)
            else:
                sys.exit(
                    "error: connection to Webreg timed out, please restart the program"
                )
        # ************************************************************************************************

    elif redirectPage == webregAddress:
        print("---Login Not Required---")
        print("Procceeding to WebReg...")
    else:
        sys.exit(
            'error: redirected from "'
            + str(webregAddress)
            + '" to unexpected page "'
            + str(redirectPage)
            + '"'
        )

    # ****************************WebReg initialization and Term Selection****************************
    print("----------------------===============================----------------------")
    print("Please enter the number of the term you would like to select:")
    webregTerms = driver.find_element(By.ID, "startpage-select-term").find_elements(
        By.TAG_NAME, "option"
    )
    for termNum, term in enumerate(
        webregTerms
    ):  # enumerate creates a list that numbers the entries within a list. In this case, said list is assigned to termNum.
        print(str(termNum) + ". " + term.text)
    while True:
        if (
            termSelection := input()
        ).isdigit():  # ":=" is known as the walrus opperator and both assign and returns the value of a variable in a single execution
            if int(termSelection) <= termNum:
                termSelection = int(termSelection)
                break
        print(
            "error: unacceptable input. Please enter the corresponding number of the term you would like to select"
        )
    # termSelection = 0 #debug
    selectedTerm = webregTerms[termSelection].text
    webregTerms[termSelection].click()
    savePage()
    driver.find_element(By.ID, "start-button-cell-id").click()
    print('Loading "' + selectedTerm + '"...')
    checkRedirectFrom(savedPage)
    if savedPage == redirectPage:
        sys.exit("error: connection to Webreg timed out, please restart the program")
    print('successfully loaded "' + selectedTerm + '"')
    # ************************************************************************************************

    # *********************WebReg: Retrieve calendar info for courses from WebReg*********************
    print('Loading "' + selectedTerm + '" courses...')
    print("Please wait, this process may take a few seconds...")

    # ==========================Get information for calendar from WebReg===========================

    # <<<<<<<<<<<<<<<<<<Find Each Course's Individual Table by Rows in WebReg<<<<<<<<<<<<<<<<<<
    courseTitleRows = []
    individualCourseTables = []
    nestedSectionCatagories = []
    coursesListRows = driver.find_element(By.ID, "list-id-table").find_elements(
        By.TAG_NAME, "tr"
    )
    for (
        row
    ) in (
        coursesListRows
    ):  # used for opening all hidden course section catagories (important for future parsing)
        try:
            nestedSectionCatagories = row.find_elements(
                By.CLASS_NAME, "wr-gridrow-header-outer-class"
            )
            for nestedSectionCatagory in nestedSectionCatagories:
                nestedSectionCatagory.find_element(By.TAG_NAME, "img").click()
        except Exception:
            pass
    for rowNum, row in enumerate(
        coursesListRows
    ):  # compiles a list of each row number that contains a class title
        if not str.isspace(row.find_elements(By.TAG_NAME, "td")[0].text):
            if row.find_elements(By.TAG_NAME, "td")[0].text:
                courseTitleRows.append(rowNum)
    for rowNumNum, rowNum in enumerate(
        courseTitleRows
    ):  # compiles a list of nested lists containing all the row numbers associated with a given course
        if rowNumNum + 1 < len(courseTitleRows):
            individualCourseTables.append(
                list(range(rowNum, courseTitleRows[int(rowNumNum) + 1]))
            )
        else:
            individualCourseTables.append(list(range(rowNum, len(coursesListRows))))
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

            # <<<<<<<<<<<<<Extract useable lists of information to put into google calendar<<<<<<<<<<<<<
    pluralColumns = [
        2,
        3,
        7,
        8,
        9,
        10,
    ]  # see comments below for correlations. Used in for loop to avoid need to copy paste code for each plural list
    nonSpecificSectionCodes = (
        []
    )  # column 2: list that holds all the section codes given on webreg for a specific course (later parsed to find exact section code rather than inexact "X00" code)
    specificSectionTypes = (
        []
    )  # column 3: stores all different sessions of course (e.g., lecture, discussion, etc.)
    specificSectionDays = (
        []
    )  # column 7: stores all different days of different sessions of course
    specificSectionTimes = (
        []
    )  # column 8: stores all different meeting times of different sessions of course
    specificSectionBuildings = (
        []
    )  # column 9: stores all different building codes of different sessions of course
    specificSectionRooms = (
        []
    )  # column 10: stores all different room codes of different sessions of course
    sectionTypeDict = {
        "LE": "Lecture",
        "DI": "Discussion Session",
        "FI": "Final",
        "LA": "Lab",
        "MI": "Midterm",
        "ST": "Studio",
    }
    individualCoursesInfo = (
        []
    )  # will store each course as a nested list after successful extraction
    for courseTable in individualCourseTables:
        specificCourseTitle = (
            coursesListRows[courseTable[0]].find_elements(By.TAG_NAME, "td")[0].text
        )
        specificInstructorName = (
            coursesListRows[courseTable[0]].find_elements(By.TAG_NAME, "td")[4].text
        )
        for rowNum in range(
            len(courseTable)
        ):  # collects and compiles lists for a specific course's multi-traits (e.g., sections times)
            for columnNum, plural in enumerate(
                [
                    nonSpecificSectionCodes,
                    specificSectionTypes,
                    specificSectionDays,
                    specificSectionTimes,
                    specificSectionBuildings,
                    specificSectionRooms,
                ]
            ):
                cellText = (
                    coursesListRows[courseTable[rowNum]]
                    .find_elements(By.TAG_NAME, "td")[pluralColumns[columnNum]]
                    .text
                )
                if (
                    columnNum == 1
                ):  # excludes row if it is an empty section catagory row
                    if not cellText or str(cellText).isspace():
                        break
                plural.append(cellText)
        for (
            sectionCode
        ) in (
            nonSpecificSectionCodes
        ):  # parses specific section code from non specific section codes
            if sectionCode:
                if not str.isspace(sectionCode):
                    if int(sectionCode[-1]) != 0:
                        specificSectionCode = sectionCode
                        nonSpecificSectionCodes = []
                        break
        else:
            specificSectionCode = nonSpecificSectionCodes[0]
        for typeNum, sectionType in enumerate(
            specificSectionTypes
        ):  # converts section type codes to actual section types
            specificSectionTypes[typeNum] = sectionTypeDict[sectionType]
        completeSpecificCourseInfo = [
            specificCourseTitle,
            specificInstructorName,
            specificSectionCode,
            specificSectionTypes,
            specificSectionDays,
            specificSectionTimes,
            specificSectionBuildings,
            specificSectionRooms,
        ]
        individualCoursesInfo.append(completeSpecificCourseInfo)
        for courseAttribute in [
            "specificCourseTitle",
            "specificInstructorName",
            "specificSectionCode",
            "specificSectionTypes",
            "specificSectionDays",
            "specificSectionTimes",
            "specificSectionBuildings",
            "specificSectionRooms",
        ]:  # variable names have to be given as strings for globals()
            globals()[courseAttribute] = type(
                globals()[courseAttribute]
            )()  # emptys variable without deleting it or changing its type to prep for next course itteration
    print("Successfully loaded courses. Proceeding to calendar configuration.")
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # *************************************************************************************************

    # #debug: pickling individualCoursesInfo instance write test code for in other file
    # pickleFile = open("individualCoursesInfo.pickle", "wb")
    # pickle.dump(individualCoursesInfo, pickleFile)
    # pickleFile.close()
    # --------------Load Test Course Data Instance--------------
    # debug: pickleFile = open("individualCoursesInfo.pickle", "rb")
    # individualCoursesInfo = pickle.load(pickleFile)
    # pickleFile.close()

    # ********************Use Extracted Course Info to Create Google Calendar Events*******************
    # ---------------------------Setting Start and End dates of Quarter----------------------------
    # <<<<<<<<<<<<<<<<<<<<<<<<<initializing variables in correct scope<<<<<<<<<<<<<<<<<<<<<<<<<
    validApprovedDates = False
    validDatePattern = r"\d\d-\d\d-\d\d\d\d"
    startQuarterDate = ""
    endQuarterDate = ""
    endQuarterDatetimeDay = datetime.date(
        2002, 6, 15
    )  # decided to use B-day for initialization value as easter egg ;)
    startQuarterDatetimeDay = datetime.date(2002, 6, 15)
    startQuarterYear = 0
    startQuarterMonth = 0
    startQuarterDay = 0
    endQuarterYear = 0
    endQuarterMonth = 0
    endQuarterDay = 0
    sectionOverrides = []
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Actual Code<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    print("----------------------===============================----------------------")
    while not validApprovedDates:
        validStartDateEntry = False
        validEndDateEntry = False
        manualApproval = False

        while not validStartDateEntry:
            print(
                'Please enter the date of the first day of classes of "'
                + selectedTerm
                + '" below written in the "mm-dd-yyyy" format:'
            )
            print("(Example: 01-03-2022)")
            startQuarterDate = input()
            # startQuarterDate = "01-03-2022" #debug
            if re.fullmatch(
                validDatePattern, startQuarterDate
            ):  # ensures input is in the \d\d-\d\d-\d\d\d\d format
                try:  # ensures input is a valid date (e.g., 13/02/2022 is not a valid date because there is no 13th month)
                    (
                        startQuarterDateRFC,
                        startQuarterYear,
                        startQuarterMonth,
                        startQuarterDay,
                    ) = convert_mmddyyyy_to_RFC_datetime(startQuarterDate)
                    startQuarterDatetimeDay = datetime.date(
                        startQuarterYear, startQuarterMonth, startQuarterDay
                    )  # needed variable as datetime.date class for operations in for loop in sections below
                    validStartDateEntry = True
                except Exception:
                    print("\nError: Invalid date. Please try again:\n")

            else:
                print(
                    '\nError: Your input does not match the "mm-dd-yyyy" format. Please try again:\n'
                )
        print(
            "\nInput Accepted (this will be changeable later if you entered an incorrect date)\n"
        )

        while not validEndDateEntry:
            print(
                'Next, please enter the date of the last day of classes of "'
                + selectedTerm
                + '" below written in the "mm-dd-yyyy" format:'
            )
            print("(Example: 03-19-2022)")
            endQuarterDate = input()
            # endQuarterDate = "03-19-2022" #debug
            if re.fullmatch(
                validDatePattern, endQuarterDate
            ):  # ensures input is in the \d\d-\d\d-\d\d\d\d format
                try:  # ensures input is a valid date (e.g., 13/02/2022 is not a valid date because there is no 13th month)
                    (
                        endQuarterYear,
                        endQuarterMonth,
                        endQuarterDay,
                    ) = convert_mmddyyyy_to_RFC_datetime(endQuarterDate)[1:]
                    endQuarterDatetimeDay = datetime.date(
                        endQuarterYear, endQuarterMonth, endQuarterDay
                    )  # used in following section to ensure that input end date is after input start date
                    endQuarterDatetimeDay -= datetime.timedelta(
                        days=6
                    )  # the last 7 days of the quarter are for finals and will thus not have normal courses during them.
                    validEndDateEntry = True
                except Exception:
                    print("\nError: Invalid date. Please try again:\n")
            else:
                print(
                    '\nError: Your input does not match the "mm-dd-yyyy" format. Please try again:\n'
                )

        if (
            startQuarterDatetimeDay >= endQuarterDatetimeDay
        ):  # ensures end date is after start date
            print(
                "\nError: The time between the start and end dates is less than 8 days or the end date comes before the start date."
            )
            print("Please reenter a valid start and end date combination:\n")
        else:
            print("\nInput Accepted.\n")
            while (
                not manualApproval
            ):  # requires user to confirm date inputs before proceeding to calendar event creation
                print(
                    "Is the following information correct? (Y/N):\n"
                    + "------------\n"
                    + "Start Date: "
                    + startQuarterDate
                    + "\n"
                    + "End Date: "
                    + endQuarterDate
                    + "\n"
                    + "------------"
                )
                yesNo = input()
                if yesNo in ("y", "Y"):
                    print("\nInputs accepted. Begining creation of calendar events...")
                    print("Please wait, this process may take a few moments...")
                    manualApproval = True
                    validApprovedDates = True
                elif yesNo in ("n", "N"):
                    print("\nInputs recinded. Please reenter your dates:")
                    manualApproval = True
                else:
                    print(
                        '\nError: Invalid input, please enter either "Y" for "Yes" or "N" for "No"\n'
                    )
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # ---------------------------------------------------------------------------------------------

    # -------------Creating/Recreating Calendar Instance To Be Filled In By Later Code------------
    currentCalendarsNamesToID = (
        {}
    )  # used to contain the correlating IDs of all existing calendars to their names
    customCalendarTitle = "UCSD " + selectedTerm[-4:] + " " + selectedTerm[:-5]
    UCSDCoursesCalendarMetaData = {
        "summary": customCalendarTitle,
        "description": "This calendar has been created autonomously using Python. Do not add to it otherwise your events may be deleted",
        "timeZone": "America/Los_Angeles",
    }
    for individualCalendar in service.calendarList().list().execute()["items"]:
        currentCalendarsNamesToID[individualCalendar["summary"]] = individualCalendar[
            "id"
        ]
    if customCalendarTitle in currentCalendarsNamesToID:
        service.calendarList().delete(
            calendarId=currentCalendarsNamesToID[customCalendarTitle]
        ).execute()
    UCSDCalendar = (
        service.calendars().insert(body=UCSDCoursesCalendarMetaData).execute()
    )
    UCSDCalendarID = UCSDCalendar["id"]  # needed later for event creation

    # ---For loop specific variables and for loop for initializing startWeekdaysDatesList values---
    startQuarterWeekday = datetime.date(
        startQuarterYear, startQuarterMonth, startQuarterDay
    ).weekday()  # gets weekday of start date ("0-6 -> mon-sun"); important for determining start date of individual repeating events
    startWeekdaysDatesList = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]  # terms 0-6 correlate to mon-sun respectively
    nextDays = 0  # used to iterate through proceeding weekdays (following start date) in for loop below
    datetimeDayIterate = startQuarterDatetimeDay
    for Weekdays in range(
        len(startWeekdaysDatesList)
    ):  # basically just for 7 iterations loop
        startWeekdaysDatesList[startQuarterWeekday + nextDays] = datetimeDayIterate
        nextDays += 1
        if startQuarterWeekday + nextDays > 6:
            nextDays = -startQuarterWeekday
        datetimeDayIterate = datetimeDayIterate + datetime.timedelta(days=1)

    # -----------------Adding Events to Calendar-----------------
    for course in individualCoursesInfo:
        classTitle = course[0]
        classTeacher = course[1]
        classSection = course[2]
        for Section in enumerate(course[3]):
            Section = Section[
                0
            ]  # parses tuples from enumerate into pure numbers of list items
            # >>>>>>>>>>>>>>>>>>Section Type (course[3])>>>>>>>>>>>>>>>>>>
            sectionType = course[3][Section]
            # Color to numbers chart: https://lukeboyle.com/blog/posts/google-calendar-api-color-id
            if sectionType == "Lecture":
                eventColor = 9  # dark blue 9
            elif sectionType == "Discussion Session":
                eventColor = 1  # light blue 1
            elif sectionType == "Final":
                eventColor = 11  # red 11
            elif sectionType == "Lab":
                eventColor = 2  # light green 2
            elif sectionType == "Midterm":
                eventColor = 5  # yellow 5
            elif sectionType == "Studio":
                eventColor = 3  # purple 3
            else:
                sys.exit("error: invalid section type")
            # >>>>>>>>>>>>>>>>>>Section Meeting Days (course[4])>>>>>>>>>>>>>>>>>>
            sectionMeetingDays = course[4][Section]
            if (
                re.search(dateRETemplate, sectionMeetingDays) is not None
            ):  # gets triggered if section is a one-time event/exam that has its exact date listed (applies to finals and midterms)
                sectionStartDate = re.findall(dateRETemplate, sectionMeetingDays)[0]
                sectionOverrides = examReminderOverrides
                if (
                    "recurrence" in eventTemplate
                ):  # removes recurrence parameter from calendar metadata when not used if present
                    eventTemplate.pop("recurrence")
                (
                    sectionStartDateYear,
                    sectionStartDateMonth,
                    sectionStartDateDay,
                ) = convert_mmddyyyy_to_RFC_datetime(sectionStartDate)[1:]
                sectionStartDate = datetime.date(
                    sectionStartDateYear, sectionStartDateMonth, sectionStartDateDay
                )
            else:  # if section is not a final or midterm
                # ----------synthesizes custom RRULE based on days that specific section occurs----------
                eventTemplate["recurrence"] = [""]
                sectionOverrides = regularReminderOverides
                regularRecurence = ["RRULE:FREQ=WEEKLY"]
                endQuarterDateRFC = convert_mmddyyyy_to_RFC_datetime(
                    endQuarterDatetimeDay
                )[
                    0
                ]  # adds "UNTIL" parameter with end date to RRule to prevent courses from repeating indefinitely
                endQuarterDateRFCReformated = endQuarterDateRFC.replace("-", "")
                endQuarterDateRFCReformated = endQuarterDateRFCReformated.replace(
                    ":", ""
                )
                regularRecurence[0] += (
                    ";UNTIL=" + endQuarterDateRFCReformated + ";BYDAY="
                )
                sectionDaysList = (
                    []
                )  # used with for loop below to create iterable list of days for parsing in proceeding code
                for day in webRegWeekdayToBYDAYConversions:
                    if day in sectionMeetingDays:
                        sectionDaysList.append(
                            startWeekdaysDatesList[
                                list(webRegWeekdayToBYDAYConversions.keys()).index(day)
                            ]
                        )  # appends each of the dates of the first weekday of the quarter that each section will meet on (e.g., if a section meets on M and Tu, this line will append the dates of the first M and Tu of the quarter)
                        if regularRecurence[0][-6:] == "BYDAY=":
                            regularRecurence[0] += webRegWeekdayToBYDAYConversions[day]
                        else:
                            regularRecurence[0] += (
                                "," + webRegWeekdayToBYDAYConversions[day]
                            )
                sectionStartDate = min(
                    sectionDaysList
                )  # Sets section Start Date based off of the soonest weekday it meets on relative to the start of the quarter
            # >>>>>>>>>>>>>>>>Section Meeting Day Times (course[5])>>>>>>>>>>>>>>>
            # everything in this section is just used to determine the RFC start and end times of the first time the section meets during the quarter
            sectionMeetingTimes = course[5][Section]
            sectionStartTime, sectionEndTime = str(sectionMeetingTimes).split("-")
            sectionStartTimeHours, sectionStartTimeMinutes = str(
                sectionStartTime[:-1]
            ).split(":")
            sectionEndTimeHours, sectionEndTimeMinutes = str(sectionEndTime[:-1]).split(
                ":"
            )

            # -----Converting am-pm time input into miltitary time output-----
            if sectionEndTimeMinutes == "00":
                sectionEndTimeMinutes = sectionEndTimeMinutes[0]
            if sectionStartTimeMinutes == "00":
                sectionStartTimeMinutes = sectionStartTimeMinutes[0]
            sectionStartTimeHours = int(sectionStartTimeHours)
            sectionEndTimeHours = int(sectionEndTimeHours)
            sectionStartTimeMinutes = int(sectionStartTimeMinutes)
            sectionEndTimeMinutes = int(sectionEndTimeMinutes)
            if sectionStartTime[-1] == "p":
                if sectionStartTimeHours != 12:
                    sectionStartTimeHours += 12
            elif sectionStartTimeHours == 12:
                sectionStartTimeHours = 0
            if sectionEndTime[-1] == "p":
                if sectionEndTimeHours != 12:
                    sectionEndTimeHours += 12
            elif sectionEndTimeHours == 12:
                sectionEndTimeHours = 0
            sectionStartTimeHours += hourAdjustment
            sectionEndTimeHours += hourAdjustment
            if sectionStartTimeHours >= 24:
                sectionStartTimeHours -= 24
            if sectionEndTimeHours >= 24:
                sectionEndTimeHours -= 24
            # ----------------------------------------------------------------

            sectionStartDateRFC = convert_mmddyyyy_to_RFC_datetime(
                sectionStartDate, sectionStartTimeHours, sectionStartTimeMinutes
            )[0]
            sectionEndDateRFC = convert_mmddyyyy_to_RFC_datetime(
                sectionStartDate, sectionEndTimeHours, sectionEndTimeMinutes
            )[
                0
            ]  # Note: Yes, this is supposed to say "sectionStartDate"
            # >>>>>>>>>>>>>>>Section Location (course[6] + course[7])>>>>>>>>>>>>>
            sectionRoom, sectionRoomNumber = course[6][Section], course[7][Section]
            sectionLocation = sectionRoom + " " + sectionRoomNumber
            # >>>>>>>>>>>>>>>>>>>>Set Event Template Values>>>>>>>>>>>>>>>>>>>>>>>
            eventTemplate["summary"] = classTitle + ": " + sectionType
            eventTemplate["location"] = sectionLocation
            eventTemplate["description"] = (
                "Proffesor: " + classTeacher + "\nSection Code: " + classSection
            )
            eventTemplate["colorId"] = eventColor
            eventTemplate["start"]["dateTime"] = sectionStartDateRFC
            eventTemplate["end"]["dateTime"] = sectionEndDateRFC
            eventTemplate["reminders"]["overrides"] = sectionOverrides
            if "recurrence" in eventTemplate:
                eventTemplate["recurrence"] = regularRecurence
            # >>>>>>>>>>>>>>>>>>>>>>Creating Section Event>>>>>>>>>>>>>>>>>>>>>>>>
            event = (
                service.events()
                .insert(
                    calendarId=UCSDCalendarID,
                    maxAttendees=maxAttendees,
                    sendNotifications=sendNotifications,
                    sendUpdates=sendUpdates,
                    supportsAttachments=supportsAttachments,
                    body=eventTemplate,
                )
                .execute()
            )
            time.sleep(3)
    print(
        "\nSuccessfully created Google calendar events from selected WebREG courses. Exiting Program."
    )
    # *************************************************************************************************

except:  # runs on error in code and raises said error after closing the selinium driver
    driver.quit()
    raise
finally:
    driver.quit()

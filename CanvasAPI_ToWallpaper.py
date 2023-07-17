#References:
# https://www.w3schools.com/python/python_datetime.asp
# https://canvas.instructure.com/doc/api/index.html
# https://canvasapi.readthedocs.io/en/stable/index.html
# https://github.com/ucfopen/canvasapi#documentation
# https://codebeautify.org/python-formatter-beautifier
# https://en.wikipedia.org/wiki/ISO_8601
from canvasapi import Canvas #Our Canvas API wrapper
import datetime #used to interact with dates
import json #used to write to the file schedule+notes.js
import pytz #We use this to convert the date and times to US Eastern Standard Time

info_file  = open('private.json')
private_info = json.load(info_file)

#The file that we use to update the schedule on my desktop
SCHEDULE_FILEPATH = private_info["SCHEDULE_FILEPATH"]

#My Canvas URL and Access Token
API_URL = private_info["API_URL"]
API_KEY = private_info["API_KEY"]

#How we interact with the Canvas API
canvas = Canvas(API_URL, API_KEY)

#Variable to store the schedule in.
scheduleNote = {
    "Sunday": [],
    "Monday": [],
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": [],
    "Saturday": []
}

#First test at using this CanvasAPI wrapper 
def courseList():
    courses = canvas.get_courses(enrollment_state="active")
    for course in courses:
        print(course)
#^works pretty well except without the enrollment state parameter it gives an error
#probably something to do with old removed courses

#UNUSED
#This should list future stuff but I need to configure it to how far in the future
#Lets try for a week in the future
#Not Printing anything originally
def getUpcomingAssignments():
    ucas = canvas.get_calendar_events(type="assignment", end_date=getAWeekFromNow())
    for uca in ucas:
        print(uca)

#UNUSED
def getAWeekFromNow():
    return (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d") 

#Method to add our Schedule items to our schedule variable.
def generateSchedule(hour, activity, day):
    match day:
        case 0:
            scheduleNote["Monday"].append({"hour":hour, "activity": activity})
        case 1:
            scheduleNote["Tuesday"].append({"hour":hour, "activity": activity})
        case 2:
            scheduleNote["Wednesday"].append({"hour":hour, "activity": activity})
        case 3:
            scheduleNote["Thursday"].append({"hour":hour, "activity": activity})
        case 4:
            scheduleNote["Friday"].append({"hour":hour, "activity": activity})
        case 5:
            scheduleNote["Saturday"].append({"hour":hour, "activity": activity})
        case 6:
            scheduleNote["Sunday"].append({"hour":hour, "activity": activity})
        case _:    
            print("Error invalid Day")
    


#Main Function call
def getWhatIGotTodo():
    todos = canvas.get_todo_items()
    for todo in todos:
        today = datetime.date.today()
        margin = datetime.timedelta(days = 7)
        duedate = datetime.datetime.fromisoformat(todo.assignment["due_at"])
        duedate = duedate.astimezone(pytz.timezone('America/New_York'))
        if duedate.date() <= (today + margin):
            #print(todo.assignment["name"] + " " + str(duedate.weekday()))
            generateSchedule(duedate.strftime("%H:%M"), todo.assignment["name"], duedate.weekday())
        #break
    #print(json.dumps(scheduleNote))
    outputString = 'var scheduleNotes = { "Schedule":' + json.dumps(scheduleNote) +',"Notes": ["EMPTY NOTE <u>Empty value</u>","EMPTY NOTE <u>Empty value</u>"]}'
    writeToScheduleScript(outputString)

#Method we use to write to the Schedule Javascript file
def writeToScheduleScript(schedule):
    f = open(SCHEDULE_FILEPATH, "w")
    f.write(schedule)
    f.close()

#Call of our Script
getWhatIGotTodo()
#getUpcomingAssignments()
#print(getAWeekFromNow())
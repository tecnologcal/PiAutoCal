import datetime
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
]

filePath = os.path.dirname(__file__)
relativePath = "/secrets/credentials.json"
newPath = os.path.join(filePath, relativePath)
tokenFolder = os.path.join(filePath, "secrets")  # Define a folder for tokens
tokenPath = os.path.join(tokenFolder, "token.json")


if not os.path.exists(tokenFolder):
    os.makedirs(tokenFolder)


def authenticate():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenPath):
        creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                newPath,
                SCOPES,
            )

            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, "w") as tokenFile:
            tokenFile.write(creds.to_json())
    return creds


def getGoogleCourses(service):

    response = service.courses().list().execute()
    courses = response.get("courses", [])
    processedCourses = {}

    for course in courses:

        courseState = course.get("courseState")

        if courseState == "ACTIVE":

            courseName = course.get("name")
            courseID = course.get("id")
            processedCourses[courseName] = courseID

    print(processedCourses)
    return processedCourses


def getGoogleAssignments(service, courses):

    today = datetime.datetime.today()

    allInfo = {}

    for courseName, courseID in courses.items():

        courseAssignmentList = {}

        response = service.courses().courseWork().list(courseId=courseID).execute()
        courseAssignments = response.get("courseWork", [])

        # print(courseAssignments)
        for assignment in courseAssignments:

            # duedates and duetimes are in a list of their own, this proccess goes through and makes it a standard date time object
            dueDates = assignment.get("dueDate")
            dueTimes = assignment.get("dueTime", {"hours": 0, "minutes": 0})

            dueHour = dueTimes.get("hours", 0)
            dueMinute = dueTimes.get("minutes", 0)

            if not dueDates:
                continue

            dueDate = f"{dueDates.get("year")}-{dueDates.get("month")}-{dueDates.get("day")} {dueHour}:{dueMinute}"
            dueDate = datetime.datetime.strptime(dueDate, "%Y-%m-%d %H:%M")

            if dueDate <= today:
                continue

            assignmentName = assignment.get("title")
            courseAssignmentList[assignmentName] = dueDate.strftime("%Y-%m-%d %I:%M")

            allInfo[courseName] = courseAssignmentList

    return allInfo


creds = authenticate()

service = build("classroom", "v1", credentials=creds)

courses = getGoogleCourses(service)
print(json.dumps(getGoogleAssignments(service, courses), indent=2))

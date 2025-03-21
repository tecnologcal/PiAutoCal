import requests
import json
import datetime
from datetime import timedelta

apiKey = "10497~9y9GuaPBT2CMcmwmJ6uCBARAXWykLZXCZEF6VeNGWkAtGWZEU42VMeDJtBJDwEz9"
baseURL = "https://mvla.instructure.com"
userID = "100032385"

# find the Id and filter out older courses
currentEnrollmentID = 265
processedCourses = {}


headers = {"Authorization": f"Bearer {apiKey}"}


def getCourses():
    url = f"{baseURL}/api/v1/users/self/courses"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        rawCourses = response.json()
        processedCourses = {}

        for rawCourse in rawCourses:

            if "name" in rawCourse and "enrollment_term_id" in rawCourse:
                enrollmentID = rawCourse["enrollment_term_id"]
                if enrollmentID == currentEnrollmentID:
                    courseName = rawCourse.get("name")
                    courseID = rawCourse.get("id")
                    processedCourses[courseName] = courseID

        print(processedCourses)
        return processedCourses
    else:
        print("Error has occurred while getting classes")


def getAssignments(courses):
    for courseName, courseID in courses.items():
        url = f"{baseURL}/api/v1/courses/{courseID}/assignments"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:

            rawAssignments = response.json()
            print(rawAssignments)

        else:
            print("Error getting assignments")


courses = getCourses()
getAssignments(courses)

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
        
    today = datetime.date.today()
    print(today)
    allInfo = {}
    
    for courseName, courseID in courses.items():
        url = f"{baseURL}/api/v1/courses/{courseID}/assignments?per_page=50"

        courseAssignmentList = {}
        
        
        while url: 
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                rawAssignments = response.json()
            
                
                for assignment in rawAssignments:
                    
                    dueDate = assignment.get('due_at')
                    if not dueDate:
                        continue
                    
                    dueDate = datetime.datetime.strptime(dueDate, "%Y-%m-%dT%H:%M:%SZ").date()
                    
                    if dueDate < today:
                        continue
                    
                    
                    
                    assignmentName = assignment.get('name')
                    if assignmentName:
                        courseAssignmentList[assignmentName] = dueDate.strftime("%Y-%m-%d")

                next_url = None
                if 'link' in response.headers:
                    links = response.headers['link'].split(',')
                    for link in links:
                        if 'rel="next"' in link:
                            next_url = link[link.find("<") + 1: link.find(">")]
                            break

                url = next_url  
           
            else:
                print(f"Error getting assignments for {courseName}")
                
        allInfo[courseName] = courseAssignmentList     
                       
    print(json.dumps(allInfo, indent=2))
    return allInfo


courses = getCourses()
getAssignments(courses)

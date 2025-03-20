import requests
import json


apiKey = "10497~9y9GuaPBT2CMcmwmJ6uCBARAXWykLZXCZEF6VeNGWkAtGWZEU42VMeDJtBJDwEz9"
baseURL = "https://mvla.instructure.com"
userID = "100032385"

headers = {"Authorization": f"Bearer {apiKey}"}


def getCourses():
    url = f"{baseURL}/api/v1/users/self/courses"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        rawCourses = response.json()
        print(rawCourses)
        processedCourses = []

        for rawCourse in rawCourses:
            enrollmentStatus = rawCourse["enrollment_state"]
            if "name" in rawCourse and enrollmentStatus == "active":
                course = rawCourse["name"]
                processedCourses.append(course)
                print(processedCourses)

    else:
        print("Error has occurred while getting classes")


getCourses()

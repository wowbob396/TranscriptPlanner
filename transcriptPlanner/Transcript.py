from Degree import Degree

import json
import ast

class Transcript:
    """
        This class will take a catalog of courses, and read them into an array.
        This course will use an Auditor object to handle the auditing of the transcript's courses
        with respect to a given degree.
    """
    def __init__(self,major, courses=[]):
        self.courses = courses
        self.major = major
    
    def audit_transcript(self,degree):
        """
            This method takes in a degree, and compares it with the transcript's 
            completed courses
        """

        # contains a list of degree requirement objects
        response = []

        for i in range(len(degree.degree_requirements)):

            # adding an empty dictionary to the response list.
            response.append({})
            
            # completed property contains the number of instances where the transcript has a degree requirement course
            response[i]['completed'] = 0
            
            # this list contains all the original courses for the requirement.  This will be used 
            response[i]['all_courses'] = degree.degree_requirements[i]['courses']
            response[i]['diff'] = []
    
            for j in range(len(degree.degree_requirements[i]['courses'])):
                if degree.degree_requirements[i]['courses'][j] in self.courses:
                    response[i]['completed'] += 1
                else:
                    response[i]['diff'].append(degree.degree_requirements[i]['courses'][j])

            # if the count for the requirement met is greater than or equal to what the degree requires, then we have satisfied the requirement
            response[i]['requirement_met'] = (response[i]['completed'] >= degree.degree_requirements[i]['required'])

        print(response)
        return response

    def load_transcript(self, file):

        with open(file) as json_file:
            data = json_file.read()
            data = ast.literal_eval(data)
            self.courses = data['courses']
            self.major = data['major']
            print(self.courses)


t = Transcript('Computer Science')

d = Degree('Computer Science')
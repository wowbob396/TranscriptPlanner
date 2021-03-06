import json
import csv


class Course:
    def __init__(self, id, name, credit, prereqs, courseNum,  offeredIn, description, department):
        self.id = id
        self.name = name
        self.credit = credit
        self.prereqs = prereqs
        self.courseNum = courseNum
        self.offeredIn = offeredIn
        self.description = description
        self.department = department

    def to_JSON(self):
        return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)

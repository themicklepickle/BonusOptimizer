import re


class course:
	def __init__(self, name, workList):
		self.name = name
		self.workList = workList

	def __repr__(self):
		return str(self.workList)

	def add_details(self, quizzes, assignments, projects, notPerfect):
		self.quizzes = quizzes
		self.assignments = assignments
		self.projects = projects
		self.notPerfect = notPerfect

	def quizzes_avg(self):
		percentages = [work.mark / work.denominator * work.weight for work in self.quizzes]
		weights = [work.weight for work in self.quizzes if work.mark != 0]
		if weights != []:
			average = sum(percentages) / sum(weights) * 100
			return average
		else:
			return 0

	def assignments_avg(self):
		percentages = [work.mark / work.denominator * work.weight for work in self.assignments]
		weights = [work.weight for work in self.assignments if work.mark != 0]
		if weights != []:
			average = sum(percentages) / sum(weights) * 100
			return average
		else:
			return 0

	def projects_avg(self):
		percentages = [work.mark / work.denominator * work.weight for work in self.projects]
		weights = [work.weight for work in self.projects if work.mark != 0]
		if weights != []:
			average = sum(percentages) / sum(weights) * 100
			return average
		else:
			return 0

	def quizzes_weight(self):
		marks = [work.mark for work in self.quizzes]
		if sum(marks) != 0:
			return 25
		else:
			return 0

	def assignments_weight(self):
		marks = [work.mark for work in self.assignments]
		if sum(marks) != 0:
			return 25
		else:
			return 0

	def projects_weight(self):
		marks = [work.mark for work in self.projects]
		if sum(marks) != 0:
			return 50
		else:
			return 0

	def overall_avg(self):
		percentages = [self.quizzes_avg() * 25, self.assignments_avg() * 25, self.projects_avg() * 50]
		weights = [self.quizzes_weight(), self.assignments_weight(), self.projects_weight()]
		average = sum(percentages) / sum(weights)
		return average


class work:
	def __init__(self, name, mark, weight, denominator, category, course):
		self.name = name
		self.mark = mark
		self.weight = weight
		self.denominator = denominator
		self.course = course
		self.category = category

	def __repr__(self):
		# return str([self.name, self.mark, self.weight, self.denominator, self.course, self.category])
		return self.name


def total_average(courses):
	percentages = [course.overall_avg() for course in courses]
	return sum(percentages) / len(percentages)


fileName = "Programming15.txt"

courseNames = [
	"CSE1010a - Computer Science 1",
	"CSE1110b - Structured Programming 1", 
	"CSE1120b - Structured Programming 2", 
	"CSE2110c - Procedural Programming 1", 
	"CSE2120c - Data Structures 1"
]

specialNames = ["Assignments", "Quizzes", "Projects"]

with open(fileName, "r") as file:
	data = file.read()

rows = [row.split("</td>")[:-1] for row in data.split("<tr>")[2:]]

courses = []
courseWork = []
count = 0
for i, row in enumerate(rows):
	values = []
	courseName = courseNames[count]
	for col in row:
		match = re.search(r'ue=".*?"|px">.*?<', col)
		if match != None:
			values.append(match.group()[4:-1])
	if values == []:
		count += 1
		courses.append(course(courseName, courseWork))
		courseWork = []
	elif values[0] in specialNames:
		category = values[0]
	elif values[1] == "":
		courseWork.append(work(values[0], 0, float(values[2]), float(values[3]), category, courseName))
	else:
		courseWork.append(work(values[0], float(values[1]), float(values[2]), float(values[3]), category, courseName))
	
count += 1
courses.append(course(courseName, courseWork))

for course in courses:
	quizzes = []
	assignments = []
	projects = []
	notPerfect = []
	for i in range(len(course.workList)):
		if course.workList[i].category == "Quizzes":
			quizzes.append(course.workList[i])
		if course.workList[i].category == "Assignments":
			assignments.append(course.workList[i])
		if course.workList[i].category == "Projects":
			projects.append(course.workList[i])
		if course.workList[i].mark != course.workList[i].denominator and course.workList[i].mark != 0:
			notPerfect.append(course.workList[i])
	course.add_details(quizzes, assignments, projects, notPerfect)

changes = []
AVERAGE = total_average(courses)
for course in courses:
	COURSE_AVERAGE = course.overall_avg()
	for work in course.notPerfect:
		temp = work.mark
		if work.denominator - work.mark > 1:
			work.mark += 1
		else:
			work.mark = work.denominator
		change = total_average(courses) - AVERAGE
		course_change = course.overall_avg() - COURSE_AVERAGE
		changes.append((work, change, course_change, work.mark))
		work.mark = temp

def change(element):
	return element[1]

changes.sort(key=change, reverse=True)

with open("OptimalBonuses.txt", "w") as file:
	file.write(f"Average: {total_average(courses)}\n\n")
	for change in changes:
		c = change[0]
		file.write(f"{c.course} --> {c.category} --> {c.name}\ntotal change: {str(change[1])}\nmodule change: {str(change[2])}\nold mark: {str(c.mark)}/{str(c.denominator)}\nnew mark: {str(change[3])}/{str(c.denominator)}\n\n")
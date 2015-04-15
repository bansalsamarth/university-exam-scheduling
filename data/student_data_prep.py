def clean_courses(course_list):
	res = []
	for crs in course_list:
		if crs[-1].isalpha():
			res.append(crs[:-1])
		else:
			res.append(crs)
	return res

import json

f = open('data_student_courses.txt')

students = {}

for i in f:
    d = i.split(",")
    clean = []
    for j in d:
    	t = j.replace("\r\n", "")
    	clean.append(t)

    students[clean[0]] = clean_courses(clean[1:])

data = json.dumps(students)

out = open('data_student.json', 'w')
out.write(data)
import json

f = open('data_course_students.txt')

courses = {}

for i in f:
	d = i.split(",")
	try:
		d.remove('\r\n')
	except:
		pass
	try:
		if d[0][-1].isalpha():
			c = d[0][:-1]
		else:
			c = d[0]

		if c in courses.keys():
			courses[c] += d[1:]
		else:
			courses[c] = d[1:]
	except:
		pass

data = json.dumps(courses)

out = open('data_course.json', 'w')
out.write(data)

#with open('data_cj.json', 'w') as outfile:
#    json.dump(data, outfile)

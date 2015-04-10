import json

f = open('data_course_students.txt')

courses = {}

for i in f:
    d = i.split(",")
    try:
        d.remove('\r\n')
    except:
        pass
    courses[d[0]] = d[1:]

data = json.dumps(courses)

out = open('data_course.json', 'w')
out.write(data)

#with open('data_cj.json', 'w') as outfile:
#    json.dump(data, outfile)

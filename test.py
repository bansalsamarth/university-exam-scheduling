def color_num(color, TIME_SLOTS):
	return (color.day)*(TIME_SLOTS) + color.slot

def test_for_clash(students, TIME_SLOTS):
	clash = []

	for student in students:
		a = []
		for crs in student.courses_enrolled:
			if crs.color:
				a.append(color_num(crs.color, TIME_SLOTS))
				if len(a)!=len(set(a)):
					clash.append(student.roll_no)

def check_three_exam_constraint(student, courses):
	days = []

	for i in courses:
		days.append(i.color.day)

	b = list(set(days))

	c = []
	for i in b:
		c.append(days.count(i))

	count = {}
	for i in c:
		if i in count.keys():
			count[i] +=1
		else:
			count[i] = 1

	student.count = count

	if 3 in count.keys():
		return False
	
	return True

def slot_difference(student, courses, TIME_SLOTS):

	color_number = [color_num(i.color, TIME_SLOTS) for i in courses].sort()

	diff = []
	if not color_number:
		return 0
	for i in range(len(color_number) - 1):
		diff.append(color_number[i+1] - color_number[i])

	res = [i>=3 for i in diff]
	failed = res.count(False)
	student.slot_diff = failed

	return failed



def test_constraints(students, TIME_SLOTS):
	not_alloted = []
	three_fails = []
	slot_fails = []
	for student in students:
		flag = 0
		courses = []
		for crs in student.courses_enrolled:
			if crs.color:
				courses.append(crs)
			else:
				not_alloted.append(crs)
			check1 = check_three_exam_constraint(student, courses)

			if not check1:
				three_fails.append(student)			

			if courses:
				check2 = slot_difference(student, courses, TIME_SLOTS)
				if check2:
					flag = 1
		if flag:
			slot_fails.append(student)
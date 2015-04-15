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
					print a, set(a)
					clash.append(student.roll_no)
	
	print "Clash for : ", len(set(clash)), " Total : ", len(students)

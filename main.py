import numpy as np
import json, operator

MAX_SCHEDULE_DAYS = 8
TIME_SLOTS = 5

GAMMA = 0.5 #Change to proivde a different coloring scheme

class Course:
    def __init__(self, id, code, student_list, old_day, old_slot):
        self.id = id
        self.course_code = code
        self.student_list = student_list
        self.no_of_students = len(student_list)
        self.degree = 0
        self.max_adjacency = 0
        #self.concurrency_level = 0 #No of rooms required
        self.adjacency_list = []
        self.color = None #Assign a color object here
        self.lecture_hall = []
        self.old_day = old_day
        self.old_slot = old_slot

    def ordered_adjacency_list(self):
        #What is order?
        return self.adjacency_list

    def assign_color(self, color):
        self.color = color
        color.courses.append(self)
        print "Assigned : ", self.course_code, color.day, color.slot
        #Anything else?
        return None

class Color:
    def __init__(self, day, slot):
        self.lecture_halls = []
        self.day = day
        self.slot = slot
        self.courses = []

    def capacity_available(self):
        #Returns max students that can be accomodated
        capacity = 0
        for i in self.lecture_halls:
            capacity += i.availability()['total']
        return capacity

    def lecture_hall_list(self):

        available_halls = []
        for i in self.lecture_halls:
            if i.availability()['total']>0:
                available_halls.append(i)
        return available_halls

class LectureHall:
    def __init__(self, number, odd_capacity, even_capacity, color):
        self.number = number
        self.color = color
        
        color.lecture_halls.append(self)

        #O implies that odd/even seats are not occupied. 
        #1 implies that odd/even seats are occupied
        self.odd = 1
        self.even = 1

        self.odd_capacity = odd_capacity
        self.even_capacity = even_capacity

    def availability(self):
        if self.odd and self.even:
            return {
                "total": max(self.odd_capacity, self.even_capacity),
                "seats": (self.odd_capacity, self.even_capacity)
            }

        elif self.odd:
            return {
                "total" : self.odd_capacity,
                "seats" : (self.odd_capacity, 0)
            }

        elif self.even:
            return {
                "total" : self.even_capacity,
                "seats" : (0, self.even_capacity)
            }

        else:
            return {
                "total" : 0,
                "seats" : (0,0)
            }

class Student:
    def __init__(self, roll_no, courses):
        #self.name = name
        self.roll_no = roll_no
        self.courses_enrolled = courses

    def fairness_quotient(self):
        pass

def calculate_common_students(c1, c2):
    return len(list(set(c1.student_list).intersection(c2.student_list)))

def calculate_degree(matrix, courses):
    for i in range(len(courses)):
        courses[i].degree = np.sum(matrix[i]!= 0)

def initiailize_colors(MAX_SCHEDULE_DAYS, TIME_SLOTS):
    color_matrix = [[0 for x in range(TIME_SLOTS)] for x in range(MAX_SCHEDULE_DAYS)] 

    for day in range(MAX_SCHEDULE_DAYS):
        for slot in range(TIME_SLOTS):
            new_color = Color(day, slot)
            color_matrix[day][slot] = new_color

    return color_matrix

def build_weight_matrix():
    with open('data/data_course.json') as data_file:
        course_data = json.load(data_file)

    with open('data/mid_sem_exam_schedule.json') as data_file:
        exam_data = json.load(data_file)

    courses=[]
    counter = 1
    err_courses = []
    for course_code, students in course_data.iteritems():
        try:
            old_day, old_slot = exam_data[course_code][0], exam_data[course_code][1]
            courses.append(Course(counter, course_code, students, old_day, old_slot))
        except:
            err_courses.append(course_code)
            courses.append(Course(counter, course_code, students, 0, 0))
        counter+=1
    print "These courses didn't have exam data : ", err_courses
    print "Total : ", len(err_courses)

    total = len(courses)
    graph = np.zeros([total, total])

    #Assigning weights to matrix
    for i in range(total):
        for j in range(i+1, total):
            graph[i,j] = calculate_common_students(courses[i], courses[j])
            graph[j,i] = graph[i,j]

    #To add adjacent courses for every courses in the adjacency list
    for i in range(total):
        courses[i].max_adjacency = max(graph[i])
        for j in range(i+1, total):
            if graph[i,j]:
                courses[i].adjacency_list.append(courses[j])
                courses[j].adjacency_list.append(courses[i])
    
    return graph, courses

def initialize_lecture_halls(color_matrix):
    with open('data/lecture_halls.json') as data_file:
        data = json.load(data_file)

    lhc = []

    for j in range(MAX_SCHEDULE_DAYS):
        for k in range(TIME_SLOTS):
            color = color_matrix[j][k]
            for number, capacity in data.iteritems():
                lec_hall = LectureHall(number, capacity[0], capacity[1], color)
                lhc.append(lec_hall)
                color.lecture_halls.append(lec_hall)
    return lhc

def initialize_students():
    with open('data/data_student.json') as data_file:
        data = json.load(data_file)

    student_list = []

    for roll, courses in data.iteritems():
        student_list.append(Student(roll, courses))

    return student_list

def dis_2(color_1, color_2):
    return abs(color_1.day - color_2.day)

def dis_1(color_1, color_2):
    #raisse exception if days not same
    if color_1.day == color_2.day:
        return abs(color_1.slot - color_2.slot)
    else:
        return "NA"

def total_dis(color_1, color_2):
    d2 = dis_2(color_1, color_2)
    d1 = dis_1(color_1, color_2)

    return GAMMA*d2 + d1

def binary_search(alist, item):
    first = 0
    last = len(alist) - 1
    found = False
    
    while first <= last and not found:
        midpoint = (first + last) // 2
        if alist[midpoint][1] == item:
            found = True
            last = midpoint-1
        else:
            if item < alist[midpoint][1]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    return last+1

def get_lecture_hall(max_students, sorted_list):
    lecturehall_list=list(sorted_list)
    selected_lecture_halls = {}    
    while(max_students > 0):
        i = binary_search(lecturehall_list, max_students)
        if(i < 0):
            i = 0
        elif(i >= len(lecturehall_list)):
            i = len(lecturehall_list) - 1
        if(i<0):
            selected_lecture_halls={}
            break
        max_students -= lecturehall_list[i][1]
        lecturehall_object =lecturehall_list[i][0][0]
        lecture_hall = lecturehall_object.number
        oe = lecturehall_list[i][0][1]
        del lecturehall_list[i]
        selected_lecture_halls[lecturehall_object] = oe
        for j in range(len(lecturehall_list)):
            if(lecturehall_list[j][0][0].number==lecture_hall):
                del lecturehall_list[j]
                break
    return selected_lecture_halls
    

def select_lecture_hall(no_of_students,lecture_halls):  
    lecture_hall_dict = {}
    for i in lecture_halls:
        lecture_hall_dict[i]=i.availability()['seats']
    
    lecture_hall_tuple_list = {}

    for num, value in lecture_hall_dict.iteritems():
        lecture_hall_tuple_list[(num,'o')] = value[0]
        lecture_hall_tuple_list[(num,'e')] = value[1]
    sorted_list = sorted(lecture_hall_tuple_list.items(), key=operator.itemgetter(1))
    return get_lecture_hall(no_of_students, sorted_list)

def update_lecture_hall(hall_list, course, color):
    course.lecture_hall = hall_list
    color = course.assign_color(color)
    for hall, position in hall_list.iteritems():
        if position=='o':
            hall.odd = 1
        elif position=='e':
            hall.even = 1


def get_first_node_color(course, color_matrix):

    for j in range(MAX_SCHEDULE_DAYS):
        for k in range(TIME_SLOTS):
            hall_list = select_lecture_hall(course.no_of_students, color_matrix[j][k].lecture_hall_list())
            #print course.course_code, hall_list
            if hall_list:
                update_lecture_hall(hall_list, course, color_matrix[j][k])
                return color_matrix[j][k], hall_list

    return None

def get_smallest_available_color(course, color_matrix):
    adj_list = course.adjacency_list
    for j in range(MAX_SCHEDULE_DAYS):
        for k in range(TIME_SLOTS):
            valid = True
            
            for r in range(len(adj_list)):
                color = adj_list[r].color
                if color:
                    if color.day!= j and color.slot!=k:
                        if dis_2(color, color_matrix[j][k]) == 0:
                            if dis_1(color, color_matrix[j][k]) <= 1:
                                
                                valid = False
                                break

                        #TODO
                        assigned_lh = select_lecture_hall(course.no_of_students, color.lecture_halls)
                        #if color.capacity_available <= course.concurrency_level:
                        if not assigned_lh:
                            valid = False
                            break
                           
                        if check_three_exams_constraint(course, color_matrix[j][k], j, color_matrix) == False:
                            valid = False
                            break
                    else:
                        valid = False
                        break #exit loop
                else:
                    continue
                    #exit the current iteration of loop?
                #TODO
            if valid == True:
                try:
                    return color_matrix[j][k], assigned_lh
                except:
                    return None
                
    return None    

def check_three_exams_constraint(course, color_jk, j, color_matrix):
    students = course.student_list

    for r in range(len(students)):
        counter = 0
        for q in range(TIME_SLOTS):
            course_list = color_matrix[j][q].courses
            for u in range(len(course_list)):
                students_u = course_list[u].student_list
                if students[r] in students_u:
                    counter+=1
                    if counter == 2:
                        return False

    return True

if __name__ == "__main__":
    graph, course_list = build_weight_matrix()
    calculate_degree(graph, course_list)    

    sorted_courses = sorted(course_list, key = lambda course: (course.degree, course.max_adjacency), reverse = True)
    deg = []

    num_colored_courses = 0

    color_matrix = initiailize_colors(MAX_SCHEDULE_DAYS, TIME_SLOTS)
    """for i in range(MAX_SCHEDULE_DAYS):
        for j in range(TIME_SLOTS):
            print color_matrix[i][j].day, color_matrix[i][j].slot
    """

    s = initialize_students()

    lh_list = initialize_lecture_halls(color_matrix)
    
    for course in sorted_courses:
        print course.course_code
        if num_colored_courses == len(course_list):
            break #exit loop and finish
    
        if not course.color:
    
            if sorted_courses.index(course)==0:
                
                r_ab, hall_list = get_first_node_color(course, color_matrix)
    
                if r_ab == None:
                    print "No schedule is possible"
                    break 
        
            else:
                res = get_smallest_available_color(course, color_matrix)
                if res:
                    r_ab, hall_list = res
                else:
                    r_ab = None

            if r_ab:
                course.assign_color(r_ab)
                num_colored_courses+=1 
                if hall_list:
                    update_lecture_hall(hall_list, course, r_ab)
    
        m = course.ordered_adjacency_list()
        for adj_course in m:
            if not adj_course.color:
                res = get_smallest_available_color(adj_course, color_matrix)
                if res:
                    r_cd, hall_list = res
                else:
                    r_cd = None

                if r_cd:
                    adj_course.assign_color(r_cd)
                    num_colored_courses+=1
                    if hall_list:
                        update_lecture_hall(hall_list, course, r_cd)
    
    for i in range(MAX_SCHEDULE_DAYS):
        for j in range(TIME_SLOTS):
            l = []
            for k in color_matrix[i][j].courses:
                l.append(key.course_code)
            print i, j, " : ", l
import numpy as np
import json

#Can add a heuristic when assiging a node color. 
#We can assume minimum number of lecture halls. eg 100 students per lecture hall
#If capacity of color is less than that, ignore the color and move to next. 
#After that, we use our algorithm to assign find optimum number of lecture halls 
#ensuring minimum wastage of space.

#For every course, when we return a color, we need to return a LectureHall object as well
#so that we can record which lecture hall and which seats do the particular course has to occupy

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
        self.concurrency_level = 0 #No of rooms required
        self.adjacency_list = []
        self.color = None #Assign a color object here
        self.lecture_hall = None
        self.old_day = old_day
        self.old_slot = old_slot

    def ordered_adjacency_list(self):
        #What is order?
        return self.adjacency_list

    def assign_color(self, color):
        self.color = color
        color.courses.append(self)
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
            capacity += i.availability['total']
        return capacity

    def get_lecture_halls(self, lecture_halls, course):
        available_halls = []
        for i in self.lecture_halls:
            if i.availability['total']>0:
                available_halls.append(i)
        return available_halls

class LectureHall:
    def __init__(self, number, odd_capacity, even_capacity, color):
        self.number = 0
        self.color = color
        
        color.lecture_halls.append(self)

        #O implies that odd/even seats are not occupied. 
        #1 implies that odd/even seats are occupied
        self.odd = 0
        self.even = 0

        self.odd_capacity = odd_capacity
        self.even_capacity = even_capacity

    def availability(self):
        if self.odd and self.even:
            return {
                "O" : self.odd_capacity, 
                "E" : self.even_capacity, 
                "total": max(self.odd_capacity, self.even_capacity)
            }

        elif self.odd:
            return {"O" : self.odd_capacity, "total" : self.odd_capacity}

        else self.even:
            return {"E" : self.even_capacity, "total" : self.even_capacity}

        else:
            return {"total" : 0}


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

    for day in range(1, MAX_SCHEDULE_DAYS+1):
        for slot in range(1, TIME_SLOTS+1):
            new_color = Color(day, slot)
            color_matrix[day-1][slot-1] = new_color

    return color_matrix

def build_weight_matrix():
    with open('data_course.json') as data_file:
        course_data = json.load(data_file)

    with open('mid_sem_exam_schedule.json') as data_file:
        exam_data = json.load(data_file)

    courses=[]
    counter = 1
    for course_code, students in course_data.iteritems():
        try:
            old_day, old_slot = exam_data[course_code][0], exam_data[course_code][1]
            courses.append(Course(counter, course_code, students, old_day, old_slot))
        except:
            print "No exam schedule for ", course_code
            courses.append(Course(counter, course_code, students, "NA", "NA"))
        counter+=1

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

def initialize_lecture_halls(color_list):
    with open('lecture_halls.json') as data_file:
        data = json.load(data_file)

    for color in color_list:
        for number, capacity in data.iteritems():
            lec_hall = LectureHall(number, capacity, color)
            color.lecture_halls.append(lec_hall)

def initialize_students():
    with open('data_student.json') as data_file:
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

def binarySearch(alist, item):
    first = 0
    last = len(alist)-1
    found = False
    
    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return last

def select_lecture_halls(max_students,lecturehall_list):
    lecturehall_list=sorted(lecturehall_list, key=MyFn)
    while(max_students>0):
        i=binarySearch(lecturehall_list.List, max_students)
        max_students=max_students-lecturehall_list.List[i]
        lecturehall_list.List.delete(i)
    #return [L1, 'O']


def get_first_node_color(course, color_matrix):

    for j in range(1, MAX_SCHEDULE_DAYS):
        for k in range(1, TIME_SLOTS):
            a = select_lecture_halls(course.no_of_students, color_matrix[j][k].get_lecture_halls())
            if a:
                return a

    return None

def get_smallest_available_color(course):
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
                                break #Need to exit loop. Is this the right way?

                        if color.capacity_available <= course.concurrency_level:
                            valid = False
                            break #Exit loop
                           
                        if check_three_exams_constraint(course, color_matrix[j][k], j) == False:
                            valid = False
                            break #Exit Loop
                    else:
                        valid = False
                        break #exit loop
                else:
                    break
                    #exit the current iteration of loop?
            if valid == True:
                return color[j][k]
                
    return None    

def check_three_exams_contraint(course, color_jk, j):
    students = course.student_list

    for r in range(len(students)):
        counter = 0
        for q in range(TIME_SLOTS):
            course_list = color_jk.courses
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
    
    num_colored_courses = 0
    
    for course in sorted_courses:
        if num_colored_courses == len(course_list):
            break #exit loop and finish
    
        if not course.color:
    
            if sorted_courses.index(course)==1:
                r_ab = get_first_node_color(course)
    
                if r_ab == None:
                    print "No schedule is possible"
                    break 
    
            else:
                r_ab = get_smallest_available_color(course)
            
            if r_ab:
                course.assign_color(r_ab)
                num_colored_courses+=1 
                """Update concurrency level of the color - subtract concurrency of course from that of slot
                Update according to class deginition                
                """
    
        m = course.ordered_adjacency_list(course)
    
        for adj_course in m:
            if not adj_course.color:
                r_cd = get_smallest_available_color(adj_course)
    
                if r_cd:
                    adj_course.assign_color(r_cd)
                    num_colored_courses+=1
                    """Update concurrency level of the color - subtract concurrency of course from that of slot
                    Update according to class deginition                
                    """
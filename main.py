import numpy as np
import json

#Can add a heuristic when assiging a node color. 
#We can assume minimum number of lecture halls. eg 100 students per lecture hall
#If capacity of color is less than that, ignore the color and move to next. 
#After that, we use our algorithm to assign find optimum number of lecture halls 
#ensuring minimum wastage of space.

MAX_SCHEDULE_DAYS = 8
TIME_SLOTS = 5
GAMMA = 0.5 #Change to proivde a different coloring scheme

class Course:
    def __init__(self, id, code, student_list):
        self.id = id
        self.course_code = code
        self.student_list = student_list
        self.no_of_students = len(student_list)
        self.degree = 0
        self.max_adjacency = 0
        self.concurrency_level = 0 #No of rooms required
        self.adjacency_list = []
        self.color = None #Assign a color object here

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
        self.day = []
        self.slot = []
        self.courses = []

    def capacity_available(self):
        capacity = 0
        for i in self.lecture_halls:
            if i.availability:
                capacity += (i.total_capacity)/2
        return capacity

    def get_lecture_halls(self, lecture_halls, course):
        available_halls = []
        for i in self.lecture_halls:
            if i.availability:
                available_halls.append(i)
        return available_halls


class LectureHall:
    def __init__(self, number, total_capacity):
        self.number = 0
        
        #O implies that odd/even seats are not occupied. 
        #1 implies that odd/even seats are occupied
        self.odd = 0
        self.even = 0

        self.total_capacity = total_capacity

    def availability(self):
        if self.odd and self.even:
            return "both"
        elif self.odd:
            return "odd"
        elif self.even:
            return "even"
        else:
            return None

class Student:
    def __init__(self, name, roll_no, courses):
        self.name = name
        self.roll_no = roll_no
        self.courses_enrolled = courses

    def fairness_quotient(self):
        pass

def calculate_common_students(c1, c2):
    return len(list(set(c1.student_list).intersection(c2.student_list)))

def calculate_degree(matrix, courses):
    for i in range(len(courses)):
        courses[i].degree = np.sum(matrix[i]!= 0)

def build_weight_matrix():
    with open('data_course.json') as data_file:
        data = json.load(data_file)

    courses=[]
    for course_code, students in data.iteritems():
        courses.append(Course(1, course_code, students))
    print len(courses)

    #for i in range(len(data)):
    #    courses.append(Course(id, data[i]["course_code"], data[i]["students"]))

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

def build_color_matrix(MAX_SCHEDULE_DAYS, TIME_SLOTS):
    matrix = np.zeros([MAX_SCHEDULE_DAYS, TIME_SLOTS])
    return matrix

def get_first_node_color(course):
    pass

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


if __name__ == "__main__":
    graph, course_list = build_weight_matrix()
    calculate_degree(graph, course_list)    

    sorted_courses = sorted(course_list, key = lambda course: (course.degree, course.max_adjacency), reverse = True)
    
    for i in sorted_courses:
        print i.course_code, i.degree, i.no_of_students

    num_colored_courses = 0
    
    for course in sorted_courses:
        if num_colored_courses == len(course_list):
            break #exit loop and finish
    
        if not course.color:
    
            if sorted_courses.index(course)==1:
                r_ab = get_first_node_color(course)
    
                if r_ab == None:
                    print "No schedyle is possible"
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
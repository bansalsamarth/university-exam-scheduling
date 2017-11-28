# university-exam-scheduling

## Course Project : Algorithms(MTH524)

### Exam Scheduling using Graph Coloring

We are scheduling exams in a university using Graph Coloring. The algorithm can be used for any university, but for testing purposes, we have tuned the program for IIT Kanpur, with data of even semester for academic year 2014-15. 

#### Input
(a) Course Data : Course Code, Students Enrolled

(b) Lecture Hall Data : Seats available in odd and even rows respectively, for exam purposes.

(c) Current Schedule : Exam schedule as alloted by university, for comparison purposes. 

#### Output
(a) Day and Slot alloted for all courses

(b) Lecture Hall and seating arrangement(odd or even) for all courses.

(c) Allotment done taking care of no clash for any students, and constraints to make the exam schedule convenient for most students. 

#### Instructions
Install NumPy

pip install numpy

The data folder includes scripts for scraping the data and stroing the json. No need to run them, as the data for IITK has been scraped and saved in the folder.


To run : python main.py
"""
Scraping examination schedule data of 
IIT Kanpur, even semester 2014-15. 
Exams are spread over 8 days, with 5 slots. 
Apart from 5 courses, exams are scheduled in Slot 1, 3, 5
"""

import requests, json
from bs4 import BeautifulSoup

#Mid Semster examination data
a = requests.get('http://172.26.142.68/examscheduler/content.php')
soup = BeautifulSoup(a.content)

table = soup.find('table')
rows = table.find_all('tr')

mid_data = {}

for i in range(2, 10):
	row = rows[i]
	cols = row.find_all('td')
	
	for j in range(1, 6):
		courses = str(cols[j])
		courses = courses.replace('<td>', '').replace('</td>', '').replace(' ','').split(',')

		day = i - 1
		slot = j
		for k in courses:
			mid_data[k] = [day, slot]

mid_data = json.dumps(mid_data)

out = open('mid_sem_exam_schedule.json', 'w')
out.write(mid_data)


#End Semster examination data
a = requests.get('http://172.26.142.68/examscheduler2/content.php')
soup = BeautifulSoup(a.content)

table = soup.find('table')
rows = table.find_all('tr')

end_data = {}

for i in range(2, 13):
	row = rows[i]
	cols = row.find_all('td')
	
	for j in range(1, 4):
		courses = str(cols[j])
		courses = courses.replace('<td>', '').replace('</td>', '').replace(' ','').split(',')
		print len(courses)

		day = i - 1
		slot = j
		for k in courses:
			end_data[k] = [day, slot]
			#print k, day, slot

end_data = json.dumps(end_data)

out = open('end_sem_exam_schedule.json', 'w')
out.write(end_data)
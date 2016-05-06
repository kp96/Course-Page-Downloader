from bs4 import BeautifulSoup
import shutil
import requests
from CaptchaParser import CaptchaParser
from PIL import Image
from Course import Course
import json
import os
import urllib as url
import re
import sys, traceback
from clint.textui import progress
from requests.adapters import HTTPAdapter
captcha_url = 'https://academics.vit.ac.in/student/captcha.asp'
submit_url = 'https://academics.vit.ac.in/student/stud_login_submit.asp'
timetable_url = 'https://academics.vit.ac.in/student/timetable_ws.asp'
home_url = 'https://academics.vit.ac.in/student/stud_home.asp'
course_page_url = 'https://academics.vit.ac.in/student/coursepage_view.asp'
course_contents_url  = 'https://academics.vit.ac.in/student/coursepage_view3.asp'
marks_url = 'https://academics.vit.ac.in/student/marks.asp?sem=WS'
head_url = 'https://academics.vit.ac.in/student'
pattern = r'(FALL|WIN|SUM){1}SEM[0-9]{4}-[0-9]{2}_CP[0-9]{4}.*_[A-Z]{2,4}[0-9]{2}_'
req = requests.Session()
req.mount('http://academics.vit.ac.in', HTTPAdapter(max_retries=10))
requests.packages.urllib3.disable_warnings()
class Api:
	@staticmethod
	def login(regno, password):
		res = []
		print "Parsing captcha for you."
		try:	
			res = req.get(captcha_url, stream = True, timeout = 40, verify = False)
			cookies = res.cookies
			with open('captcha.bmp', 'wb') as out_file:
				shutil.copyfileobj(res.raw, out_file)
			img = Image.open("captcha.bmp")
			parser = CaptchaParser()
			captcha = parser.getCaptcha(img)
			data = {}
			data['message'] = "";
			data['regno'] = regno
			data['passwd'] = password
			data['vrfcd'] = captcha
			print "Logging In..."
			login_res = req.post(submit_url, data = data, cookies = cookies, timeout = 40)
			soup = BeautifulSoup(login_res.text, "html.parser")
			try:
				x = ((soup.findAll('table')[1]).td.font.string.split(" - "))[1]
				if x == regno:
					success = True
					req.get(home_url, cookies = cookies, timeout = 40) # just to make sure that session id is validated
					res = [success, cookies]
					return res
				else:
					success = False
					res = [success, None]
					return res
			except:
					success = False
					res = [success, None]
					return res
		except:
			print "Connection is too Slow.. try again!"
	@staticmethod
	def get_courses(cookies):
		try:
			print "Getting your list of courses..."
			timetable_res = req.get(timetable_url, cookies = cookies, timeout = 40)
			soup = BeautifulSoup(timetable_res.text, "html.parser")
			ttsoup = soup.findAll('table')[1]
			courses = []
			for course in ttsoup.findAll('tr'):
				if course['bgcolor'] == "#EDEADE":
					details = course.findAll('td')
					course_code = ""
					course_slot = ""
					course_fac = ""
					try:
						course_code = details[3].string
						course_fac = details[11].string.split(" - ")[0]
						course_slot = details[9].string
					except IndexError:
						course_code = details[1].string
						course_fac = details[9].string.split(" - ")[0]
						course_slot = details[7].string
					cur_course = Course(course_code, course_slot, course_fac, "xyz")
					courses.append(cur_course)
			print "Going to Course Page..."
			print len(courses)
			for course in courses:
				params = {}
				params['sem'] = 'WS'
				params['slt'] = course.course_slot
				params['crs'] = course.course_code
				params['fac'] = ''
				res = req.get(course_page_url, cookies = cookies, params = params, timeout = 40)
				print "Getting details of course and faculties " + course.course_code
				soup = BeautifulSoup(res.text, "html.parser")
				try:
					faculty_soup = soup.table.findAll('table')[1]
					for factag in faculty_soup.findAll('tr'):
						if factag['bgcolor'] == "#E1ECF2":
							fac_name = factag.findAll('td')[3].string.split(" - ")[1]
							if fac_name == course.course_faculty:
								course.course_secret = factag.form.td.findAll('input')[1]['value']
								break

				except IndexError:
					print "Course page not available for course " + course.course_code
			return courses
		except Exception,e: print str(e)
	@staticmethod
	def download(course, cookies, folder_path):
		try:
			print "Downloading " + course.course_faculty + " Materials "
			directory = course.course_code + " - " + course.course_faculty
			location = os.path.join(folder_path, directory)
			if not os.path.exists(location):
				os.makedirs(location)
			data = {}
			data['sem'] = "WS"
			data['crsplancode'] = course.course_secret
			data['crpnvwcmd'] = "View"
			res = req.post(course_contents_url, data = data, timeout = 40)
			soup = BeautifulSoup(res.text, "html.parser")
			for link in soup.findAll('a'):
				link_name = link.get('href')
				link_name = head_url + '/' +  link_name
				res = req.head(link_name, cookies = cookies, timeout = 40)
				link_file_name = ''
				try:
					link_file_name =  res.headers.get('Content-Disposition').split(';')[1].split('=')[1]
				except:
					res.headers.get('Content-Disposition')
					link_file_name = 'unrecognized_format'
				if re.match(pattern, link_file_name):
					file_name = re.split(pattern, link_file_name)[-1]
					if os.path.isfile(os.path.join(location,file_name)):
						print "Already Downloaded " + file_name
					else:
						print "Downloading " + file_name
						res = req.get(link_name, cookies = cookies, stream = True, timeout = 40)
						with open(os.path.join(location,file_name), 'wb') as f:
							total_length = int(res.headers.get('content-length'))
							for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
								if chunk:
									f.write(chunk)
									f.flush()
		except Exception, a:
			print "Connection is too Slow! Try again"
	
							
				



		



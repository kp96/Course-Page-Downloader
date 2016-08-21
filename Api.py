from bs4 import BeautifulSoup
import shutil
import time
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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from requests.adapters import HTTPAdapter
from clint.textui import progress
captcha_url = 'https://vtop.vit.ac.in/student/captcha.asp'
submit_url = 'https://vtop.vit.ac.in/student/stud_login_submit.asp'
timetable_url = 'https://vtop.vit.ac.in/student/course_regular.asp?sem=FS'
home_url = 'https://vtop.vit.ac.in/student/stud_home.asp'
course_page_url = 'https://vtop.vit.ac.in/student/coursepage_plan_view.asp?sem=FS'
course_contents_url  = 'https://vtop.vit.ac.in/student/coursepage_view3.asp'
marks_url = 'https://vtop.vit.ac.in/student/marks.asp?sem=WS'
head_url = 'https://vtop.vit.ac.in/student'
pattern = r'(FALL|WIN|SUM){1}SEM[0-9]{4}-[0-9]{2}_CP[0-9]{4}.*_[A-Z]{2,4}[0-9]{2}_'
req = requests.Session()
req.mount('http://vtop.vit.ac.in', HTTPAdapter(max_retries=10))
requests.packages.urllib3.disable_warnings()
executable_path = "C:/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path
chrome_options = Options()
chrome_options.add_extension('autocaptcha-for-chrome.crx')
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
class Api:
	def __init__(self, regno, pwd, gui = None, folder = None):
		self.regno = regno
		self.pwd = pwd
		self.gui = gui
		self.folder = folder

	def set_folder(self, folder):
		self.folder = folder
	def login(self):
		print "Loggin in"
		driver.get('https://vtop.vit.ac.in/student/stud_login.asp')
		time.sleep(0.5) # Let the user actually see something!
		regno_el = driver.find_element_by_name('regno')
		pwd_el = driver.find_element_by_name('passwd')
		regno_el.send_keys(self.regno)
		pwd_el.send_keys(self.pwd)
		pwd_el.send_keys(Keys.RETURN)
		time.sleep(1) # Let the user actually see something!
		soup = BeautifulSoup(driver.page_source, "html.parser")
		try:
			x = ((soup.findAll('table')[1]).td.font.string.split(" - "))[1]
			return x == self.regno
		except:
				return False
	def get_courses(self):
		try:
			print "Getting your list of courses..."
			driver.get(timetable_url)
			soup = BeautifulSoup(driver.page_source, "html.parser")
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
						print course_code + " " + course_fac + " " + course_slot
					except IndexError:
						course_code = details[1].string
						course_fac = details[9].string.split(" - ")[0]
						course_slot = details[7].string
					cur_course = Course(course_code, course_slot, course_fac, details[4].string)
					courses.append(cur_course)
			return courses
		except Exception,e: print str(e)
	def download(self, courses, folder_path):
		print "Starting selenium instance.."
		self.folder = folder_path
		try:
			for course in courses:
				print "Downloading " + course.course_faculty + " Materials "
				directory = course.course_code + " - " + course.course_faculty
				location = os.path.join(self.folder, directory)
				if not os.path.exists(location):
					os.makedirs(location)
				driver.get('https://vtop.vit.ac.in/student/coursepage_plan_view.asp?sem=FS')
				time.sleep(1)
				try:
					select_course = Select(driver.find_element_by_name('course'))
					select_course.select_by_value(course.course_code)
					time.sleep(0.5)
					select_slot = Select(driver.find_element_by_name('slot'))
					select_slot.select_by_value(course.course_slot)
					time.sleep(0.5)
					select_fac = Select(driver.find_element_by_name('faculty'))
					fac_options = [x for x in driver.find_element_by_name('faculty').find_elements_by_tag_name("option")]
					fac_val = ""
					for a_fac in fac_options:
						if course.course_faculty in a_fac.text:
							fac_val = a_fac.get_attribute('value')
							break
					select_fac.select_by_value(fac_val)
					driver.find_element_by_name('crpnvwcmd').click()
					time.sleep(0.5)
					cookies = driver.get_cookies()
					for cookie in cookies:
						req.cookies.set(cookie['name'], cookie['value'])
					links = driver.find_elements_by_tag_name('a')
					for i in range(len(links)):
						link_name = links[i].get_attribute('href')
						#link_name = head_url + '/' +  link_name
						res = req.head(link_name, timeout = 40)
						link_file_name = ''
						try:
							link_file_name =  res.headers.get('Content-Disposition').split(';')[1].split('=')[1]
						except:
							link_file_name = 'unrecognized_format'
						file_name = re.split(pattern, link_file_name)[-1]
						if os.path.isfile(os.path.join(location,file_name)):
							print "Already Downloaded " + file_name
						else:
							print "Downloading " + file_name
							res = req.get(link_name, stream = True, timeout = 40)
							with open(os.path.join(location,file_name), 'wb') as f:
								total_length = int(res.headers.get('content-length'))
								for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
									if chunk:
										f.write(chunk)
										f.flush()
				except Exception, a: print "Cannot download contents for " + course.course_faculty + " Proceeding to next."
		except Exception, a:
			print "Some error try again."
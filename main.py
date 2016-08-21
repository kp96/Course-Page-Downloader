from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import base
from Course import Course 
from User import User
from Api import Api
import tkFileDialog
import getpass
from Tkinter import *
from tkFileDialog import *
engine = create_engine("sqlite:///course.db")
base.Base.metadata.create_all(engine, checkfirst = True)
Session = sessionmaker(bind = engine)
db = Session()
userdata = db.query(User)
user = User()
first = False
loggedin = False
if userdata.count() == 0:
	print "Welcome to Auto Course Downloader! To get started fill the details below"
	user_regno = raw_input("Enter regno: ")
	user_password = getpass.getpass("Enter password: ")
	user.user_regno = user_regno
	user.user_password = user_password
	first = True
else:
	for firstu in userdata:
		user.user_regno = firstu.user_regno
		user.user_password = firstu.user_password
		user.user_folder = firstu.user_folder
api = Api(user.user_regno, user.user_password)
try:
	login = api.login()
	if login:
		loggedin = True
		if first:
			courses = api.get_courses()
			root = Tk()
			root.withdraw()
			folder_path = askdirectory()
			print folder_path
			user.user_folder = folder_path
			db.add(user)
			db.add_all(courses)
			db.commit()
		else:
			courses = db.query(Course)
			folder_path = user.user_folder
		api.download(courses, folder_path)
		print "All done Successfully"

	else:
		print "Invalid Credentials Quitting the program"
except Exception,e: print str(e)

raw_input("press any key to quit")

	


			
		
 

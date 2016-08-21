from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import base
from Course import Course 
from User import User
from Api import Api
from tkFileDialog import *
import getpass
from Tkinter import *
from GUI import CpdlGui
engine = create_engine("sqlite:///course.db")
base.Base.metadata.create_all(engine, checkfirst = True)
Session = sessionmaker(bind = engine)
db = Session()
userdata = db.query(User)
user = User()
first = False
loggedin = False
import ttk
root = Tk()
gui = CpdlGui(root)
if userdata.count() != 0:
	for a_user in userdata:
		gui.set_regno(a_user.user_regno)
		gui.set_pwd(a_user.user_password)
		loggedin = True
		gui.set_folder(a_user.user_folder)
root.mainloop()

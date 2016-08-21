from Tkinter import *
import ttk
from tkFileDialog import *
class CpdlGui:
	def __init__ (self, root):
		self.root = root
		root.title ("Course Page Downlaoder")
		mainframe = ttk.Frame(root, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		self.mainframe = mainframe
		ttk.Label(mainframe, text="Registration Number").grid(row=0, column=0)
		self.regno = StringVar()
		self.pwd = StringVar()
		self.cache = IntVar()
		self.cache.set(1)
		self.progress = IntVar()
		self.progress.set(0)
		self.hint = StringVar()
		print "mama here"
		self.hint.set("Hit Download or Return to Proceed")
		self.regno_entry = ttk.Entry(self.mainframe, width=60, textvariable=self.regno)
		self.regno_entry.grid(column=0, row=1, sticky=(E))
		self.pwd_label = ttk.Label(self.mainframe, text="Password").grid(row=2, column=0)
		self.pwd_entry = ttk.Entry(self.mainframe, width=60, show='*', textvariable=self.pwd)
		self.pwd_entry.grid(column=0, row=3, sticky=(E))
		self.cb = ttk.Checkbutton(self.mainframe, text="Remember Me", variable = self.cache)
		self.cb.grid(column=0, row=4)
		self.dlbutton = ttk.Button(self.mainframe, text="Download", command= lambda: self.calculate())
		self.dlbutton.grid(column = 0, row=5)
		for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
		self.hint_label = ttk.Label(self.mainframe, text="Press Download to Begin", justify='center')
		self.hint_label.grid(row=6)
		self.prgbar = ttk.Progressbar(self.mainframe, orient='horizontal', mode='determinate', variable=self.progress).grid(column=0, row=7)
		self.regno_entry.focus()

	def update_progess(self, val):
		self.progress.set(val)

	def set_hint (self, val):
		self.hint_label.configure(text = val)
	def get_regno (self):
		return self.regno.get()

	def set_regno(self, val):
		self.regno.set(val)

	def get_pwd (self):
		return self.pwd.get()

	def set_pwd (self, val):
		self.pwd.set(val)

	def set_callback(self, callback):
		self.dlbutton.configure(command = callback)

	def set_folder(self, folder):
		self.folder = folder

	def get_folder():
		return self.folder

	def calculate(self):
    try:
        e_regno = self.get_regno()
        e_pwd = self.get_pwd()
        if e_regno == "" or e_pwd == "":
        	self.set_hint("Enter regno and password")
        else:
        	if loggedin is False:
        		api = Api(e_regno, e_pwd, self)
        	else:
        		api = Api(e_regno, e_pwd, self, self.folder)
        	user.user_regno = e_regno
        	user.user_password = e_pwd
        	login = api.login()
        	if login:
				if userdata.count() == 0:
					courses = api.get_courses()
					root = Tk()
					root.withdraw()
					folder_path = askdirectory()
					user.user_folder = folder_path
					api.set_folder(folder_path)
					db.add(user)
					db.add_all(courses)
					db.commit()
					api.download(courses)
				else:
					courses = db.query(Course)
					api.download(courses)
				self.set_hint("All files are downloaded successfully")
    except ValueError:
        pass
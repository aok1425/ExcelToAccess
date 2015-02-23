# my attempt to have user locate Access file on program
# now i think it's better to look in default loc, and if it's not there, ask user to locate it.
def access_file_location_check():
	"""Bc path is too long, I have '...'. If path hasn't changed, replace it to the full version."""
	if access_file.get == r'...\Quarterly BPHC Reporting\Access template 2014\e2Boston_RsrPlus-empty.mdb':
		return r'\\dotwell\dfs\Storage\Departments\DotWell\CDPP\Case Management\Quarterly BPHC Reporting\Access template 2014\e2Boston_RsrPlus-empty.mdb'

access_file = StringVar()
access_file.set(r'\\...\Quarterly BPHC Reporting\Access template 2014\e2Boston_RsrPlus-empty.mdb')
Label(mainframe, text="Location of empty Access template (from BPHC):").grid(column=1, row=1, sticky=(W,E))
Label(mainframe, textvariable=access_file_location_check()).grid(column=2, row=1, sticky=W)
Button(mainframe, text='Choose different location', command=set_access_file_location).grid(column=3, row=1, sticky=W)

# attempts at creating whole Frame()s or Toplevel()s to display errors
# now I think I'll just say 'see file'
def make_access_file(*args):
	error_window = Toplevel(root)
	error_window.geometry('300x200-5+40')
	error_window.grid(column=0, row=0, sticky=(N,W,E,S))
	error_window.columnconfigure(0, weight=1)
	error_window.rowconfigure(0, weight=1)	
	Message(error_window, text='something here').pack()
	# t = Text(error_window)
	# t.insert('1.0', 'here is my text to insert')
	# error_window.destroy()

# def make_access_file(*args):
# 	top = Toplevel()
# 	top.title("About this application...")

# 	msg = Message(top, text='about_message')
# 	msg.pack()

# 	button = Button(top, text="Dismiss", command=top.destroy)
# 	button.pack()	

# replaced this w True in df.duplicated(column)
def check_SSN_error_in_log_file():
	"""Super-hacky. Checks if 'SSN' is in one of the elements in log_file. If so, return True. Then, there's an SSN missing. If some of the SSN rows are missing for a patient, will be duplicate Access error."""
	error = 0

	for entry in log_file:
		if "Changed it to '9999' for Access" in entry:
			error += 1

	if error > 0:
		return True

# only MCMWithTransOnlyUnit matters, so deleting this
def check_MCMOnlyUnit(df, health_center):
	indexes = df.MCMOnlyUnit[df.MCMOnlyUnit != 1].index
	column = 'MCMOnlyUnit'

	if len(indexes) == 0:
		text = 'Checking for {} errors: No errors.'.format(column)
		append_text(text)
	else:
		for row_num in indexes:
			text = "{} for {} is not 1. Changing it to 1.".format(column, df.MRN[row_num])
			df.loc[row_num, column] = 1	
			append_text(text)			

# replaced bc of logging module
def append_text(text):
	"""Only 'write' to log_file if it's not the same as the last element there."""
	if log_file == []:
		print text
		log_file.append(text)
	else:
		if text != log_file[-1]:
			print text
			log_file.append(text)				
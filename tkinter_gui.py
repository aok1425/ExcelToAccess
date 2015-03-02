# idk why i can't reset log in write_access_file(). even when i do global, sth's not working.
# must be my misunderstanding around scope

from Tkinter import *
from tkFileDialog import *
import tkMessageBox as messagebox
from validation_check import *
from os import remove as delete_file
from datetime import datetime
from shutil import copy as copy_file

def set_utl_location_cs(*args):
	dir_path = askopenfilename()
	utl_file_cs.set(dir_path)

def set_utl_location_dh(*args):
	dir_path = askopenfilename()
	utl_file_dh.set(dir_path)	

def set_access_file_location(*args):
	dir_path = askopenfilename()
	access_file.set(dir_path)	

def setup_access_file(*args):
	if utl_file_dh.get() and utl_file_cs.get():
		filename1 = './e2Boston_RsrPlus-empty.mdb'
		time = datetime.now().strftime("%Y%m%d_%H%M_%S")
		filename2 = "./utilization_for_E2Boston" + time + ".mdb"		
		copy_file(filename1, filename2)
		
		try:
			write_access_file(filename2)
		except:
			delete_file(filename2)
			open_error_log_window()
			raise

	else:
		messagebox.showinfo(message='Choose both CS utilization file and DH utilization file.')		

def write_access_file(filename):
	# Done so that I didn't have to copy the below lines if I wanted to catch exceptions
	cs = ValidationCheckerExcelToAccess('COD')
	cs.load(utl_file_cs.get())
	cs.save(filename)

	dh = ValidationCheckerExcelToAccess('DOR')
	dh.load(utl_file_dh.get())
	dh.save(filename)	

	messagebox.showinfo(message='All done with no errors.\nAccess file is in same folder as this program.')	

def open_error_log_window():
	# maybe make this have 2 cols, w : as separator?
	second_root = Toplevel(root)

	mainframe = Frame(second_root)
	mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)

	Label(mainframe, text="Please fix these errors:").grid(column=1, row=1)
	Label(mainframe, text="\n".join(log)).grid(column=1, row=2, sticky=W)
	Label(mainframe, text="Access file was not made.").grid(column=1, row=3)
	Button(mainframe, text='OK', command=second_root.destroy).grid(column=1, columnspan=4, row=4)

	for child in mainframe.winfo_children():
		child.grid_configure(padx=5, pady=5)

	# Text(mainframe)

root = Tk()
root.title("Alex's Excel to Access program")

mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

intro_text = """If BPHC changes it's requirements, 
and this program stops working,
please email aok1425@gmail.com."""

Label(mainframe, text=intro_text).grid(row=0, column=1, columnspan=4)
	
utl_file_cs = StringVar()
Label(mainframe, text="Choose CS utilization file:").grid(column=1, row=2, sticky=E)
Label(mainframe, textvariable=utl_file_cs).grid(column=2, row=2, sticky=W)
Button(mainframe, text='Browse', command=set_utl_location_cs).grid(column=3, row=2, sticky=W)

utl_file_dh = StringVar()
Label(mainframe, text="Choose DH utilization file:").grid(column=1, row=3, sticky=E)
Label(mainframe, textvariable=utl_file_dh).grid(column=2, row=3, sticky=W)
Button(mainframe, text='Browse', command=set_utl_location_dh).grid(column=3, row=3, sticky=W)

Button(mainframe, text='Make Access file', command=setup_access_file).grid(column=1, columnspan=4, row=4)
Label(mainframe, text="Access file will be stored in same folder as this program.\nLast updated February 2015").grid(column=1, columnspan=4, row=5)


for child in mainframe.winfo_children():
	child.grid_configure(padx=5, pady=5)

root.mainloop()
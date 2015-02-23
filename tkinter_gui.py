# to-do: if error msgs, open dialog box. also maybe save that txt to dir?

from Tkinter import *
from tkFileDialog import *
import tkMessageBox as messagebox
from validation_check import *

def set_utl_location_cs(*args):
	dir_path = askopenfilename()
	utl_file_cs.set(dir_path)

def set_utl_location_dh(*args):
	dir_path = askopenfilename()
	utl_file_dh.set(dir_path)	

def set_access_file_location(*args):
	dir_path = askopenfilename()
	access_file.set(dir_path)	

def make_access_file(*args):
	try:
		copy_file(filename1, filename2)
	except IOError: # Can alternatively write whole traceback to log using logger.exception()
		append_text("Program can't find the empty Access template. This file should be \\dotwell\dfs\Storage\Departments\DotWell\CDPP\Case Management\Quarterly BPHC Reporting\Access template 2014\e2Boston_RsrPlus-empty.mdb.")
		
	try:
		db = pypyodbc.win_connect_mdb(filename2)
		c = db.cursor()

		append_text('For Codman: \n')
		ValidationCheckerExcelToAccess().run(utl_file_cs.get())

		append_text('\nFor Dorchester House: \n')			
		ValidationCheckerExcelToAccess(utl_file_dh.get()).run()	

		db.close()
		append_text("\nDone!")

		messagebox.showinfo(message='All done with no errors.')
	except:
		messagebox.showinfo(message="Something was wrong. There was an error. Program didn't complete.\n\nSee log{}.txt".format(time))

root = Tk()
root.title("Alex's Excel to Access program (last updated 2/22/15)")

mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

bottomframe = Frame(root)
bottomframe.grid(column=0, row=1, sticky=S)
bottomframe.columnconfigure(0, weight=1)
bottomframe.rowconfigure(1, weight=1)

intro_text = """Choose the location of the empty Access file, if it's different from the default location.
Then, choose the locations of the CS and DH utilization files from Rima.
Lastly, click Make Access File and hopefully everything will work"""

Label(mainframe, text=intro_text).grid(row=0, column=1, columnspan=4)
	
utl_file_cs = StringVar()
Label(mainframe, text="Choose CS utilization file:").grid(column=1, row=2, sticky=E)
Label(mainframe, textvariable=utl_file_cs).grid(column=2, row=2, sticky=W)
Button(mainframe, text='Browse', command=set_utl_location_cs).grid(column=3, row=2, sticky=W)

utl_file_dh = StringVar()
Label(mainframe, text="Choose DH utilization file:").grid(column=1, row=3, sticky=E)
Label(mainframe, textvariable=utl_file_dh).grid(column=2, row=3, sticky=W)
Button(mainframe, text='Browse', command=set_utl_location_dh).grid(column=3, row=3, sticky=W)

Button(bottomframe, text='Make Access file', command=make_access_file).grid(column=0, row=0)
Label(bottomframe, text="File will be stored in same folder as this program.").grid(column=0, row=1)


for child in mainframe.winfo_children():
	child.grid_configure(padx=5, pady=5)

root.mainloop()
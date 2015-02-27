# have prog throw errors at the right time (like if DOR file is malformatted)
# clean up exceptions

# account for all possible user errors!
# if only CS or only DH, have dialog window open

# any way to put the traceback exceptions into the error msg
# and then make that text so Carole can email it to me?

# UX thinking: error msg for missing files shld not close prog, while from error in prog shld

from Tkinter import *
from tkFileDialog import *
import tkMessageBox as messagebox
from validation_check import *
from os import remove as delete_file

def set_utl_location_cs(*args):
	dir_path = askopenfilename()
	utl_file_cs.set(dir_path)

def set_utl_location_dh(*args):
	dir_path = askopenfilename()
	utl_file_dh.set(dir_path)	

def set_access_file_location(*args):
	dir_path = askopenfilename()
	access_file.set(dir_path)	

def make_test():
	c = 'something'
	Test('a').run()

def make_access_file(*args):
	copy_file(filename1, filename2)

	# append_text('For Codman: \n')
	# cs = ValidationCheckerExcelToAccess()
	# cs.load(utl_file_cs.get())
	# cs.save(filename2)

	# append_text('\nFor Dorchester House: \n')			
	# dh = ValidationCheckerExcelToAccess()
	# dh.load(utl_file_dh.get())
	# dh.save(filename2)	

	# append_text("\nDone!")

	# messagebox.showinfo(message='All done with no errors.')

	try:
		append_text('For Codman: \n')
		cs = ValidationCheckerExcelToAccess()
		cs.load(utl_file_cs.get())
		cs.save(filename2)

		# append_text('\nFor Dorchester House: \n')			
		# dh = ValidationCheckerExcelToAccess()
		# dh.load(utl_file_dh.get())
		# dh.save(filename2)	

		append_text("\nDone!")
		messagebox.showinfo(message='All done with no errors.')
	except:
		delete_file(filename2)
		open_error_log_window()
		# messagebox.showinfo(message='This is a test')
		# messagebox.showinfo(message="Something was wrong. There was an error. Program didn't complete.\n\nSee log{}.txt".format(time))

def open_error_log_window():
	# maybe make this have 2 cols, w : as separator?
	second_root = Toplevel(root)

	mainframe = Frame(second_root)
	mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)

	Label(mainframe, text="There were errors. Access file was not made. Please fix these errors.").grid(column=1, row=1)
	Label(mainframe, text="\n".join(log)).grid(column=1, row=3, sticky=W)
	Button(mainframe, text='OK', command=root.destroy).grid(column=1, columnspan=4, row=4)

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

Button(mainframe, text='Make Access file', command=make_access_file).grid(column=1, columnspan=4, row=4)
Label(mainframe, text="Access file will be stored in same folder as this program.").grid(column=1, columnspan=4, row=5)

Label(mainframe, text="Last updated February 2015").grid(row=6, column=1, columnspan=4)


for child in mainframe.winfo_children():
	child.grid_configure(padx=5, pady=5)

root.mainloop()
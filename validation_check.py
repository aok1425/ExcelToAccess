# filenames MUST start w COD or DOR, for MCMOnlyUnit()
# put template file in permanent location

# to do: if log/Access file already exist for that time, make another one w suffix '2'

import pandas as pd
import pypyodbc 
import os
import re
import logging
from datetime import datetime
from math import isnan
from shutil import copy as copy_file
from numpy import float64

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

filename1 = r"\\dotwell\dfs\Storage\Departments\DotWell\CDPP\Case Management\Quarterly BPHC Reporting\Access Template 2014\e2Boston_RsrPlus-empty.mdb"
# filename1 = '../e2Boston_RsrPlus-empty.mdb'
time = datetime.now().strftime("%Y%m%d_%H%M")
filename2 = "../utilization_for_E2Boston" + time + ".mdb"

def append_text(text):
	logger.info(text)			

handler = logging.FileHandler('../log' + time + '.txt')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)			

def transform_MRN(x):
	"""For .map(). Adds 0s when inputted an MRN as a float converted to a str.
	Assumes that all MRNs will start w 0s.
	A hack bc .read_excel() in Pandas 0.15 doesn't have dtype argument like .read_csv()."""
	num_zeros = 10 - len(x)
	if len(x) <= 10:
		return num_zeros * '0' + x[:8 - num_zeros]
	else:
		raise Exception('Something wrong w MRN')
	
def make_initials(row_num, df):
	pre_join = [df.FirstInitial[row_num], df.FirstInitial3[row_num], df.LastInitial[row_num], df.LastInitial3[row_num]]
	
	for i in range(len(pre_join)):
		if type(pre_join[i]) == float:
			if isnan(pre_join[i]):
				pre_join[i] = ' '		
			
	return ''.join(pre_join)	

def convert_nan_to_none(a_tuple):
	"""For ClientReportService"""
	temp_list = list(a_tuple)
	
	for i in range(len(temp_list)):
		if type(temp_list[i]) == float64 or type(temp_list[i]) == float:
			if isnan(temp_list[i]):
				temp_list[i] = None
	
	return tuple(temp_list)

def find_health_center(filename_path):
	"""From filename path, find whether health center is COD or DOR.
	If COD or DOR is in filename path multiple times, it will choose the first one :("""
	match = re.search('COD', filename_path)
	if match:
		return match.group()
	else:
		match = re.search('DOR', filename_path)
		if match:
			return match.group()

def check_blank_SSN(df):
	"""Input a DataFrame, and find the MRNs for pts w blank SSNs."""
	indexes_of_blank_SSNs = df.Last4SSN[df.Last4SSN.notnull() == False].index
	
	if len(indexes_of_blank_SSNs) == 0:
		text = 'Checking for SSN errors: No errors.'
		append_text(text)
	else:
		for row_num in indexes_of_blank_SSNs:
			initials = make_initials(row_num, df)
			df.loc[row_num, 'Last4SSN'] = '9999'
			text = "SSN for {}/{} is blank. Changed it to '9999' for Access. Please update SSN in CPS.".format(initials, df.MRN[row_num])
			append_text(text)

def check_MCMOnlyTransUnit(df, health_center):
	"""If DOR, it's fine. If COD, move columns. Will have to chg write() too."""
	if health_center == 'COD':
		df = df.rename(columns = {
			'MCMUnitTime': 'MCMwithTransUnitTime',
			'MCMOnlyUnit': 'MCMwithTransOnlyUnit'}, inplace=True)			

def write_to_ClientReportService(df, health_center):
	"""Input a DataFrame, and write to the empty Access template in the same folder."""
	if health_center == 'DOR':
		for i in df.index:
			entry = df.MRN[i], df.ServiceDate[i], df.ServiceTime[i], df.Employee[i], df.ServiceID[i], df.SubserviceID[i], df.GrantID[i], df.DrugAssistanceDateReimburse[i], df.DrugAssistanceUnit[i], df.FoodUnit[i], df.NutritionalAssessment[i], df.NutritionalCounselingTime[i], df.MedicalNutritionalTherapyUnit[i], df.MedicalNutritionalTherapyAssessment[i], df.MedicalNutritionalTherapyCounselingTime[i], df.RentalAssistanceUnit[i], df.UtilityAssistanceUnit[i], df.HousingAdvocacyUnit[i], df.HousingAdvocacyPlacementUnit[i], df.MCMwithTransUnitTime[i], df.MCMwithTransOnlyUnit[i]
			entry = convert_nan_to_none(entry)
			c.execute('''INSERT INTO ClientReportService(ClientReportID, ServiceDate, ServiceTime, Employee, ServiceID, SubserviceID, GrantID, DrugAssistanceDateReimbursed, DrugAssistanceUnit, FoodUnit, NutritionalAssessment, NutritionalCounselingTime, MedicalNutritionalTherapyUnit, MedicalNutritionalTherapyAssessment, MedicalNutritionalTherapyCounselingTime, RentalAssistanceUnit, UtilityAssistanceUnit, HousingAdvocacyUnit, HousingAdvocacyPlacementUnit, MCMwithTransUnitTime, MCMwithTransOnlyUnit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', entry)
	elif health_center == 'COD':
		for i in df.index:
			entry = df.MRN[i], df.ServiceDate[i], df.ServiceTime[i], df.Employee[i], df.ServiceID[i], df.SubserviceID[i], df.GrantID[i], df.DrugAssistanceDateReimburse[i], df.DrugAssistanceUnit[i], df.FoodUnit[i], df.NutritionalAssessment[i], df.NutritionalCounselingTime[i], df.MedicalNutritionalTherapyUnit[i], df.MedicalNutritionalTherapyAssessment[i], df.MedicalNutritionalTherapyCounselingTime[i], df.RentalAssistanceUnit[i], df.UtilityAssistanceUnit[i], df.HousingAdvocacyUnit[i], df.HousingAdvocacyPlacementUnit[i], df.MCMUnitTime[i], df.MCMOnlyUnit[i]
			entry = convert_nan_to_none(entry)
			c.execute('''INSERT INTO ClientReportService(ClientReportID, ServiceDate, ServiceTime, Employee, ServiceID, SubserviceID, GrantID, DrugAssistanceDateReimbursed, DrugAssistanceUnit, FoodUnit, NutritionalAssessment, NutritionalCounselingTime, MedicalNutritionalTherapyUnit, MedicalNutritionalTherapyAssessment, MedicalNutritionalTherapyCounselingTime, RentalAssistanceUnit, UtilityAssistanceUnit, HousingAdvocacyUnit, HousingAdvocacyPlacementUnit, MCMUnitTime, MCMOnlyUnit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', entry)			

	c.commit()
	append_text('Writing to ClientReportService table: OK.')
		
def write_to_ClientReport(df):
	"""Input a DataFrame, and write to the empty Access template in the same folder."""
	df = df.ix[:,'MRN':'GenderID'].drop_duplicates()
	for i in df.index:
		entry = df.MRN[i], df.FirstInitial[i], df.FirstInitial3[i], df.LastInitial[i], df.LastInitial3[i], df.BirthDate[i], df.Last4SSN[i], df.MothersFirstName[i], df.BirthGenderID[i], df.GenderID[i]
		entry = convert_nan_to_none(entry)			
		c.execute('''INSERT INTO ClientReport(ID, FirstInitial, FirstInitial3, LastInitial, LastInitial3, BirthDate, Last4SSN, MothersFirstName, BirthGenderID, GenderID) VALUES(?,?,?,?,?,?,?,?,?,?)''', entry)

	c.commit()
	append_text('Writing to ClientReport table: OK.')

class ValidationCheckerExcelToAccess(object):
	"""Takes in XLS, does various validation checks, and writes to new Access file."""
	def __init__(self, filename):
		self.header_rows = 3 # num of rows on top of file until you get to the column names
		self.df = pd.io.excel.read_excel(filename, header=self.header_rows)
		self.health_center = find_health_center(filename.upper())

	def preprocess(self):
		"""Takes out header and footer, and transforms type in MRN column."""
		self.df = self.df.dropna(how='all') # trying to delete the tail blank rows

		if 'Page -1 of 1' in self.df.tail(1).values[0]: # deleting last row, which in all my tests contains 'Page -1 of 1'
			self.df = self.df.ix[:self.df.shape[0] - 2]
			
		self.df.MRN = self.df.MRN.astype(str).map(transform_MRN)
		
	def check_moms_name(self, df):
		"""Input the DataFrame, and find those rows for which the mom's name contains a number. For those rows, write to file."""
		names_of_moms = df.MothersFirstName.map(lambda x: pd.isnull(x) or ('0' in x) or ('1' in x) or ('2' in x) or ('3' in x) or ('4' in x) or ('5' in x) or ('6' in x) or ('7' in x) or ('8' in x) or ('9' in x))

		indexes_of_names_of_moms = names_of_moms[names_of_moms].index # filtering those which are True

		if len(indexes_of_names_of_moms) == 0:
			text = "Checking for errors in moms' names: No errors."
			append_text(text)
		else:
			for row_num in indexes_of_names_of_moms:
				initials = make_initials(row_num, df)
				if pd.isnull(df.MothersFirstName[row_num]):
					text = "Mom's name for {}/{} is blank. Please update CPS and Excel file for {} row #{}.".format(initials, df.MRN[row_num], self.health_center, row_num + self.header_rows + 2)
				else:
					text = "Mom's name for {}/{} contains number: {}. Please update CPS and Excel file for {} row #{}.".format(initials, df.MRN[row_num], df.MothersFirstName[row_num], self.health_center, row_num + self.header_rows + 2)
				append_text(text)
				raise Exception(text)

	def run(self):
		self.preprocess()
		# self.df = self.df.head(2) # for testing
		check_MCMOnlyTransUnit(self.df, self.health_center)
		check_blank_SSN(self.df)		
		self.check_moms_name(self.df)
		self.df.drop_duplicates(inplace=True)

		try:
			write_to_ClientReport(self.df)
			write_to_ClientReportService(self.df, 'DOR') # bc of the '../'	
		except pypyodbc.IntegrityError:
			append_text("Check the Excel file. An SSN for one of the rows may be missing, where it should not.")
			raise Exception()
			
if __name__ == '__main__':
	try:
		copy_file(filename1, filename2)
	except IOError: # Can alternatively write whole traceback to log using logger.exception()
		append_text("Program can't find the empty Access template. This file should be \\dotwell\dfs\Storage\Departments\DotWell\CDPP\Case Management\Quarterly BPHC Reporting\Access template 2014\e2Boston_RsrPlus-empty.mdb.")
		
	db = pypyodbc.win_connect_mdb(filename2)
	c = db.cursor()

	for file_ in os.listdir('..'):
		file_ = file_.upper()
		if 'COD' in file_:
			append_text('For Codman: \n')
			ValidationCheckerExcelToAccess('../' + file_).run()
		elif 'DOR' in file_:
			append_text('\nFor Dorchester House: \n')			
			ValidationCheckerExcelToAccess('../' + file_).run()
	
	db.close()
	append_text("\nDone! Press any key to exit.")
	raw_input("")
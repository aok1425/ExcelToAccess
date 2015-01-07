# tests all the possibilities for each of the 3 checks. that is all.

from validation_check import *
from numpy import NaN
from nose.tools import raises

test_instance_COD = ValidationCheckerExcelToAccess('./tests/COD Service Utilization Report 2014 Q3.xls')
test_instance_COD.preprocess()

test_instance_DOR = ValidationCheckerExcelToAccess('./tests/DOR Service Utilization Report 2014 Q3.xls')
test_instance_DOR.preprocess()

def test_no_blank_SSNs():
	temp_df = test_instance_COD.df.head().copy()
	temp_df.Last4SSN = 9999
	check_blank_SSN(temp_df)
	assert 'Checking for SSN errors: No errors.' in log_file

def test_one_blank_SSN():
	temp_df = test_instance_COD.df.head().copy()
	temp_df.loc[0, 'Last4SSN'] = None
	check_blank_SSN(temp_df)	
	assert "SSN for JAAC/00017470 is blank. Changed it to '9999' for Access. Please update SSN in CPS." in log_file	

def test_no_MCM_blanks_for_COD():
	temp_df = test_instance_COD.df.head().copy()
	temp_df.MCMOnlyUnit = 1
	check_MCMOnlyUnit(temp_df, 'COD')
	assert 'Checking for MCMOnlyUnit errors: No errors.' in log_file	

def test_no_MCM_blanks_for_DOR():
	temp_df = test_instance_DOR.df.head().copy()
	temp_df.MCMwithTransOnlyUnit = 1
	check_MCMOnlyUnit(temp_df, 'DOR')
	assert 'Checking for MCMwithTransOnlyUnit errors: No errors.' in log_file

def test_one_MCM_blank_for_COD():
	temp_df = test_instance_COD.df.head().copy()
	temp_df.loc[1, 'MCMOnlyUnit'] = None
	check_MCMOnlyUnit(temp_df, 'COD')
	assert "MCMOnlyUnit for 00020087 is not 1. Changing it to 1." in log_file	

def test_one_MCM_blank_for_DOR():
	temp_df = test_instance_DOR.df.head(10).copy()
	temp_df.loc[5, 'MCMwithTransOnlyUnit'] = NaN
	check_MCMOnlyUnit(temp_df, 'DOR')
	assert "MCMwithTransOnlyUnit for 00142383 is not 1. Changing it to 1." in log_file		

def test_moms_name_no_errors():
	temp_df = test_instance_COD.df.head().copy()
	temp_df.MothersFirstName = 'AAA'
	test_instance_COD.check_moms_name(temp_df)
	assert "Checking for errors in moms' names: No errors." in log_file	

@raises(Exception)
def test_moms_name_blank():
	temp_df = test_instance_COD.df.head().copy()
	temp_df.loc[0, 'MothersFirstName'] = NaN	
	test_instance_COD.check_moms_name(temp_df)

def test_err_msg_from_moms_name_blank():
	assert "Mom's name for JAAC/00017470 is blank. Please update CPS and Excel file for COD row #5." in log_file		

@raises(Exception)
def test_moms_name_one_number():
	temp_df = test_instance_COD.df.head(10).copy()
	temp_df.loc[6, 'MothersFirstName'] = 'AA9'
	test_instance_COD.check_moms_name(temp_df)

def test_err_msg_from_moms_name_one_number():
	assert "Mom's name for KTAO/00020087 contains number: AA9. Please update CPS and Excel file for COD row #11." in log_file			
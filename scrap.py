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
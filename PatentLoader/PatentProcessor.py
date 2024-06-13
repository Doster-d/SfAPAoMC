import pandas as pd
import numpy as np
import re


class PatentProcessor:
	"""
	Class for processing patent data, including reading, cleaning, and transforming patent records.

	Methods:
	- __init__: Initializes the DataFrame attributes and defines the columns and data types.
	- read_patents: Reads patent data from an Excel file.
	- load_patents: Loads patent data from a DataFrame.
	- apply_replace_strategy: Replaces missing values in a specific column based on an alternate column.
	- lower_text: Converts text to lowercase.
	- find_foreign: Identifies foreign patents based on specific patterns.
	- process_patent_holder: Cleans and normalizes the patent holder text.
	- split_holders: Splits the patent holders string into unique components.
	- remove_parentheses: Removes text within parentheses.
	- remove_spaces: Removes spaces from text.
	- process_design: Processes each row of the DataFrame to clean and normalize patent data.
	- start_process: Starts the processing of the patent DataFrame.
	"""

	def __init__(self):
		"""
		Initializes the DataFrame attributes and defines the columns and data types.
		"""
		self.patents_ids = pd.DataFrame()
		self.current_patents_dataframe = pd.DataFrame()
		self.current_ids_dataframe = pd.DataFrame()
		self.current_columns = [
			"registration number",
			"patent_holders",
			"authors"
		]
		self.current_dtype = {
			'registration number': int,
		}

	def read_patents(self, read_object):
		"""
		Reads patent data from an Excel file.

		Parameters:
		read_object: Object representing the Excel file (e.g., file path or file-like object).
		"""
		self.current_patents_dataframe = pd.read_excel(
			read_object,
			usecols=self.current_columns,
			dtype=self.current_dtype
		)

	def load_patents(self, patents_df: pd.DataFrame):
		"""
		Loads patent data from a DataFrame.

		Parameters:
		patents_df (pd.DataFrame): DataFrame containing patent data.
		"""
		self.current_patents_dataframe = patents_df

	def apply_replace_strategy(self, row, column='patent processed', column_alt='authors'):
		"""
		Replaces missing values in a specific column based on an alternate column.

		Parameters:
		row (pd.Series): Row of data.
		column (str): Column name to check for missing values.
		column_alt (str): Alternate column name to use for replacement.

		Returns:
		Value from the column or alternate column based on the condition.
		"""
		return row[column_alt] if pd.isna(row[column]) and row[column_alt] != "" else row[column]

	def lower_text(self, text: str) -> str:
		"""
		Converts text to lowercase.

		Parameters:
		text (str): Input text.

		Returns:
		str: Lowercase text.
		"""
		return text.lower()

	def find_foreign(self, row):
		"""
		Identifies foreign patents based on specific patterns.

		Parameters:
		row (pd.Series): Row of data.

		Returns:
		list: List indicating whether each patent holder is foreign.
		"""
		pattern = r'\((.*?)\)'
		data = self.apply_replace_strategy(row, column='patent_holders').lower()
		data = self.process_patent_holder(data)
		mask = []
		preparts = [part.strip() for part in re.split(pattern, data) if part.strip()]
		find = {}
		for ind in range(len(preparts) - 1):
			part = preparts[ind].lower()
			index = preparts[ind + 1].lower()
			if find.get(part) is not None:
				continue
			find[part] = True
			if part in row['patent processed']:
				mask.append(False if index == 'ru' else True)
		patent_len = len(row['patent processed'])
		is_foreign_len = len(mask)
		if patent_len > is_foreign_len:
			mask.extend([False] * (patent_len - is_foreign_len))
		elif patent_len < is_foreign_len:
			mask = mask[:patent_len]
		return mask

	def process_patent_holder(self, text: str) -> str:
		"""
		Cleans and normalizes the patent holder text.

		Parameters:
		text (str): Input text.

		Returns:
		str: Cleaned and normalized text.
		"""
		text = text.replace("ИП", "")
		text = re.split(r'[,:;]+', text)[0]
		text = re.sub(r'[«»"]+', "", text)
		return text

	def split_holders(self, patent_holder: str) -> list:
		"""
		Splits the patent holders string into unique components.

		Parameters:
		patent_holder (str): String of patent holders.

		Returns:
		list: List of unique patent holders.
		"""
		pattern = r"\s*\([^)]*\)\s*"
		parts = [part.strip() for part in re.split(pattern, patent_holder) if part.strip()]
		unique_parts = list(set(parts))
		return unique_parts

	def remove_parentheses(self, text: list) -> list:
		"""
		Removes text within parentheses from a list of strings.

		Parameters:
		text (list): List of strings.

		Returns:
		list: List of strings without parentheses.
		"""
		return [re.sub(r'\([^)]*\)', '', word) for word in text]

	def remove_spaces(self, text: list) -> list:
		"""
		Removes spaces from a list of strings.

		Parameters:
		text (list): List of strings.

		Returns:
		list: List of strings without spaces.
		"""
		return [word.replace(" ", "") for word in text]

	def process_design(self, row: pd.Series) -> pd.Series:
		"""
		Processes each row of the DataFrame to clean and normalize patent data.

		Parameters:
		row (pd.Series): Row of data.

		Returns:
		pd.Series: Processed row of data.
		"""
		row['patent processed'] = self.apply_replace_strategy(row)
		if pd.isna(row['patent_holders']):
			return row
		row['patent processed'] = self.lower_text(row['patent processed'])
		row['patent processed'] = self.process_patent_holder(row['patent processed'])
		row['patent processed'] = self.split_holders(row['patent processed'])
		row['is foreign'] = self.find_foreign(row)
		row['patent processed'] = self.remove_parentheses(row['patent processed'])
		row['patent processed'] = self.remove_spaces(row['patent processed'])

		return row

	def start_process(self):
		"""
		Starts the processing of the patent DataFrame, cleaning and normalizing the data.
		"""
		self.current_patents_dataframe['patent processed'] = self.current_patents_dataframe['patent_holders']
		self.current_patents_dataframe['is foreign'] = np.nan

		self.current_patents_dataframe = self.current_patents_dataframe.apply(
			self.process_design,
			axis=1
		)
		self.patents_ids = self.current_patents_dataframe[["registration_number", "patent processed", 'is foreign']]
		self.patents_ids = self.patents_ids.explode(['patent processed', 'is foreign'])

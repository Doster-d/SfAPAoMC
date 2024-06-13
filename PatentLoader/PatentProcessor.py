import pandas as pd
import numpy as np
import re


class PatentProcessor:
	def __init__(self):
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
		self.current_patents_dataframe = pd.read_excel(
			read_object,
			usecols=self.current_columns,
			dtype=self.current_dtype
		)

	def load_patents(self, patents_df):
		self.current_patents_dataframe = patents_df

	def apply_replace_strategy(self, row, column='patent processed', column_alt='authors'):
		return row[column_alt] if pd.isna(row[column]) and row[column_alt] != "" else row[column]

	def lower_text(self, text):
		return text.lower()

	def find_foreign(self, row):
		pattern = r'\((.*?)\)'
		# mask = [True if word=='ru' else False for word in re.findall(pattern, row)]
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

	def process_patent_holder(self, text):
		text = text.replace("ИП", "")
		text = re.split(r'[,:;]+', text)[0]
		text = re.sub(r'[«»"]+', "", text)
		return text

	def split_holders(self, patent_holder):
		pattern = r"\s*\([^)]*\)\s*"
		# Разделяем строку по паттерну и применяем strip к каждому элементу
		parts = [part.strip() for part in re.split(pattern, patent_holder) if part.strip()]
		# Удаляем дубликаты
		unique_parts = list(set(parts))
		return unique_parts

	def remove_parentheses(self, text):
		return [re.sub(r'\([^)]*\)', '', word) for word in text]

	def remove_spaces(self, text):
		return [word.replace(" ", "") for word in text]

	def process_design(self, row):
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
		self.current_patents_dataframe['patent processed'] = self.current_patents_dataframe['patent_holders']
		self.current_patents_dataframe['is foreign'] = np.nan

		self.current_patents_dataframe = self.current_patents_dataframe.apply(
			self.process_design,
			axis=1
		)
		self.patents_ids = self.current_patents_dataframe[["registration_number", "patent processed", 'is foreign']]
		self.patents_ids = self.patents_ids.explode(['patent processed', 'is foreign'])

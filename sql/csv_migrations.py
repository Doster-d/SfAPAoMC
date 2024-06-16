# ATTENTION! TO RUN THIS FILE YOU NEED AT LEAST 21 GB FREE RAM

import pandas as pd
import asyncpg
import asyncio
import os
import re
from pathlib import Path
from datetime import datetime
import csv

_DEFAULT_PROJECT_PATH = Path(__file__).resolve().parents[1]

PROJECT_ROOT = Path(os.getenv('PROJ_ROOT', _DEFAULT_PROJECT_PATH))
os.chdir(PROJECT_ROOT)


def split_holders(patent_holder):
	pattern = r"\s*\([^)]*\)\s*"
	# Разделяем строку по паттерну и применяем strip к каждому элементу
	parts = [part.strip() for part in re.split(pattern, patent_holder) if part.strip()]
	# Удаляем дубликаты
	unique_parts = list(set(parts))
	return unique_parts


def process_company(
		path_to_file="data/DatabaseOfAllOrganizationsAndIE/DatasetOrg.csv",
		use_columns=None,
		save_to="data/ProcessedData/DatasetOrg"
):
	if use_columns is None:
		use_columns = [
			'ID компании', 'Наименование полное', 'Наименование краткое',
			'ИНН', 'ОГРН', 'ОКВЭД2 расшифровка', 'Головная компания (1) или филиал (0)',
			# 'id Компании-наследника (реорганизация и др)'
		]
	dtype = {
		'ID компании': str,
		'ИНН': str,
		'ОГРН': str,
		'Головная компания (1) или филиал (0)': str,
		# 'id Компании-наследника (реорганизация и др)': str
	}
	chunk_size = 5000000
	chunk_id = 0
	for chunk in pd.read_csv(
			path_to_file,
			sep=';',
			chunksize=chunk_size,
			usecols=use_columns,
			dtype=dtype):
		company_data = chunk.rename(columns={
			'ID компании': 'company_id',
			'Наименование полное': 'full_name',
			'Наименование краткое': 'shorten_name',
			'ИНН': 'tin',
			'ОГРН': 'psrn',
			'ОКВЭД2 расшифровка': 'okved',
			'Головная компания (1) или филиал (0)': 'is_active_company'
		})
		company_data['classification'] = None
		company_data['is_active_company'] = company_data['is_active_company'].apply(
			lambda state: bool(state) if pd.notna(state) else False
		)
		company_data['full_name'] = company_data['full_name'].apply(
			lambda name: name if pd.notna(name) else None
		)
		company_data['shorten_name'] = company_data['shorten_name'].apply(
			lambda name: name if pd.notna(name) else None
		)
		company_data['company_id'] = company_data['company_id'].apply(
			lambda cid: int(cid.replace("\ufeff", ""))
		)
		company_data['tin'] = company_data['tin'].apply(
			lambda nid: nid if pd.notna(nid) and nid.isdigit() else 0
		)
		company_data['psrn'] = company_data['psrn'].apply(
			lambda nid: nid if pd.notna(nid) and nid.isdigit() else 0
		)
		company_data['okved'] = company_data['okved'].apply(
			lambda nid: nid if pd.notna(nid) else None
		)
		company_data.to_csv(
			save_to + str(chunk_id) + ".csv",
			columns=[
				'company_id',
				'full_name',
				'shorten_name',
				'okved',
				'classification',
				'tin',
				'psrn',
				'is_active_company'
			],
			sep=";",
			quotechar="'",
			index=False,
			na_rep='NULL',
			quoting=csv.QUOTE_ALL)
		chunk_id = chunk_id + 1


def process_patent(
		path_to_file="data/PatentDatabaseFromPublicData/POOD.csv",
		use_columns=None,
		patent_type='design',
		save_to="data/ProcessedData/POOD.csv"
):
	if use_columns is None:
		use_columns = [
			'registration number', 'registration date', 'authors', 'patent holders', 'actual', 'industrial design name']
	dtype = {
		'registration number': str,
		'registration date': str,
		'actual': bool
	}
	date_format = "%Y%m%d"
	unix_start_time = datetime.strptime('19700101', date_format)
	patent_data = pd.read_csv(
		path_to_file,
		usecols=use_columns,
		dtype=dtype
	)
	patent_data['registration number'] = patent_data['registration number'].apply(
		lambda id: int(id.replace("\ufeff", ""))
	)
	patent_data['patent holders'] = patent_data.apply(
		lambda row: row['authors'] if pd.isna(row['patent holders']) and row['authors'] != "" else row[
			'patent holders'],
		axis=1
	)
	patent_data['registration date'] = patent_data['registration date'].apply(
		lambda date: datetime.strptime(date, date_format) if pd.notna(date) else unix_start_time
	)
	patent_data['actual'] = patent_data['actual'].apply(
		lambda state: state if pd.notna(state) else False
	)
	patent_data = patent_data.rename(columns={
		'registration number': 'registration_number',
		'registration date': 'publish_date',
		'patent holders': 'patent_holders',
		'actual': 'is_active',
	})
	# patent_data['is_model'] = patent_type == 'model'
	# patent_data['is_invention'] = patent_type == 'invention'
	# patent_data['is_design'] = patent_type == 'design'
	if patent_type == 'design':
		patent_data['industrial design name'] = patent_data['industrial design name'].apply(
			lambda desc: desc if pd.notna(desc) else ""
		)
		patent_data = patent_data.rename(columns={
			'industrial design name': 'description'
		})
	elif patent_type == 'model':
		patent_data['utility model name'] = patent_data['utility model name'].apply(
			lambda desc: desc if pd.notna(desc) else ""
		)
		patent_data = patent_data.rename(columns={
			'utility model name': 'description'
		})
	else:
		patent_data['invention name'] = patent_data['invention name'].apply(
			lambda desc: desc if pd.notna(desc) else ""
		)
		patent_data = patent_data.rename(columns={
			'invention name': 'description'
		})
	patent_data.to_csv(
		save_to,
		quotechar="'",
		index=False,
		na_rep='NULL',
		quoting=csv.QUOTE_ALL
	)


process_patent()

process_patent(path_to_file="data/PatentDatabaseFromPublicData/PMOD.csv", use_columns=[
	'registration number', 'registration date', 'authors', 'patent holders', 'actual', 'utility model name'
], patent_type='model', save_to="data/ProcessedData/PMOD.csv")

process_patent(path_to_file="data/PatentDatabaseFromPublicData/inventionsOD.csv", use_columns=[
	'registration number', 'registration date', 'authors', 'patent holders', 'actual', 'invention name'
], patent_type='invention', save_to="data/ProcessedData/inventionsOD.csv")

process_company()

import pandas as pd


# Copy and modify this function to update DB with csv data
def db_load_func(data: pd.DataFrame):
	# your code here
	# DataFrame.to_sql(name, con, *, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None,
	# dtype=None, method=None)
	# DataFrame.rename(columns={'oldName': 'newName'})
	pass


def load_data_chunk(
		func_chunk,
		chunk_size=1000000,
		path_to_file="data/DatabaseOfAllOrganizationsAndIE/DatasetOrg.csv",
		sep=";",
		low_memory=False,
		use_columns=None
):
	if use_columns is None:
		use_columns = [
			'ID компании', 'Наименование полное', 'Юр адрес', 'Факт адрес', 'Наименование краткое', 'ИНН', 'ОГРН'
		]

	for chunk in pd.read_csv(
			path_to_file,
			sep=sep,
			chunksize=chunk_size,
			usecols=use_columns,
			low_memory=low_memory):
		func_chunk(chunk)


def load_data_csv(
		func,
		path_to_file="data/PatentDatabaseFromPublicData/POOD.csv",
		use_columns=None):
	if use_columns is None:
		use_columns = [
			'registration number', 'registration date', 'authors', 'patent holders', 'actual', 'industrial design name']
	loaded_data = pd.read_csv(
		path_to_file,
		usecols=use_columns)
	func(loaded_data)


load_data_csv(db_load_func)

load_data_csv(db_load_func, path_to_file="data/PatentDatabaseFromPublicData/PMOD.csv", use_columns=[
	'registration number', 'registration date', 'authors', 'patent holders', 'actual', 'utility model name'
])

load_data_csv(db_load_func, path_to_file="data/PatentDatabaseFromPublicData/inventionsOD.csv", use_columns=[
	'registration number', 'registration date', 'authors', 'patent holders', 'actual', 'invention name'
])

load_data_chunk(db_load_func)

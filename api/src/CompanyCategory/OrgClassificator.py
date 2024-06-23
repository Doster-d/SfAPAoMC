import logging
from .OrgDatabaseLink import OrgDatabaseLink

try:
    import cudf.pandas
except ImportError:
    pass
import pandas as pd
import asyncio
import numpy as np
from icecream import ic

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def update_category_count(row, categories):
	category = row["okved"]
	ic(category)
	if category in categories:
		categories[category] += 1
	return row

def fix_row(row):
	"""
		    Fixes the format of 'company_id' and 'patent processed' fields in the row.

		    Parameters:
		    row (pd.Series): The row from the DataFrame.

		    Returns:
		    pd.Series: The fixed row.
		"""
	logging.info("Starting fix_row")
	row['patent processed'] = row['patent processed'].replace("]", "").replace("[", "").replace("'", "").split(', ')

	try:
		row['company_id'] = row['company_id'].replace("]", "").replace("[", "")
		row['company_id'] = row['company_id'].split(', ')
		row['company_id'] = [str(int(id.replace(" ", "").split('.')[0])) if id != 'nan' and len(id) > 0 else np.nan for
		                     id
		                     in row['company_id']]
		row['company_id'] = row['company_id'][:len(row['patent processed'])]
	except AttributeError:
		row['company_id'] = [np.nan]

	logging.info("Completed fix_row")
	return row


class OrgClassificator:
	"""
    Class for classifying organizations and patents based on their OKVED descriptions and company data.

    Methods:
    - __init__: Initializes the OrgClassificator with necessary attributes and links.
    - reset_classification: Resets the classification dictionary.
    - reset_global_classification: Resets the global classification dictionary.
    - classify_companies: Classifies a chunk of company data.
    - classify_company: Classifies companies based on provided IDs.
    - classify_patent: Classifies patents by type.
    - run_process_manual: Runs the classification process for companies manually.
    - run_process_manual_patents: Runs the classification process for patents manually.
    """

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(OrgClassificator, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		"""
        Initializes the OrgClassificator with necessary attributes and links.
        """
		logging.info("Initializing OrgClassificator")
		self.dirty = True
		self.classification = None
		self.link = OrgDatabaseLink()
		self.reset_classification()
		self.reset_global_classification()
		logging.info("OrgClassificator initialized")

	def reset_classification(self):
		"""
        Resets the classification dictionary.
        """
		self.classification = {
			"count": 0,
			"count_found": 0,
			"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			"categories": {
				"ВУЗ": 0,
				"Высокотехнологичные ИТ компании": 0,
				"Добывающая промышленность": 0,
				"Здравоохранение и социальные услуги": 0,
				"Колледжи": 0,
				"Медиа и развлечения": 0,
				"Научные организации": 0,
				"Нет категории": 0,
				"Обрабатывающая промышленность": 0,
				"Розничная торговля": 0,
				"Сельское хозяйство и пищевая промышленность": 0,
				"Строительство и недвижимость": 0,
				"Транспорт и логистика": 0,
				"Туризм и гостиничный бизнес": 0,
				"Финансовые услуги": 0,
				"Энергетика": 0,
				"Юридические и профессиональные услуги": 0,
			},
		}
		logging.info('reset_classification complete')

	def reset_global_classification(self):
		"""
        Resets the global classification dictionary.
        """
		self.global_classification = {
			"model": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			},
			"design": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			},
			"invention": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			},
		}
		logging.info('reset_global_classification complete')

	async def classify_companies(
			self,
			chunk: pd.DataFrame,
			patent_type="all",
			classify_categories=True,
			target_classifier=None,
			total=None
	):
		"""
        Classifies a chunk of company data.

        Parameters:
        chunk (pd.DataFrame): DataFrame containing a chunk of company data.
        patent_type (str): Type of patent (default is "all").
        classify_categories (bool): Whether to classify categories (default is True).
        target_classifier (dict): Target classifier dictionary (default is None).
        """
		logging.info("start processing company chunk")
		if target_classifier is None:
			target_classifier = self.classification
		if total:
			target_classifier["count"] = total
		if classify_categories:
			company_class = self.link.category_detector(
				chunk, okvd_column_name="okved", new_column_name="classification"
			)
		for ind, row in chunk.iterrows():
			if not total:
				target_classifier["count"] += 1
			full_name = row["full_name"]
			await self.count_company(full_name, target_classifier)
			# if await self.link.does_exist_in_holders(row["company_id"], patent_type):
			target_classifier["count_found"] += 1
			if classify_categories:
				company_class.apply(update_category_count, axis=1, categories=target_classifier["categories"])
		logging.info("company chunk proceesed")

	async def count_company(self, full_name, target_classifier):
		logging.info("Starting count_company function")
		full_name = full_name.lower()
		if any(le_class in full_name for le_class in ["организация", "общество", "предприятие"]):
			target_classifier["patent_holders"]["LE"] += 1
		elif any(ie_class in full_name for ie_class in ["индивидуальный предприниматель", "ип"]):
			target_classifier["patent_holders"]["IE"] += 1
		else:
			target_classifier["patent_holders"]["PE"] += 1
		logging.info("Completed count_company function")

	async def classify_company(
			self,
			company_ids,
			patent_type="all",
			classify_categories=True,
			target_classifier=None,
	):
		"""
        Classifies companies based on provided IDs.

        Parameters:
        company_ids (list): List of company IDs.
        patent_type (str): Type of patent (default is "all").
        classify_categories (bool): Whether to classify categories (default is True).
        target_classifier (dict): Target classifier dictionary (default is None).
        """
		logging.info("Starting classify_company")
		self.reset_classification()
		if company_ids is None:
			return
		clear_company_ids = [id for id in company_ids if type(id) == str]
		async for chunk in self.link.fetch_company_entities_in_chunks(
				5000000, clear_company_ids
		):
			await self.classify_companies(
				chunk, patent_type, classify_categories, target_classifier, total=len(company_ids)
			)
		logging.info("FINISHED classify_company")

	async def classify_patent(self):
		"""
        Classifies patents by type.

        Parameters:
        patent_type (str): Type of patent (default is "design").

        Returns:
        None
        """
		logging.info("Starting classify_patent")
		self.dirty = False
		self.reset_global_classification()
		for patent_type in ["design", "model", "invention"]:
			chunks = []
			async for chunk in self.link.fetch_patent_entities_in_chunks(
					5000000, patent_type
			):
				chunks = list(set(chunk + chunks))
			chunks = [str(i) for i in chunks if type(i) != str]
			company_ids = []
			async for company_ids_chunk in self.link.fetch_holder_entities_in_chunks_by_ids(
					chunks, 5000000, patent_type
			):
				company_ids = list(set(company_ids + company_ids_chunk))
			company_ids = [str(i) for i in company_ids if type(i) != str]
			await self.classify_company(
				company_ids, patent_type, False, self.global_classification[patent_type]
			)
		logging.info("FINISHED classify_patent")

	def get_company_ids_from_excel(self, file_path):
		logging.info("Starting get_company_ids_from_excel")
		try:
			df = pd.read_excel(file_path, usecols={'company_id', 'patent processed'})
			df = df.apply(
				fix_row, axis=1
			)
			company_ids = df['company_id'][df['company_id'] != np.nan].to_list()
			company_ids = [item for sublist in company_ids for item in sublist]
			logging.info("Completed get_company_ids_from_excel")
			return company_ids
		except ValueError:
			logging.error(f"Failed with {file_path}")
			return None

	async def classify_companies_by_tin_data(self, data_df: pd.DataFrame):
		logging.info("Starting classify_companies_by_tin_data")
		self.reset_classification()
		categories_template = {
			"ВУЗ": 0,
			"Высокотехнологичные ИТ компании": 0,
			"Добывающая промышленность": 0,
			"Здравоохранение и социальные услуги": 0,
			"Колледжи": 0,
			"Медиа и развлечения": 0,
			"Научные организации": 0,
			"Нет категории": 0,
			"Обрабатывающая промышленность": 0,
			"Розничная торговля": 0,
			"Сельское хозяйство и пищевая промышленность": 0,
			"Строительство и недвижимость": 0,
			"Транспорт и логистика": 0,
			"Туризм и гостиничный бизнес": 0,
			"Финансовые услуги": 0,
			"Энергетика": 0,
			"Юридические и профессиональные услуги": 0,
		}

		classification = {
			"model": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			},
			"design": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			},
			"invention": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {"LE": 0, "PE": 0, "IE": 0},
			},
			"general_classification": categories_template
		}
		company_names = data_df.set_index('company_id')['full_name'].to_dict()
		result = await self.link.check_company_in_patent_holders(set(data_df['company_id'].unique()))
		for company_id, patents in result.items():
			if patents:
				# print(f"Company ID {company_id} has the following patents:")
				for patent_id, patent_type, description in patents:
					classification[patent_type]["count"] += 1
					classification[patent_type]["count_found"] += 1
					await self.count_company(company_names[company_id], classification[patent_type])
					# print(f"  - Patent ID {patent_id} ({patent_type}): {description}")
			else:
				classification["model"]["count"] += 1
				classification["design"]["count"] += 1
				classification["invention"]["count"] += 1
				# print(f"Company ID {company_id} is not found in any patent types")
			data_df = self.link.category_detector(
				data_df, okvd_column_name="okved", new_column_name="classification"
			)
			data_df.apply(update_category_count, axis=1, categories=classification["general_classification"])
		logging.info("Completed classify_companies_by_tin_data")
		return classification

	async def get_company_data_from_excel_tin(self, file_path):
		logging.info("Starting get_company_data_from_excel_tin")
		try:
			df = pd.read_excel(file_path, dtype={'ИНН': str})
			if 'ИНН' not in df.columns.to_list():
				return None
			tins = [int(tin) for tin in df['ИНН'].to_list()]
			ic(tins)
			data = await self.link.fetch_company_data_by_tin(tins)
			logging.info("Completed get_company_data_from_excel_tin")
			return data
		except ValueError:
			logging.error(f"Failed with {file_path}")
			return None

	async def get_global_classification(self):
		logging.info('start get_global_classification')
		counts = await self.link.fetch_patent_info()
		global_classification = {
	        "model": {
	            "count": counts["model"]["count"],
	            "count_found": counts["model"]["count_found"],
		        "patent_holders": counts["model"]["patent_holders"]
	        },
	        "design": {
	            "count": counts["design"]["count"],
	            "count_found": counts["design"]["count_found"],
		        "patent_holders": counts["design"]["patent_holders"]
	        },
	        "invention": {
	            "count": counts["invention"]["count"],
	            "count_found": counts["invention"]["count_found"],
		        "patent_holders": counts["invention"]["patent_holders"]
	        },
        }
		logging.info('finish get_global_classification')
		return global_classification

	def run_process_manual(self, company_ids):
		"""
        Runs the classification process for companies manually.

        Parameters:
        company_ids (list): List of company IDs.

        Returns:
        None
        """
		logging.info("Starting run_process_manual")
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.classify_company(company_ids))
		ic(self.classification)
		logging.info("Completed run_process_manual")


	def run_process_manual_patents(self, file_path):
		"""
        Runs the classification process for patents manually.

        Parameters:
        patent_ids (list): List of patent IDs.

        Returns:
        None
        """
		logging.info("Starting run_process_manual_patents")
		loop = asyncio.get_event_loop()
		company_ids = self.get_company_ids_from_excel(file_path)
		loop.run_until_complete(self.classify_company(
			company_ids, classify_categories=False, target_classifier=self.global_classification["design"]
		))
		print(self.global_classification)
		logging.info("Completed run_process_manual_patents")


if __name__ == "__main__":
	"""
	The basic block to start the data processing.

	Example:
	company_ids = [
		1627747, 1627748, 1627749, 1627750, 1627751, 1627752, 1627753, 1627754, 1627755, 1627756, 1627757,
		1627758, 1627759, 1627760, 1627761, 1627762, 1627764, 1627765, 1627766, 1627767, 1627768, 1627769,
		1627771, 1627772, 1627773, 1627774, 1627775, 1627776, 1627777, 1627778, 1627779, 1627780, 1627781
	]
	company_ids = [str(i) for i in company_ids]
	dblink = OrgDatabaseLink()
	dblink.run_process(company_ids)
	"""
	company_ids = [
		27245300,
		23835322,
		23940849,
		26473466,
		27511281,
		27796092,
		28742157,
		29031331,
		30459384,
		30517450,
		30743235,
		32535242,
		33797639,
		34458207,
		36602820,
		37191647,
		45339716,
		48378043,
		49078539,
		49704514,
		50253625,
		52103220,
		52446822,
		52926946,
		1628643,
		38369653,
		38370517,
		38581294,
		38710519,
		38820990,
		38984383,
		39337464,
		40338087,
		42148869,
		42337884,
		42337912,
		43294502,
		43658673,
		15115574,
		15115574,
		20758360,
		1663223,
		29935058,
		30073926,
		49921048,
		29477739,
		32701351,
		45763729,
		27352705,
		27529093,
		31438054,
		48456946,
		19013181,
		27420805,
		32412966,
		27420805,
		32412966,
		26481680,
		26680151,
		27991975,
		28653781,
		28798143,
		30138166,
		31446154,
		32761837,
		33855235,
		34635876,
		35486305,
		35683480,
		36895932,
		45780143,
		48309759,
		50405906,
		52333131,
		52513423,
		1678798,
		15217470,
		18167886,
		18822653,
		19409748,
		38426098,
		39735709,
		18350654,
		27123674,
		25451318,
		25604095,
		25910336,
		26083864,
		26905461,
		26993629,
		27147811,
		27161057,
		27368215,
		27481526,
		27512075,
		28024457,
		28181810,
		28611269,
		28674010,
		29021828,
	]
	patent_ids = [
		100001,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100002,
		100004,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100005,
		100006,
		100007,
		100008,
		100016,
		100017,
		100017,
		100017,
		100018,
		100018,
		100018,
		100036,
		100036,
		100036,
		100036,
		100037,
		100039,
		100039,
		100040,
		100040,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100045,
		100060,
		100061,
		100061,
		100061,
		100061,
		100061,
		100061,
		100086,
		100088,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
		100092,
	]
	company_ids = [str(i) for i in company_ids]
	# patent_ids = [str(i) for i in patent_ids]
	dblink = OrgClassificator()
	# dblink.run_process_manual(company_ids)
	dblink.run_process_manual_patents("../../../data/Обработанный_DesignsSmall1.xlsx")

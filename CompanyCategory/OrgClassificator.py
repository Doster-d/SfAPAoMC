from OrgCategory import CategoryDetector
from OrgDatabaseLink import OrgDatabaseLink
import os
import pandas as pd
import asyncio

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

	def __init__(self):
		"""
		Initializes the OrgClassificator with necessary attributes and links.
		"""
		self.classification = None
		self.link = OrgDatabaseLink()

	async def reset_classification(self):
		"""
		Resets the classification dictionary.
		"""
		self.classification = {
			"count": 0,
			"count_found": 0,
			"patent_holders": {
				"LE": 0,
				"PE": 0,
				"IE": 0
			},
			"categories": {
				"Сельское хозяйство и пищевая промышленность": 0,
				"Добывающая промышленность": 0,
				"Обрабатывающая промышленность": 0,
				"Энергетика": 0,
				"Строительство и недвижимость": 0,
				"Транспорт и логистика": 0,
				"Высокотехнологичные ИТ компании": 0,
				"Финансовые услуги": 0,
				"Здравоохранение и социальные услуги": 0,
				"Туризм и гостиничный бизнес": 0,
				"Розничная торговля": 0,
				"Медиа и развлечения": 0,
				"Юридические и профессиональные услуги": 0,
				"Колледжи": 0,
				"ВУЗ": 0,
				"Научные организации": 0
			}
		}

	async def reset_global_classification(self):
		"""
		Resets the global classification dictionary.
		"""
		self.global_classification = {
			"model": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {
					"LE": 0,
					"PE": 0,
					"IE": 0
				}
			},
			"design": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {
					"LE": 0,
					"PE": 0,
					"IE": 0
				}
			},
			"invention": {
				"count": 0,
				"count_found": 0,
				"patent_holders": {
					"LE": 0,
					"PE": 0,
					"IE": 0
				}
			}
		}

	async def classify_companies(
			self,
			chunk: pd.DataFrame,
			patent_type="all",
			classify_categories=True,
			target_classifier=None
	):
		"""
		Classifies a chunk of company data.

		Parameters:
		chunk (pd.DataFrame): DataFrame containing a chunk of company data.
		patent_type (str): Type of patent (default is "all").
		classify_categories (bool): Whether to classify categories (default is True).
		target_classifier (dict): Target classifier dictionary (default is None).
		"""
		if target_classifier is None:
			target_classifier = self.classification
		if classify_categories:
			company_class = self.link.category_detector(chunk, okvd_column_name='okved', new_column_name='classification')
		for ind, row in chunk.iterrows():
			target_classifier["count"] += 1
			full_name = row["full_name"]
			if any(le_class in full_name for le_class in ['организация', 'общество', 'предприятие']):
				target_classifier["patent_holders"]["LE"] += 1
			elif any(ie_class in full_name for ie_class in ['индивидуальный предприниматель', 'ИП']):
				target_classifier["patent_holders"]["IE"] += 1
			else:
				target_classifier["patent_holders"]["PE"] += 1
			if await self.link.does_exist_in_holders(row["company_id"], patent_type):
				target_classifier["count_found"] += 1
			if classify_categories:
				target_classifier["categories"][company_class.loc[ind]["classification"]] += 1

	async def classify_company(self, company_ids, patent_type="all", classify_categories=True, target_classifier=None):
		"""
		Classifies companies based on provided IDs.

		Parameters:
		company_ids (list): List of company IDs.
		patent_type (str): Type of patent (default is "all").
		classify_categories (bool): Whether to classify categories (default is True).
		target_classifier (dict): Target classifier dictionary (default is None).
		"""
		await self.reset_classification()
		async for chunk in self.link.fetch_company_entities_in_chunks(5000000, company_ids):
			await self.classify_companies(chunk, patent_type, classify_categories, target_classifier)

	async def classify_patent(self, patent_type="design"):
		"""
		Classifies patents by type.

		Parameters:
		patent_type (str): Type of patent (default is "design").

		Returns:
		None
		"""
		await self.reset_global_classification()
		for patent_type in ['design', 'model', 'invention']:
			chunks = []
			async for chunk in self.link.fetch_holder_entities_in_chunks(5000000, patent_type):
				chunks = list(set(chunk["company_id"].to_list() + chunks))
			chunks = [str(i) for i in chunks if type(i) != str]
			await self.classify_company(chunks, patent_type, False, self.global_classification[patent_type])

	def run_process_manual(self, company_ids):
		"""
		Runs the classification process for companies manually.

		Parameters:
		company_ids (list): List of company IDs.

		Returns:
		None
		"""
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.classify_company(company_ids))
		print(self.classification)

	def run_process_manual_patents(self, patent_ids):
		"""
		Runs the classification process for patents manually.

		Parameters:
		patent_ids (list): List of patent IDs.

		Returns:
		None
		"""
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.classify_patent(patent_ids))
		print(self.global_classification)


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
		27245300, 23835322, 23940849, 26473466, 27511281, 27796092, 28742157, 29031331, 30459384, 30517450,
		30743235, 32535242, 33797639, 34458207, 36602820, 37191647, 45339716, 48378043, 49078539, 49704514,
		50253625, 52103220, 52446822, 52926946, 1628643, 38369653, 38370517, 38581294, 38710519, 38820990,
		38984383, 39337464, 40338087, 42148869, 42337884, 42337912, 43294502, 43658673, 15115574, 15115574,
		20758360, 1663223, 29935058, 30073926, 49921048, 29477739, 32701351, 45763729, 27352705, 27529093,
		31438054, 48456946, 19013181, 27420805, 32412966, 27420805, 32412966, 26481680, 26680151, 27991975,
		28653781, 28798143, 30138166, 31446154, 32761837, 33855235, 34635876, 35486305, 35683480, 36895932,
		45780143, 48309759, 50405906, 52333131, 52513423, 1678798, 15217470, 18167886, 18822653, 19409748,
		38426098, 39735709, 18350654, 27123674, 25451318, 25604095, 25910336, 26083864, 26905461, 26993629,
		27147811, 27161057, 27368215, 27481526, 27512075, 28024457, 28181810, 28611269, 28674010, 29021828
	]
	patent_ids = [
		100001, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002,
		100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100002, 100004, 100005, 100005, 100005,
		100005, 100005, 100005, 100005, 100005, 100005, 100005, 100005, 100005, 100005, 100006, 100007, 100008, 100016,
		100017, 100017, 100017, 100018, 100018, 100018, 100036, 100036, 100036, 100036, 100037, 100039, 100039, 100040,
		100040, 100045, 100045, 100045, 100045, 100045, 100045, 100045, 100045, 100045, 100045, 100045, 100045, 100045,
		100045, 100045, 100045, 100045, 100045, 100060, 100061, 100061, 100061, 100061, 100061, 100061, 100086, 100088,
		100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092, 100092,
		100092, 100092
	]
	company_ids = [str(i) for i in company_ids]
	patent_ids = [str(i) for i in patent_ids]
	dblink = OrgClassificator()
	dblink.run_process_manual(company_ids)
	dblink.run_process_manual_patents(patent_ids)

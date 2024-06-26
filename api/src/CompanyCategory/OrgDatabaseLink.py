from .OrgCategory import CategoryDetector
import os

try:
	import cudf.pandas
except ImportError:
	pass
import pandas as pd
import asyncpg
import asyncio
from icecream import ic

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OrgDatabaseLink:
	"""
    A class for working with organization database and data classification.

    Methods:
    - __init__: Initialization of connection and classifier parameters.
    - fetch_company_entities: Retrieve data of organizations by their ID.
    - fetch_company_entities_in_chunks: Fetch organization data by chunks.
    - fetch_holder_entities: Retrieve data of patent holders by offset and limit.
    - fetch_holder_entities_in_chunks: Fetch patent holder data by chunks.
    - does_exist_in_holders: Check if a company exists in the patent holders table.
    - process_company: Process company data with its classification.
    - run_process: Start the data processing.
    - insert_classification: Inserting the classification results into the database.
    - update_classification: Updating the classification in the database.
    """

	def __init__(self):
		"""
        Initializes the connection parameters and classifier.
        """
		logging.info("Initializing OrgDatabaseLink")
		self.chunk_size = int(os.getenv("chunk_size", "5000000"))
		self.port = os.getenv("DB_port", 5432)
		self.host = os.getenv("DB_address", "postgres")
		self.user = os.getenv("DB_user", "patentexpertuser")
		self.password = os.getenv("DB_pass", "mycoolpassword123")
		self.database = os.getenv("DB_db", "patentanal")
		self.category_detector = CategoryDetector()
		logging.info("OrgDatabaseLink initialized")

	async def get_connection(self):
		return await asyncpg.connect(
			user = self.user,
			password = self.password,
			database = self.database,
			host = self.host,
			port = self.port
		)

	async def fetch_company_entities(self, target_ids, offset, limit, target_where="company_id", use_offset=True):
		"""
        Fetches the data of organizations by their IDs.

        Parameters:
        company_ids (list): List of company IDs.
        offset (int): Offset for data sampling.
        limit (int): The limit of the data sample.

        Returns:
        list: Records from the database.
        """
		logging.info("Starting fetch_company_entities function")
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)

		offset_limit_clause = "OFFSET $2 LIMIT $3" if use_offset else ""

		query = f"""
		SELECT company_id, okved, full_name
		FROM HOLDER_ENTITY
		WHERE {target_where} = ANY($1::bigint[])
		{offset_limit_clause};
		"""

		ic(query)

		params = [target_ids]
		if use_offset:
			params.extend([offset, limit])

		try:
			records = await conn.fetch(query, *params)
		except Exception as e:
			ic(e)
			records = {'company_id': [], 'okved': [], 'full_name': []}
		finally:
			await conn.close()

		ic(len(records))
		logging.info("Completed fetch_company_entities function")
		return records

	async def fetch_patent_chunks(self, query, conn, count_company_func, global_classification, patent_type,
	                              chunk_size=int(os.getenv("chunk_size", '500000'))):
		offset = 0
		while True:
			chunk = await conn.fetch(query, chunk_size, offset)
			if not chunk:
				break
			for record in chunk:
				await count_company_func(record['full_name'], global_classification[patent_type])
			offset += chunk_size

	async def fetch_patent_info(self):
		logging.info("Starting fetch_patent_info function")
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)
		QUERIES = {
			"model": {
				"count": "SELECT COUNT(*) FROM PATENT_MODEL;",
				"count_found": "SELECT COUNT(DISTINCT patent_id) FROM PATENT_MODEL_HOLDER;",
				"class_counts": """
		            SELECT classification, COUNT(DISTINCT pmh.patent_id) AS count
		            FROM HOLDER_ENTITY he 
		            JOIN PATENT_MODEL_HOLDER pmh ON he.company_id = pmh.company_id 
		            GROUP BY classification;
		        """
			},
			"invention": {
				"count": "SELECT COUNT(*) FROM PATENT_INVENTION;",
				"count_found": "SELECT COUNT(DISTINCT patent_id) FROM PATENT_INVENTION_HOLDER;",
				"class_counts": """
		            SELECT classification, COUNT(DISTINCT pih.patent_id) AS count
		            FROM HOLDER_ENTITY he 
		            JOIN PATENT_INVENTION_HOLDER pih ON he.company_id = pih.company_id 
		            GROUP BY classification;
		        """
			},
			"design": {
				"count": "SELECT COUNT(*) FROM PATENT_DESIGN;",
				"count_found": "SELECT COUNT(DISTINCT patent_id) FROM PATENT_DESIGN_HOLDER;",
				"class_counts": """
		            SELECT classification, COUNT(DISTINCT pdh.patent_id) AS count
		            FROM HOLDER_ENTITY he 
		            JOIN PATENT_DESIGN_HOLDER pdh ON he.company_id = pdh.company_id 
		            GROUP BY classification;
		        """
			}
		}
		results = {}
		for key, q_dict in QUERIES.items():
			results[key] = {}
			for label, query in q_dict.items():
				if label == "class_counts":
					class_counts = await conn.fetch(query)
					results[key]["patent_holders"] = {"LE": 0, "PE": 0, "IE": 0}
					for record in class_counts:
						results[key]["patent_holders"][record['classification']] = record['count']
				else:
					result = await conn.fetchval(query)
					results[key][label] = result
		await conn.close()
		logging.info("Completed fetch_patent_info function")
		return results


	async def does_exist_in_holders(self, company_id, patent_type="all"):
		"""
        Check if a company exists in the patent holders table.

        Parameters:
        company_id (int): The ID of the company.
        patent_type (str): Type of patent (default is "all").

        Returns:
        bool: True if the company exists, False otherwise.
        """
		logging.info("Starting does_exist_in_holders function")
		query = """
		SELECT EXISTS (
			SELECT 1 FROM PATENT_MODEL_HOLDER WHERE company_id = $1
			UNION
			SELECT 1 FROM PATENT_INVENTION_HOLDER WHERE company_id = $1
			UNION
			SELECT 1 FROM PATENT_DESIGN_HOLDER WHERE company_id = $1
		);
		"""

		if patent_type == "model":
			query = """
			SELECT EXISTS (
				SELECT 1
				FROM PATENT_MODEL_HOLDER
				WHERE company_id = $1
			);
			"""
		elif patent_type == "design":
			query = """
			SELECT EXISTS (
				SELECT 1
				FROM PATENT_DESIGN_HOLDER
				WHERE company_id = $1
			);
			"""
		elif patent_type == "invention":
			query = """
			SELECT EXISTS (
				SELECT 1
				FROM PATENT_INVENTION_HOLDER
				WHERE company_id = $1
			);
			"""
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)
		async with conn.transaction():
			exists = await conn.fetchval(query, company_id)
		await conn.close()
		logging.info("Completed does_exist_in_holders function")
		return exists

	async def fetch_company_entities_in_chunks(self, chunk_size, company_ids):
		"""
        Fetches organization data in chunks.

        Parameters:
        chunk_size (int): The size of the chunk to sample the data.
        company_ids (list): List of company IDs.

        Returns:
        generator: A DataFrame generator with data of organizations.
        """
		logging.info("Starting fetch_company_entities_in_chunks function")
		if len(company_ids) <= 0:
			return
		offset = 0
		while True:
			records = await self.fetch_company_entities(company_ids, offset, chunk_size)
			if not records:
				break
			df_chunk = pd.DataFrame(
				records, columns=["company_id", "okved", "full_name"]
			)
			yield df_chunk
			offset += chunk_size
		logging.info("Completed fetch_company_entities_in_chunks function")

	async def fetch_patent_entities_in_chunks(self, chunk_size, patent_type="design"):
		"""
        Fetches organization data in chunks.

        Parameters:
        chunk_size (int): The size of the chunk to sample the data.
        company_ids (list): List of company IDs.

        Returns:
        generator: A DataFrame generator with data of organizations.
        """
		logging.info("Starting fetch_patent_entities_in_chunks function")
		offset = 0
		while True:
			records = await self.fetch_patent_entities(patent_type, offset, chunk_size)
			if not records:
				break
			yield records
			offset += chunk_size
		logging.info("Completed fetch_patent_entities_in_chunks function")


	async def fetch_patent_entities(self, patent_type, offset, limit):
		"""
		  Fetches patent data by chunks.

		  Parameters:
		  offset (int): Offset for data sampling.
		  limit (int): The limit of the data sample.
		  patent_type (str): Type of patent (default is "design").

		  Returns:
		  list: Records from the database.
		  """
		logging.info("Starting fetch_patent_entities")
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)

		patent_types = {
			"model": "patent_model",
			"design": "patent_design",
			"invention": "patent_invention",
		}
		query = f"""
        		SELECT registration_number
        		FROM {patent_types[patent_type]}
        		OFFSET {offset} LIMIT {limit};
        		"""

		records = await conn.fetch(query)
		await conn.close()
		if records is None:
			return records
		logging.info("Finished fetch_patent_entities")
		return [record['registration_number'] for record in records]

	async def fetch_company_data_by_tin(self, tins):
		"""
		Fetches organization data in chunks.

		Parameters:
		chunk_size (int): The size of the chunk to sample the data.
		company_ids (list): List of company IDs.

		Returns:
		generator: A DataFrame generator with data of link between patents and organizations.
		"""
		logging.info("Starting fetch_company_data_by_tin")
		records = await self.fetch_company_entities(
			tins,
			offset=0,
			limit=0,
			use_offset=False,
			target_where="tin")
		if not records:
			return
		logging.info("Completed fetch_company_data_by_tin")
		return pd.DataFrame(
			records, columns=["company_id", "okved", "full_name"]
		)

	async def fetch_description(self, conn, patent_id, patent_type):
		"""
		Fetches the description of the patent based on patent_id and patent_type.

		Parameters:
		conn (Connection): The database connection.
		patent_id (int): The ID of the patent.
		patent_type (str): The type of the patent.

		Returns:
		str: The description of the patent.
		"""
		logging.info("Starting fetch_description function")
		table_mapping = {
			'model': 'PATENT_MODEL',
			'design': 'PATENT_DESIGN',
			'invention': 'PATENT_INVENTION'
		}

		query = f"SELECT description FROM {table_mapping[patent_type]} WHERE registration_number = $1"
		record = await conn.fetchrow(query, patent_id)
		logging.info("Completed fetch_description function")
		return record['description'] if record else None

	async def check_company_in_patent_holders(self, company_ids):
		"""
		Checks if company_ids are present in PATENT_MODEL_HOLDER, PATENT_DESIGN_HOLDER, or PATENT_INVENTION_HOLDER
		and fetches the descriptions.

		Parameters:
		company_ids (list): List of company_ids to check.

		Returns:
		dict: Dictionary with company_id as key and list of tuples (patent_id, patent_type, description) where the company_id is found.
		"""
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)
		logging.info("Starting check_company_in_patent_holders function")
		query_template = """
	    SELECT company_id, patent_id, 'model' as patent_type FROM PATENT_MODEL_HOLDER WHERE company_id = ANY($1)
	    UNION ALL
	    SELECT company_id, patent_id, 'design' as patent_type FROM PATENT_DESIGN_HOLDER WHERE company_id = ANY($1)
	    UNION ALL
	    SELECT company_id, patent_id, 'invention' as patent_type FROM PATENT_INVENTION_HOLDER WHERE company_id = ANY($1)
	    """

		records = await conn.fetch(query_template, company_ids)

		result = {company_id: [] for company_id in company_ids}
		for record in records:
			description = await self.fetch_description(conn, record['patent_id'], record['patent_type'])
			result[record['company_id']].append((record['patent_id'], record['patent_type'], description))

		await conn.close()
		logging.info("Completed check_company_in_patent_holders function")
		return result

	async def fetch_holder_entities(self, offset, limit, patent_type="design"):
		"""
	    Fetches organization data by chunks.

	    Parameters:
	    offset (int): Offset for data sampling.
	    limit (int): The limit of the data sample.
	    patent_type (str): Type of patent (default is "design").

	    Returns:
	    list: Records from the database.
	    """
		logging.info("Starting fetch_holder_entities function")
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)

		patent_types = {
			"model": "patent_model_holder",
			"design": "patent_design_holder",
			"invention": "patent_invention_holder",
		}
		query = f"""
	        SELECT company_id, patent_id
	        FROM {patent_types[patent_type]}
	        OFFSET {offset} LIMIT {limit};
	        """

		records = await conn.fetch(query)
		await conn.close()
		logging.info("Completed fetch_holder_entities function")
		return records

	async def fetch_holder_entities_in_chunks(self, chunk_size, patent_type="design"):
		"""
	        Fetches organization data in chunks.

	        Parameters:
	        chunk_size (int): The size of the chunk to sample the data.
	        patent_type (str): Type of patent (default is "design").

	        Returns:
	        generator: A DataFrame generator with data of organizations.
	        """
		logging.info("Starting fetch_holder_entities_in_chunks function")
		offset = 0
		while True:
			records = await self.fetch_holder_entities(offset, chunk_size, patent_type)
			if not records:
				break
			df_chunk = pd.DataFrame(records, columns=["company_id", "patent_id"])
			yield df_chunk
			offset += chunk_size
		logging.info("Completed fetch_holder_entities_in_chunks function")

	async def fetch_holder_entities_in_chunks_by_ids(self, patent_ids, chunk_size, patent_type="design"):
		"""
	        Fetches organization data in chunks.

	        Parameters:
	        chunk_size (int): The size of the chunk to sample the data.
	        patent_type (str): Type of patent (default is "design").

	        Returns:
	        generator: A DataFrame generator with data of organizations.
	    """
		logging.info("Starting fetch_holder_entities_in_chunks_by_ids function")
		offset = 0
		while True:
			records = await self.fetch_holder_entities_by_ids(patent_ids, offset, chunk_size, patent_type)
			if not records:
				break
			yield records
			offset += chunk_size
		logging.info("Completed fetch_holder_entities_in_chunks_by_ids function")

	async def fetch_holder_entities_by_ids(self, patent_ids, offset, limit, patent_type="design"):
		"""
	        Fetches organization data by chunks.

	        Parameters:
	        offset (int): Offset for data sampling.
	        limit (int): The limit of the data sample.
	        patent_type (str): Type of patent (default is "design").

	        Returns:
	        list: Records from the database.
		"""
		logging.info("Starting fetch_holder_entities_by_ids function")
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)

		patent_types = {
			"model": "patent_model_holder",
			"design": "patent_design_holder",
			"invention": "patent_invention_holder",
		}
		query = f"""
	        SELECT company_id
	        FROM {patent_types[patent_type]}
	        WHERE patent_id IN ({', '.join(patent_ids)})
	        OFFSET {offset} LIMIT {limit};
	        """

		records = await conn.fetch(query)
		await conn.close()
		if records is None:
			logging.error("in fetch_holder_entities_by_ids records is None")
			return records

		logging.info("Completed fetch_holder_entities_by_ids function")
		return [record['company_id'] for record in records]

	async def process_company(self, company_ids, batch_size=10000):
		"""
        Processes company data with its classification.

        Parameters:
        company_ids (list): List of company IDs.
        batch_size (int): The batch size for the data to be inserted.

        Returns:
        None
        """
		logging.info("Starting process_company function")
		async for chunk in self.fetch_company_entities_in_chunks(self.chunk_size, company_ids):
			data = self.category_detector(
				chunk, okvd_column_name="okved", new_column_name="classification"
			)
			await self.insert_classification(data, batch_size)
		logging.info("Completed process_company function")

	def run_process(self, company_ids):
		"""
        Starts the data processing.

        Parameters:
        company_ids (list): A list of company IDs.

        Returns:
        None
        """
		logging.info("Starting run_process function")
		loop = asyncio.get_event_loop()
		try:
			loop.run_until_complete(self.process_company(company_ids))
		except Exception as e:
			logging.error(f"Error in run_process: {e}")
		finally:
			loop.close()
		logging.info("Completed run_process function")

	async def insert_classification(self, updates, batch_size):
		"""
        Inserts the classification results into the database.

        Parameters:
        updates (pd.DataFrame): DataFrame with the classification results.
        batch_size (int): The batch size for the data to insert.

        Returns:
        None
        """
		logging.info("Starting insert_classification function")
		conn = await asyncpg.connect(
			user=self.user,
			password=self.password,
			database=self.database,
			host=self.host,
			port=self.port,
		)
		try:
			for i in range(0, len(updates), batch_size):
				batch = updates[i: i + batch_size]
				await self.update_classification(conn, batch)
		except Exception as e:
			logging.error(f"Error in insert_classification: {e}")
		finally:
			await conn.close()
		logging.info("Completed insert_classification function")

	async def update_classification(self, conn, updates):
		"""
	       Updates the classification in the database.

	        Parameters:
	        conn (asyncpg.Connection): Connection to the database.
	        updates (pd.DataFrame): DataFrame with the results of the classification.

	        Returns:
	        None
	        """
		logging.info("Starting update_classification function")
		query = """
	        UPDATE HOLDER_ENTITY
	        SET classification = $1
	        WHERE company_id = $2
	        """
		async with conn.transaction():
			try:
				for index, row in updates.iterrows():
					await conn.execute(query, row["classification"], row["company_id"])
			except Exception as e:
				logging.error(f"Error in update_classification: {e}")
		logging.info("Completed update_classification function")

	async def get_patent_data(self, conn, patent_type, patent_id):
		table_map = {
			'model': 'PATENT_MODEL',
			'invention': 'PATENT_INVENTION',
			'design': 'PATENT_DESIGN'
		}
		table_name = table_map.get(patent_type.lower())
		if table_name:
			query = f"SELECT * FROM {table_name} WHERE registration_number = $1"
			return await conn.fetch(query, patent_id)
		else:
			return []

	async def get_tin_by_id(self, conn, company_id):
		query = "SELECT tin FROM HOLDER_ENTITY WHERE company_id = $1"
		result = await conn.fetch(query, company_id)
		return result[0]['tin'] if result else None


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
		1627747,
		1627748,
		1627749,
		1627750,
		1627751,
		1627752,
		1627753,
		1627754,
		1627755,
		1627756,
		1627757,
		1627758,
		1627759,
		1627760,
		1627761,
		1627762,
		1627764,
		1627765,
		1627766,
		1627767,
		1627768,
		1627769,
		1627771,
		1627772,
		1627773,
		1627774,
		1627775,
		1627776,
		1627777,
		1627778,
		1627779,
		1627780,
		1627781,
	]
	company_ids = [str(i) for i in company_ids]
	dblink = OrgDatabaseLink()
	dblink.run_process(company_ids)

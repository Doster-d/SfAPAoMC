from .OrgCategory import CategoryDetector
import os
import pandas as pd
import asyncpg
import asyncio


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
        self.port = os.getenv("DB_port", 5432)
        self.host = os.getenv("DB_address", "postgres")
        self.user = os.getenv("DB_user", "patentexpertuser")
        self.password = os.getenv("DB_pass", "mycoolpassword123")
        self.database = os.getenv("DB_db", "patentanal")
        self.category_detector = CategoryDetector()

    async def fetch_company_entities(self, company_ids, offset, limit):
        """
        Fetches the data of organizations by their IDs.

        Parameters:
        company_ids (list): List of company IDs.
        offset (int): Offset for data sampling.
        limit (int): The limit of the data sample.

        Returns:
        list: Records from the database.
        """
        conn = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )

        query = f"""
		SELECT company_id, okved, full_name
		FROM HOLDER_ENTITY
		WHERE company_id IN ({', '.join(company_ids)})
		OFFSET {offset} LIMIT {limit};
		"""

        records = await conn.fetch(query)
        await conn.close()
        return records

    async def does_exist_in_holders(self, company_id, patent_type="all"):
        """
        Check if a company exists in the patent holders table.

        Parameters:
        company_id (int): The ID of the company.
        patent_type (str): Type of patent (default is "all").

        Returns:
        bool: True if the company exists, False otherwise.
        """
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
        offset = 0
        while True:
            records = await self.fetch_holder_entities(offset, chunk_size, patent_type)
            if not records:
                break
            df_chunk = pd.DataFrame(records, columns=["company_id", "patent_id"])
            yield df_chunk
            offset += chunk_size

    async def process_company(self, company_ids, batch_size=10000):
        """
        Processes company data with its classification.

        Parameters:
        company_ids (list): List of company IDs.
        batch_size (int): The batch size for the data to be inserted.

        Returns:
        None
        """
        async for chunk in self.fetch_company_entities_in_chunks(5000000, company_ids):
            data = self.category_detector(
                chunk, okvd_column_name="okved", new_column_name="classification"
            )
            await self.insert_classification(data, batch_size)

    def run_process(self, company_ids):
        """
        Starts the data processing.

        Parameters:
        company_ids (list): A list of company IDs.

        Returns:
        None
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.process_company(company_ids))

    async def insert_classification(self, updates, batch_size):
        """
        Inserts the classification results into the database.

        Parameters:
        updates (pd.DataFrame): DataFrame with the classification results.
        batch_size (int): The batch size for the data to insert.

        Returns:
        None
        """
        conn = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )
        for i in range(0, len(updates), batch_size):
            batch = updates[i : i + batch_size]
            await self.update_classification(conn, batch)
        await conn.close()

    async def update_classification(self, conn, updates):
        """
        Updates the classification in the database.

        Parameters:
        conn (asyncpg.Connection): Connection to the database.
        updates (pd.DataFrame): DataFrame with the results of the classification.

        Returns:
        None
        """
        query = """
		UPDATE HOLDER_ENTITY
		SET classification = $1
		WHERE company_id = $2
		"""
        async with conn.transaction():
            for index, row in updates.iterrows():
                await conn.execute(query, row["classification"], row["company_id"])


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

from .PatentProcessor import PatentProcessor
from .PatentLinkage import PatentLinkage
import os
import pandas as pd
import asyncpg
import asyncio


class DatabaseLoader:
    """
    Class for loading patent data and linking it to companies in the database.

    Methods:
    - __init__: Initialize database connection parameters and helper objects.
    - fetch_holder_entities: Fetch company data from the database with offset and limit.
    - fetch_holder_entities_in_chunks: Fetch company data from the database in chunks.
    - insert_patent_model_holder: Insert patent holder data into the database.
    - process_company: Process company data and link it to patents.
    - load_company: Run the process of loading and linking company and patent data.
    - fetch_patent_models: Fetch patent data from the database by patent type.
    - fetch_and_convert_to_df: Convert patent data to a DataFrame.
    - load_patent_model: Load patent data and start its processing.
    """

    def __init__(self):
        """
        Initializes database connection parameters and helper objects.
        """
        self.chunk_size = 5000000
        self.patents_df = pd.DataFrame()
        self.port = os.getenv("DB_port", 6432)
        self.host = os.getenv("DB_address", "127.0.0.1")
        self.user = os.getenv("DB_user", "patentexpertuser")
        self.password = os.getenv("DB_pass", "mycoolpassword123")
        self.database = os.getenv("DB_db", "patentanal")
        self.patent_processor = PatentProcessor()
        self.patent_linker = PatentLinkage()
        self.mtmlinks = {
            "model": """
			INSERT INTO PATENT_MODEL_HOLDER (patent_id, company_id)
			VALUES ($1, $2)
			ON CONFLICT (patent_id, company_id) DO NOTHING;
			""",
            "design": """
			INSERT INTO PATENT_DESIGN_HOLDER (patent_id, company_id)
			VALUES ($1, $2)
			ON CONFLICT (patent_id, company_id) DO NOTHING;
			""",
            "invention": """
			INSERT INTO PATENT_INVENTION_HOLDER (patent_id, company_id)
			VALUES ($1, $2)
			ON CONFLICT (patent_id, company_id) DO NOTHING;
			""",
        }
        self.sql_getters = {
            "model": """
			SELECT registration_number, authors, patent_holders
			FROM PATENT_MODEL;
			""",
            "design": """
			SELECT registration_number, authors, patent_holders
			FROM PATENT_DESIGN;
			""",
            "invention": """
			SELECT registration_number, authors, patent_holders
			FROM PATENT_INVENTION;
			""",
        }
        self.sql_setters = {
            "model": """
			INSERT INTO PATENT_MODEL (registration_number, publish_date, description, authors, patent_holders, is_active)
			VALUES ($1, $2, $3, $4, $5, $6)
			ON CONFLICT (registration_number) DO NOTHING;
			""",
            "design": """
			INSERT INTO PATENT_DESIGN (registration_number, publish_date, description, authors, patent_holders, is_active)
			VALUES ($1, $2, $3, $4, $5, $6)
			ON CONFLICT (registration_number) DO NOTHING
			""",
            "invention": """
			INSERT INTO PATENT_INVENTION (registration_number, publish_date, description, authors, patent_holders, is_active)
			VALUES ($1, $2, $3, $4, $5, $6)
			ON CONFLICT (registration_number) DO NOTHING
			""",
        }

    async def fetch_holder_entities(self, offset: int, limit: int):
        """
        Fetches company data from the database with offset and limit.

        Parameters:
        offset (int): Offset for data selection.
        limit (int): Limit for data selection.

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
		SELECT company_id, full_name
		FROM HOLDER_ENTITY
		ORDER BY company_id
		OFFSET {offset} LIMIT {limit};
		"""
        records = await conn.fetch(query)
        await conn.close()
        return records

    async def fetch_holder_entities_in_chunks(self, chunk_size: int):
        """
        Fetches company data from the database in chunks.

        Parameters:
        chunk_size (int): Size of each chunk for data selection.

        Returns:
        generator: Generator yielding DataFrame with company data.
        """
        offset = 0
        while True:
            records = await self.fetch_holder_entities(offset, chunk_size)
            if not records:
                break
            df_chunk = pd.DataFrame(records, columns=["company_id", "full_name"])
            yield df_chunk
            offset += chunk_size

    async def insert_patent_model(self, conn, df: pd.DataFrame, patent_type: str):
        """
        Inserts patent holder data into the database.

        Parameters:
        conn (asyncpg.Connection): Database connection.
        df (pd.DataFrame): DataFrame with data to insert.
        patent_type (str): Type of patent (model, design, invention).

        Returns:
        None
        """
        query = self.sql_setters[patent_type]
        async with conn.transaction():
            for index, row in df.iterrows():
                if patent_type == "design":
                    description = row["industrial_design_name"]
                elif patent_type == "model":
                    description = row["utility_model_name"]
                else:
                    description = row["invention_name"]
                if pd.isna(description):
                    description = "NULL"
                # (registration_number, publish_date, description, authors, patent_holders, is_active)
                await conn.execute(
                    query,
                    row["registration_number"],
                    row["registration_date"],
                    description,
                    row["authors"],
                    row["patent_holders"],
                    row["actual"],
                )

    async def insert_patents(self, df: pd.DataFrame, patent_type: str):
        conn = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )
        await self.insert_patent_model(conn, df, patent_type)
        await conn.close()

    async def insert_patent_model_holder(
        self, conn, df: pd.DataFrame, patent_type: str
    ):
        """
        Inserts patent holder data into the database.

        Parameters:
        conn (asyncpg.Connection): Database connection.
        df (pd.DataFrame): DataFrame with data to insert.
        patent_type (str): Type of patent (model, design, invention).

        Returns:
        None
        """
        query = self.mtmlinks[patent_type]
        async with conn.transaction():
            for index, row in df.iterrows():
                await conn.execute(query, row["registration_number"], row["company_id"])

    async def process_company(self, patent_type: str):
        """
        Processes company data and links it to patents.

        Parameters:
        patent_type (str): Type of patent (model, design, invention).

        Returns:
        None
        """
        async for chunk in self.fetch_holder_entities_in_chunks(self.chunk_size):
            data = await self.patent_linker.proceed_chunk(chunk)
            conn = await asyncpg.connect(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port,
            )
            await self.insert_patent_model_holder(conn, data, patent_type)
            await conn.close()

    def load_company(self, patent_type="model"):
        """
        Runs the process of loading and linking company and patent data.

        Parameters:
        patent_type (str): Type of patent (model, design, invention).

        Returns:
        None
        """
        self.patent_linker.load_patent_df(self.patents_df)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.process_company(patent_type))

    async def fetch_patent_models(self, patent_type: str):
        """
        Fetches patent data from the database by patent type.

        Parameters:
        patent_type (str): Type of patent (model, design, invention).

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
        query = self.sql_getters[patent_type]
        records = await conn.fetch(query)
        await conn.close()
        return records

    async def fetch_and_convert_to_df(self, patent_type: str) -> pd.DataFrame:
        """
        Converts patent data to a DataFrame.

        Parameters:
        patent_type (str): Type of patent (model, design, invention).

        Returns:
        pd.DataFrame: DataFrame with patent data.
        """
        records = await self.fetch_patent_models(patent_type)
        df = pd.DataFrame(
            records, columns=["registration_number", "authors", "patent_holders"]
        )
        return df

    def load_patent_model(self, patent_type="model"):
        """
        Loads patent data and starts its processing.

        Parameters:
        patent_type (str): Type of patent (model, design, invention).

        Returns:
        None
        """
        loop = asyncio.get_event_loop()
        self.patents_df = loop.run_until_complete(
            self.fetch_and_convert_to_df(patent_type)
        )
        self.patent_processor.load_patents(self.patents_df)
        self.patent_processor.start_process()
        self.patents_df = self.patent_processor.patents_ids


if __name__ == "__main__":
    """
	Main block to start the process of loading patent and company data.

	Example:
	a = DatabaseLoader()
	a.load_patent_model()
	a.load_company()
	"""
    a = DatabaseLoader()
    a.load_patent_model()
    a.load_company()

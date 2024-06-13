from PatentProcessor import PatentProcessor
from PatentLinkage import PatentLinkage
import os
import pandas as pd
import asyncpg
import asyncio


class DatabaseLoader:
	def __init__(self):
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
			'model': """
			INSERT INTO PATENT_MODEL_HOLDER (patent_id, company_id)
			VALUES ($1, $2)
			""",
			'design': """
			INSERT INTO PATENT_DESIGN_HOLDER (patent_id, company_id)
			VALUES ($1, $2)
			""",
			'invention': """
			INSERT INTO PATENT_INVENTION_HOLDER (patent_id, company_id)
			VALUES ($1, $2)
			"""
		}
		self.mtmgetters = {
			'model': """
			SELECT registration_number, authors, patent_holders
			FROM PATENT_MODEL;
			""",
			'design': """
			SELECT registration_number, authors, patent_holders
			FROM PATENT_DESIGN;
			""",
			'invention': """
			SELECT registration_number, authors, patent_holders
			FROM PATENT_INVENTION;
			"""
		}

	async def fetch_holder_entities(self, offset, limit):
		conn = await asyncpg.connect(
			user=self.user, password=self.password,
			database=self.database, host=self.host, port=self.port)
		query = f"""
		SELECT company_id, full_name
		FROM HOLDER_ENTITY
		ORDER BY company_id
		OFFSET {offset} LIMIT {limit};
		"""
		records = await conn.fetch(query)
		await conn.close()
		return records

	async def fetch_holder_entities_in_chunks(self, chunk_size):
		offset = 0
		while True:
			records = await self.fetch_holder_entities(offset, chunk_size)
			if not records:
				break
			df_chunk = pd.DataFrame(records, columns=['company_id', 'full_name'])
			yield df_chunk
			offset += chunk_size

	async def insert_patent_model_holder(self, conn, df, patent_type: str):
		query = self.mtmlinks[patent_type]
		async with conn.transaction():
			for index, row in df.iterrows():
				await conn.execute(query, row['registration_number'], row['company_id'])

	async def process_company(self, patent_type: str):
		async for chunk in self.fetch_holder_entities_in_chunks(5000000):
			# print(chunk)
			data = await self.patent_linker.proceed_chunk(chunk)
			conn = await asyncpg.connect(
				user=self.user, password=self.password,
				database=self.database, host=self.host, port=self.port)
			await self.insert_patent_model_holder(conn, data, patent_type)
			await conn.close()

	def load_company(self, patent_type='model'):
		self.patent_linker.load_patent_df(self.patents_df)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.process_company(patent_type))

	async def fetch_patent_models(self, patent_type: str):
		conn = await asyncpg.connect(
			user=self.user, password=self.password,
			database=self.database, host=self.host, port=self.port)
		query = self.mtmgetters[patent_type]
		records = await conn.fetch(query)
		await conn.close()
		return records

	async def fetch_and_convert_to_df(self, patent_type: str):
		records = await self.fetch_patent_models(patent_type)
		df = pd.DataFrame(records, columns=['registration_number', 'authors', 'patent_holders'])
		return df

	def load_patent_model(self, patent_type='model'):
		loop = asyncio.get_event_loop()
		self.patents_df = loop.run_until_complete(self.fetch_and_convert_to_df(patent_type))
		self.patent_processor.load_patents(self.patents_df)
		self.patent_processor.start_process()
		self.patents_df = self.patent_processor.patents_ids


if __name__ == "__main__":
	a = DatabaseLoader()
	a.load_patent_model()
	a.load_company()
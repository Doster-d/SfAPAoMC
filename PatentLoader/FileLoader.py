from PatentProcessor import PatentProcessor
from PatentLinkage import PatentLinkage
from DatabaseLoader import DatabaseLoader
import os
import pandas as pd
import asyncpg
import asyncio


class FileLoader:
	"""
	Class for loading patent data from a file and processing it to link with company data.

	Methods:
	- __init__: Initializes the FileLoader with instances of DatabaseLoader, PatentProcessor, and PatentLinkage.
	- load_file: Loads and processes a patent file.
	- process_file: Processes the loaded patent file to link with company data.
	- manual_start: Manually starts the process of loading and processing a patent file.
	"""

	def __init__(self):
		"""
		Initializes the FileLoader with instances of DatabaseLoader, PatentProcessor, and PatentLinkage.
		"""
		self.dataBaseLoader = DatabaseLoader()
		self.patent_processor = self.dataBaseLoader.patent_processor
		self.patent_linker = self.dataBaseLoader.patent_linker

	async def load_file(self, file_path: str, patent_type="design"):
		"""
		Loads and processes a patent file.

		Parameters:
		file_path (str): Path to the patent file.
		patent_type (str): Type of the patent (default is "design").
		"""
		self.patent_processor.read_patents(file_path)
		await self.dataBaseLoader.insert_patents(self.patent_processor.current_patents_dataframe, patent_type)
		self.patent_processor.start_process()
		self.dataBaseLoader.patents_df = self.patent_processor.patents_ids
		self.patent_linker.load_patent_df(self.dataBaseLoader.patents_df)

	async def process_file(self, patent_type="design"):
		"""
		Processes the loaded patent file to link with company data.

		Parameters:
		patent_type (str): Type of the patent (default is "design").
		"""
		await self.dataBaseLoader.process_company(patent_type)

	async def manual_start(self, file_path: str, patent_type="design"):
		"""
		Manually starts the process of loading and processing a patent file.

		Parameters:
		file_path (str): Path to the patent file.
		patent_type (str): Type of the patent (default is "design").
		"""
		await self.load_file(file_path, patent_type)
		await self.process_file(patent_type)


if __name__ == "__main__":
	"""
	Main block to start the process of loading patent and company data.

	Example:
	a = FileLoader()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(a.manual_start("../data/DesignsSmall.xlsx"))
	"""
	a = FileLoader()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(a.manual_start("../data/DesignsSmall.xlsx"))

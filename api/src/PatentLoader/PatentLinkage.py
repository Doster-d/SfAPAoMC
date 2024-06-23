from .LinkStrategy.RapidLinkStrategy import RapidLinkStrategy
try:
    import cudf.pandas
except ImportError:
    pass
import pandas as pd
import re
import numpy as np
import math
import asyncpg
import asyncio


def process_row(row):
	try:
		return len(row['patent processed']) != len(row['company_id'])
	except TypeError:
		return True

class PatentLinkage:
	"""
    Class for linking patent data with company data.

    Methods:
    - __init__: Initializes the DataFrame attributes.
    - clean_name: Cleans and normalizes the company name.
    - load_patent_df: Loads the patent DataFrame.
    - proceed_chunk: Processes a chunk of company data and links it to patent data.
    - process_rapid_df_linkage: Links patent data to company data using rapid fuzzy matching.
    - extract_tin: Extracts TIN and PSRN and merges them with the patent DataFrame.
    """

	allow_rapid_linkage = True

	def __init__(self):
		"""
        Initializes the DataFrame attributes.
        """
		self.patent_df = pd.DataFrame()
		self.linkage_df = pd.DataFrame()
		self.final_df = pd.DataFrame()

	def clean_name(self, name: str) -> str:
		"""
        Cleans and normalizes the company name.

        Parameters:
        name (str): The name of the company.

        Returns:
        str: The cleaned and normalized company name.
        """
		name = name.replace(" ", "")
		name = re.sub(r'[«»"]+', "", name)
		name = re.sub(r"\([^)]*\)", "", name)
		return name

	def load_patent_df(self, patent_df: pd.DataFrame):
		"""
        Loads the patent DataFrame.

        Parameters:
        patent_df (pd.DataFrame): DataFrame containing patent data.
        """
		self.patent_df = patent_df

	def load_linkage_df(self, linkage_df: pd.DataFrame):
		"""
		Loads the patent DataFrame.

		Parameters:
		linkage_df (pd.DataFrame): DataFrame containing full patent data.
		"""
		self.final_df = linkage_df

	async def process_rapid_df_linkage(
			self, df: pd.DataFrame, chunk_df: pd.DataFrame
	) -> pd.DataFrame:
		"""
        Links patent data to company data using rapid fuzzy matching.

        Parameters:
        df (pd.DataFrame): DataFrame with patent data.
        chunk_df (pd.DataFrame): DataFrame containing a chunk of company data.

        Returns:
        pd.DataFrame: DataFrame with linked company and patent data.
        """
		cleared = chunk_df[
			~chunk_df["company_id"].isin(
				df[df["company_id"].notna()]["company_id"].to_list()
			)
		]
		return df.apply(RapidLinkStrategy.process_row, axis=1, args=(cleared,))

	async def proceed_chunk(self, chunk_df: pd.DataFrame) -> pd.DataFrame:
		"""
        Processes a chunk of company data and links it to patent data.

        Parameters:
        chunk_df (pd.DataFrame): DataFrame containing a chunk of company data.

        Returns:
        pd.DataFrame: DataFrame with linked company and patent data.
        """
		company_df = chunk_df
		company_df["full_name"] = company_df["full_name"].str.lower()
		company_df = company_df.dropna(subset=["full_name", "company_id"])
		company_df["full_name"] = company_df["full_name"].apply(self.clean_name)
		self.patent_df["is foreign"].fillna(True, inplace=True)
		df = self.patent_df[self.patent_df["is foreign"] == False].merge(
			company_df, left_on="patent processed", right_on="full_name", how="left"
		)
		if self.allow_rapid_linkage:
			df = await self.process_rapid_df_linkage(df, chunk_df)
		del df["full_name"]
		df = df.dropna(subset=["company_id", "registration_number"])
		self.extract_tin(df)
		return df

	def extract_tin(self, df: pd.DataFrame):
		"""
		Extracts TIN and PSRN and merges them with the patent DataFrame.

		Parameters:
		df (pd.DataFrame): DataFrame with linked company and patent data.
		"""
		final_df = df.groupby('registration_number')['company_id'].apply(list).reset_index()
		final_df["tin"] = df.groupby('registration_number')["tin"].apply(list).reset_index()["tin"]
		final_df["psrn"] = df.groupby('registration_number')["psrn"].apply(list).reset_index()["psrn"]
		final_df = self.final_df.merge(final_df, on='registration_number', how='left')
		if 'company_id' not in final_df.columns.to_list():
			return
		final_df["is_multiple_choice"] = final_df.apply(
			process_row, axis=1
		)
		self.final_df = final_df

	def export_final_dataframe_to_excel(self, filepath):
		self.final_df.to_excel(filepath)

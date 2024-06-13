from PatentLoader import PatentProcessor
import pandas as pd
import re
import asyncpg
import asyncio


class PatentLinkage:
	def __init__(self):
		self.patent_df = pd.DataFrame()
		self.linkage_df = pd.DataFrame()
		self.final_df = pd.DataFrame()

	def clean_name(self, name):
		name = name.replace(" ", "")
		name = re.sub(r'[«»"]+', "", name)
		name = re.sub(r'\([^)]*\)', '', name)
		return name

	def load_patent_df(self, patent_df):
		self.patent_df = patent_df

	async def proceed_chunk(self, chunk_df):
		company_df = chunk_df
		company_df['full_name'] = company_df['full_name'].str.lower()
		company_df = company_df.dropna(subset=['full_name', 'company_id'])
		company_df['full_name'] = company_df['full_name'].apply(self.clean_name)
		self.patent_df['is foreign'].fillna(True, inplace=True)
		df = self.patent_df[self.patent_df['is foreign'] == False].merge(
			company_df,
			left_on='patent processed',
			right_on='full_name',
			how='left'
		)
		del df['full_name']
		df = df.dropna(subset=['company_id', 'registration_number'])
		return df

	# self.linkage_df = df

	def extract_tin(self, df):
		final_df = df.groupby('registration_number')['company_id'].apply(list).reset_index()
		final_df["tin"] = df.groupby('registration_number')["tin"].apply(list).reset_index()["tin"]
		final_df["psrn"] = df.groupby('registration_number')["psrn"].apply(list).reset_index()["psrn"]
		final_df = self.patent_df.merge(final_df, on='registration_number', how='left')
		final_df["is_multiple_choice"] = final_df.apply(
			lambda row: len(row['patent_holders']) != len(row['company_id']), axis=1
		)
		self.final_df = final_df

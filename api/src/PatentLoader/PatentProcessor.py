try:
    import cudf.pandas
except ImportError:
    pass
import pandas as pd
import numpy as np
from datetime import datetime
import re
from .ParseStrategies.StandardParseStrategy import StandardParseStrategy
import re


def has_numbers(inputString):
    return bool(re.search(r"\d", inputString))


class PatentProcessor:
    """
    Class for processing patent data, including reading, cleaning, and transforming patent records.

    Methods:
    - __init__: Initializes the DataFrame attributes and defines the columns and data types.
    - read_patents: Reads patent data from an Excel file.
    - load_patents: Loads patent data from a DataFrame.
    - process_design: Processes each row of the DataFrame to clean and normalize patent data.
    - start_process: Starts the processing of the patent DataFrame.
    """

    def __init__(self):
        """
        Initializes the DataFrame attributes and defines the columns and data types.
        """
        self.patent_type = "design"
        self.patents_ids = pd.DataFrame()
        self.current_patents_dataframe = pd.DataFrame()
        self.current_ids_dataframe = pd.DataFrame()
        self.current_columns = [
            "registration_number",
            "registration_date",
            "authors",
            "patent_holders",
            "actual",
            "industrial_design_name",
        ]
        self.current_dtype = {
            "registration number": int,
        }

    def read_patents(self, read_object, use_cols=None):
        """
        Reads patent data from an Excel file.

        Parameters:
        read_object: Object representing the Excel file (e.g., file path or file-like object).
        """
        if use_cols is None:
            use_cols = self.current_columns
        self.current_patents_dataframe = pd.read_excel(
            read_object, dtype=self.current_dtype
        )
        columns = self.current_patents_dataframe.columns.to_list()
        if "industrial_design_name" in columns:
            self.patent_type = "design"
        elif "utility_model_name" in columns:
            self.patent_type = "model"
        else:
            self.patent_type = "invention"

		# self.current_patents_dataframe = self.current_patents_dataframe[use_cols]
        date_format = "%Y-%m-%d"
        unix_start_time = datetime.strptime('1970-01-01', date_format)
        self.current_patents_dataframe.dropna(subset={'registration_number'})
        self.current_patents_dataframe['patent_holders'].fillna("NULL (CN)", inplace=True)
        self.current_patents_dataframe['authors'].fillna("NULL (CN)", inplace=True)
        self.current_patents_dataframe['registration_date'] = self.current_patents_dataframe['registration_date'].apply(
			lambda date: datetime.strptime(date, date_format) if pd.notna(date) and has_numbers(date) else unix_start_time
        )
        self.current_patents_dataframe['actual'] = self.current_patents_dataframe['actual'].apply(
			lambda state: state if pd.notna(state) else False
        )

    def load_patents(self, patents_df: pd.DataFrame):
        """
        Loads patent data from a DataFrame.

        Parameters:
        patents_df (pd.DataFrame): DataFrame containing patent data.
        """
        self.current_patents_dataframe = patents_df

    def process_design(self, row: pd.Series) -> pd.Series:
        """
        Processes each row of the DataFrame to clean and normalize patent data.

        Parameters:
        row (pd.Series): Row of data.

        Returns:
        pd.Series: Processed row of data.
        """
        if pd.isna(row["patent_holders"]):
            return row
        row["patent processed"] = StandardParseStrategy.lower_text(row["patent processed"])
        row["patent processed"] = StandardParseStrategy.process_patent_holder(
            row["patent processed"]
        )
        row["patent processed"] = StandardParseStrategy.split_holders(row["patent processed"])
        row["is foreign"] = StandardParseStrategy.find_foreign(row)
        row["patent processed"] = StandardParseStrategy.remove_parentheses(row["patent processed"])
        row["patent processed"] = StandardParseStrategy.remove_spaces(row["patent processed"])

        return row

    def start_process(self):
        """
        Starts the processing of the patent DataFrame, cleaning and normalizing the data.
        """
        self.current_patents_dataframe["patent processed"] = (
            self.current_patents_dataframe["patent_holders"]
        )
        self.current_patents_dataframe["is foreign"] = np.nan

        self.current_patents_dataframe = self.current_patents_dataframe.apply(
            self.process_design, axis=1
        )
        self.current_patents_dataframe.dropna(
            subset={"registration_number", "patent processed"}
        )
        self.patents_ids = self.current_patents_dataframe[
            ["registration_number", "patent processed", "is foreign"]
        ]
        self.patents_ids = self.patents_ids.explode(["patent processed", "is foreign"])

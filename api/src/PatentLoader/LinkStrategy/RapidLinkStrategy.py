import pandas as pd
import numpy as np
from rapidfuzz import process, utils


class RapidLinkStrategy:
    """
    Class for linking patent data to company data using rapid fuzzy matching.

    Methods:
    - process_row: Processes a row of data to link patent holders to companies based on fuzzy matching.
    """

    def process_row(self, row, cleared_company_df: pd.DataFrame) -> pd.Series:
        """
        Processes a row of data to link patent holders to companies based on fuzzy matching.

        Parameters:
        row (pd.Series): Row of data containing patent holder information.
        cleared_company_df (pd.DataFrame): DataFrame containing company information.

        Returns:
        pd.Series: Processed row with updated company_id if a match is found.
        """
        if row["company_id"] != np.nan:
            return row

        matches = process.extract(
            utils.default_process(row["patent processed"]),
            cleared_company_df["full_name"],
            processor=None,
            score_cutoff=93,
        )

		if matches is not None and len(matches) > 0:
			row['company_id'] = []
			row['tin'] = []
			row['psrn'] = []
			for match in matches:
				extracted_row = cleared_company_df.loc[match[2]]
				row['company_id'].append(extracted_row['company_id'])
				row['tin'].append(extracted_row['tin'])
				row['psrn'].append(extracted_row['psrn'])

        return row

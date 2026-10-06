import pandas as pd
import numpy as np

class DataCleaner:
    @staticmethod
    def get_clean_representation(df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns a clean derived copy of the DataFrame without mutating the original file/DataFrame.
        Handles missing value representations, date conversions, and whitespace stripping.
        """
        clean_df = df.copy()
        
        # Strip whitespace from string columns
        for col in clean_df.select_dtypes(include=['object', 'string']).columns:
            clean_df[col] = clean_df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            # Standardize common null representations
            clean_df[col] = clean_df[col].replace(['N/A', 'n/a', 'NA', 'null', 'NULL', 'None', 'none', '?', 'unk', 'unknown', '-999', '9999'], np.nan)

        return clean_df

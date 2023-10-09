# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 09:08:09 2023

@author: jackl
"""

import pandas as pd
def repairRepeatedMidnightStamps(df_counts):
    """
    Repairs rows in a DataFrame with repeated midnight timestamps.
    
    Logic:
    1. For each location and date, identify groups of rows with the same midnight timestamp.
    2. Rank the entries within each group based on the 'ID' column.
    3. Use the rank to offset the hours from midnight for these entries.
    4. Only modify rows within groups that have multiple midnight timestamps.
    
    Assumptions:
    - The 'ID' column values are strictly increasing with time.
    - Each group with multiple midnight timestamps represents hourly data for that day.
    
    Parameters:
    - df_counts (pd.DataFrame): DataFrame with 'LocationName', 'DateTime', and 'ID' columns.
    
    Returns:
    - pd.DataFrame: DataFrame with corrected timestamps.
    """
    
    # Filter for rows with DateTime at midnight
    midnight_rows = df_counts[df_counts['DateTime'].dt.hour == 0]
    
    # For each group of midnight rows, check if there are multiple rows, and if so, adjust the timestamps
    for (loc_name, date), group in midnight_rows.groupby(['LocationName', df_counts['DateTime'].dt.date]):
        if len(group) == 24:
            sorted_ids = group.sort_values('ID')['ID']
            hour_offsets = pd.to_timedelta(sorted_ids.rank(method='first').astype(int) - 1, unit='h')
            df_counts.loc[sorted_ids.index, 'DateTime'] = group['DateTime'] + hour_offsets
            
    return df_counts

def imputeMissing(df_counts):
    print("Todo: Imputation")
    return repairRepeatedMidnightStamps(df_counts)
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:12:57 2023

@author: jackl
"""

# Some common dataFrame manipulations I use across experiments.

import pandas as pd


def countsLongToWideHourly(df_counts):
    df1 = df_counts[['LocationName','HourlyCount','DateTime']]
    df1 = df1.pivot(index='DateTime',columns='LocationName',values='HourlyCount')
    df1 = df1.asfreq('h')
    return df1

if __name__ == "__main__":
    from PedestrianDataImporter import getHourlyCounts
    from Imputation import repairRepeatedMidnightStamps
    import datetime
    
    df_counts,df_locations = getHourlyCounts['Melbourne']()
    df_counts = repairRepeatedMidnightStamps(df_counts)
    df_wide = countsLongToWideHourly(df_counts)



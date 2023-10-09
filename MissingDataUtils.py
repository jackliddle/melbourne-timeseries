# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 11:22:19 2023

@author: jackl
"""

import itertools
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator

from DataFrameManipulations import countsLongToWideHourly
from Imputation import repairRepeatedMidnightStamps

# def countGaps(df,test=np.isnan):
#     groupings = [(len(list(group)),test_passed) 
#                  for test_passed,group in itertools.groupby(df,test)]
#     if groupings[0][1]:
#         # If the first entry is a gap, ignore it.
#         # It is only missing in the sense that another location has that data and this one doesn't
#         groupings = groupings[1:]
#     return [l for l,t in groupings if t]
# %%

def findMissingness(df_wide,loc):
    df = df_wide[loc]
    missing = []
    # Walk over the series and find all the sections which are NaN and which are not
    for k, l in itertools.groupby( df.items(), key=lambda row: ~np.isnan( row[1] )): 
            ts = [i[0] for i in l]
            missing.append((k,min(ts),max(ts)))
    return missing
# %%

def plotMissing(gaps_d,ax):
    for i, (place, data) in enumerate(gaps_d.items()):
        y_pos = i * 2  # Increment by 2 for each place to leave space between bars

        for present, start_time, end_time in data:
            #start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            #end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

            if present:
                ax.barh(y_pos, end_time - start_time, left=start_time, height=1, color='green')
            else:
                ax.barh(y_pos, end_time - start_time, left=start_time, height=1, color='red')
    
    date_format = DateFormatter('%Y-%m')  # Define the date format
    month_locator = MonthLocator(interval=12) 
    ax.xaxis.set_major_formatter(date_format)  # Set the date format
    ax.xaxis.set_major_locator(month_locator)  # Set the tick locator to show ticks on the 1st day of January and every 3 months

    ax.set_yticks([i for i in range(0, len(gaps_d) * 2, 2)])
    ax.set_yticklabels(gaps_d.keys())
    ax.set_xlabel('Time')

    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels

    ax.xaxis.grid(True)  # Add vertical grid lines

# %%    
if __name__ == "__main__":
    from PedestrianDataImporter import getHourlyCounts
    import matplotlib.pyplot as plt
    import tqdm 
    df_counts,df_locations = getHourlyCounts['Melbourne']()
    df_counts = repairRepeatedMidnightStamps(df_counts)
    df_wide = countsLongToWideHourly(df_counts)
    # %%
    
    locations = df_counts['LocationName'].unique()
    gaps_d = {location:findMissingness(df_wide,location) for location in tqdm.tqdm(locations)}
    # %%
    
    fig, ax = plt.subplots(figsize=(4,16))
    plotMissing(gaps_d,ax)
    


# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:01:37 2023

@author: jackl
"""

import shutil
import tempfile
import urllib
import zipfile#.request
import pathlib

import pandas as pd

from tqdm import tqdm

from cacheDecorator import cacheDecorator
from DateTimeHelpers import parse_date

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# %% The goal here is to have a common interface/dataframe 

# TODO:
# Understand the InCount/OutCount for the York data
# Understand the InCount/OutCount for the Dublin data
# Understand the InCount/OutCount for the Leeds data
# %%
def csvUrlToDF(url,zipped=False):
    with urllib.request.urlopen(url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
        if zipped:
            tempdir = tempfile.TemporaryDirectory()
            zipfile.ZipFile(tmp_file.name).extractall(path=tempdir.name)
            csvs = [csv for csv in pathlib.Path(tempdir.name).glob('*.csv')]
            df = pd.read_csv(csvs[0])
        else:                       
            df = pd.read_csv(tmp_file.name)
    return df

# %%

@cacheDecorator('Dublin')
def getDublinCounts():
    url_root = 'https://data.smartdublin.ie/dataset/cc421859-1f4f-43f6-b349-f4ca0e1c60fa/resource/'
    csv_urls = [
            '2c07d9bd-81ca-42df-b229-8742c2152540/download/dcc-2016-pedestrian-footfall.csv',
            '14667740-246c-42f7-869b-c7097e30645c/download/dcc-2017-pedestrian-footfall.csv',
            '8fbad5e5-d7cc-4f94-b3ed-c6894d52ff45/download/dcc-2018-pedestrian-footfall.csv',
            '0e1ac985-3a45-4134-a696-32909a0310aa/download/dcc-2019-pedestrian-footfall-count-jan-dec_14082020.csv',
            '3048794e-16bd-4edb-9ba9-8018a6aadcdb/download/jan-dec-2020-ped-data.csv',
            'ef530dde-1511-4617-b783-c4a3ad1cd7dc/download/2021-jan-dec-dcc-footfall.csv',
            '2beeedcc-7fe6-4ae2-b8c7-ee8179686595/download/pedestrian-counts-2022.csv',
            '0d0f0de2-d82d-404e-8da2-d238de985532/download/pedestrian-counts-1-jan-3-july-2023.csv',
                ]
    loc_url = '215d83bd-003d-4c1a-ac0d-b1132661746c/download/dublin-city-centre-footfall-counter-locations-18072023.csv'

    df_counts    = [csvUrlToDF(url_root+url) for url in tqdm(csv_urls)]
    df_locations = csvUrlToDF(url_root+loc_url)
    df_locations.rename(columns={
                '_id':'Location_ID',
                'Counter Locations':'Location_Desc',
             }
            ,inplace=True)

    # The count data has two problems:
    # * The DateTime is inconsistently labelled
    # * Each location has its own column, I want each row to be a unique time.
    # This is simple to fix
    possible_names = ['Date and Time','Time','Date & Time']
    def relabelAndReorder(df):
        called = set(df.columns).intersection(possible_names)
        called = list(called)[0]
        dd = pd.melt(df,id_vars = called)
        dd.rename(columns={
                            called:'DateTime',
                            'variable':'LocationName',
                            'value':'HourlyCount',
                           },
                        inplace=True)
        return dd
    df_counts = pd.concat( [relabelAndReorder(df) for df in df_counts] )
    df_counts = df_counts.loc[~df_counts['HourlyCount'].isna()]
    
    #
    date_formats = ["%d-%m-%Y %H:%M:%S","%d/%m/%Y %H:%M"]
    df_counts['DateTime'] = df_counts['DateTime'].apply(lambda s: parse_date(s,date_formats))

    return df_counts, df_locations
# %%

@cacheDecorator('Melbourne')
def getMelbourneCounts():
    location_url   = 'https://melbournetestbed.opendatasoft.com/api/explore/v2.1/catalog/datasets/pedestrian-counting-system-sensor-locations/exports/csv?lang=en&timezone=Europe%2FLondon&use_labels=true&delimiter=%2C'
    df_locations = csvUrlToDF(location_url)
    df_locations.rename(columns={
                        'Sensor_Description':'Location_Desc',
                     },
            inplace=True
            )



    sensordata_url = 'https://melbournetestbed.opendatasoft.com/api/datasets/1.0/pedestrian-counting-system-monthly-counts-per-hour/attachments/pedestrian_counting_system_monthly_counts_per_hour_may_2009_to_14_dec_2022_csv_zip/'
    df_counts = csvUrlToDF(sensordata_url,zipped=True)
    
    df_counts['DateTime'] = pd.to_datetime(df_counts['Date_Time'])
    
    drop_cols = ['Time','Year', 'Mdate','Month', 'Mdate', 'Day','Date_Time']
    df_counts.drop(drop_cols,axis='columns',inplace=True)   
    df_counts.rename(columns={
                'Hourly_Counts':'HourlyCount',
                'Sensor_ID':'Location_ID',
                'Sensor_Name':'LocationName',
             }
            ,inplace=True)
    #
    return df_counts,df_locations

# %%
@cacheDecorator('Leeds')
def getLeedsCounts():
    # Taken from the map at https://datamillnorth.org/dataset/leeds-city-centre-footfall-data
    df_locations = pd.DataFrame([[1,"Briggate",53.79672,-1.54249],
                                 [2,"Briggate at McDonald's",53.79880,-1.54187],
                                 [3,"Headrow",53.79930,-1.54404],
                                 [4,"Dortmund Square",53.79952,-1.54401],
                                 [5,"Albion Street North",53.79742,-1.54508],
                                 [6,"Albion Street South",53.79726,-1.54507],
                                 [7,"Commercial Street at Lush",53.79733,-1.54389],
                                 [8,"Commercial Street at Barretts",53.79732,-1.54370]],
                                 columns=["Location_ID","Location_Desc","Latitude","Longitude"])
    df_counts = "TBD"
    return df_counts,df_locations
# %%

@cacheDecorator('York')
def getYorkCounts():
    location_url = "http://data.cyc.opendata.arcgis.com/datasets/a5c99f66807345df94517a9470d8cb7e_17.csv"
    csv_url='https://data.yorkopendata.org/dataset/6449d8f5-76e7-4aff-bfb1-46d46542a56c/resource/b36a8dfc-49e1-4ce0-99d3-baefb5c8bdfd/download/footfallhourly.csv'
    
    df_locations = csvUrlToDF(location_url)
    df_locations.rename(columns={
                            'X':'Longitude',
                            'Y':'Latitude',
                            'CAMERA_LOC':'Location_Desc',
                            'OBJECTID':'Location_ID',
                                },
                        inplace=True
                        )
    df_counts = csvUrlToDF(csv_url)
    
    # %% A little data cleaning

    df_counts['DateTime'] = pd.to_datetime(df_counts['Date'])

    drop_cols = ['Id','SiteName','LocationGroup',
                 'WeekDay','BRCYear','BRCQuarter','BRCMonth','BRCWeek',
                 'BusinessInCount', 'BusinessOutCount', 'BusinessTotalCount',
                 'FactoredInCount', 'FactoredOutCount', 'FactoredTotalCount',
                 'Date', #Also drop the Date now we have converted it
                 ]
    
    df_counts.drop(drop_cols,axis='columns',inplace=True)   
    df_counts = df_counts.drop_duplicates()
    
    df_counts.rename(columns={
                'TotalCount':'HourlyCount',
             }
            ,inplace=True)
    # %%
    return df_counts,df_locations
# %%    

getHourlyCounts={}
getHourlyCounts['Dublin'] = getDublinCounts
getHourlyCounts['Melbourne'] = getMelbourneCounts
getHourlyCounts['Leeds'] = getLeedsCounts
getHourlyCounts['York']  = getYorkCounts
# %%

if __name__ == "__main__":
    df_counts_must = ['LocationName','HourlyCount','DateTime']

    locations = ['Melbourne','York']
    #locations += ['Dublin'] # Fails due to 
    #locations += ['Leeds']  # Fails due to not being finished.
    for location in locations:
        df_counts,df_locations = getHourlyCounts[location]()
        print(location)
        print(df_counts.columns)
        
        for must in df_counts_must:
            assert must in df_counts.columns,f"{must} be in df_counts for location {location}"
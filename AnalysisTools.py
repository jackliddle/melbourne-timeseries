# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:24:42 2023

@author: jackl
"""

from sktime.utils.plotting import plot_series
import numpy as np
import pandas as pd

# Plot an example of the CV 
# i: the fold to plot,
# ax: axis to plot to.
# tail: how much of the training series to plot.
def plotCVSeries(evals,i,ax,tail=50):
    plot_series(evals['y_train'].iloc[i].tail(tail),
                evals['y_test'].iloc[i],
                evals['y_pred'].iloc[i],
                labels=['Train','Test','Pred'],
                ax = ax,
                markers=['.','.','.'])
# %%

def fastSMAPEelements(yt,yp):
    np.seterr(divide='ignore', invalid='ignore') #Shut up about divide by zero when both yp and yt are both zero
    elements =  2*np.abs(yp-yt)/(np.abs(yp)+np.abs(yt))
    return elements.cumsum()/np.arange(1,len(elements)+1)
    np.seterr(divide='warn', invalid='warn')
    
def ScoreFold(e):
     # Take a fold from the cross-validation and calculate the error on all possible horizons.
     y_pred,y_test = e[['y_pred','y_test']]
     horizons = range(1,len(y_pred)+1)
     s = fastSMAPEelements(y_test.values,y_pred.values)
     return pd.DataFrame(np.array([s,horizons]).T,columns=['Score','Horizon'])

def ScoreForecaster(e):
    # Take a set of folds and calculate the fold scores.
    dd = [ScoreFold(row) for _,row in e.iterrows()]
    for f,d in enumerate(dd):
        d['fold'] = f
    dd = pd.concat(dd)
    dd.reset_index(drop=True,inplace=True)
    return dd

def getScoreTable(evals):
    df_all = []
    for forecaster_name in evals.keys():
        for location_name in evals[forecaster_name].keys():
            dd = ScoreForecaster(evals[forecaster_name][location_name])
            dd['Location']   = location_name
            dd['Forecaster'] = forecaster_name
            df_all.append(dd)
    df_scores = pd.concat(df_all)
    df_scores.loc[df_scores['Score'].isna(),'Score'] = 0
    return df_scores

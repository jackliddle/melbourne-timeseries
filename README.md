# Melbourne Time Series

Here I am gathering my work on the Melbourne Pedestrian footfall time-series.

1. [Data Exploration](https://github.com/jackliddle/melbourne-timeseries/blob/main/01%20Data%20exploration.ipynb)
   Initial exploration of the Melbourne dataset, locations of sensors, missing data.

2. Distributions and Hypothesis testing.
   * 2a [Distributions and Hypothesis testing](https://github.com/jackliddle/melbourne-timeseries/blob/main/02a%20Distributions%20and%20Hypothesis%20Testing.ipynb)
  What distributions should the pedestrian counts follow?
   * 2b [Poisson distributions, Negative Binomial and Normal Distribution](https://github.com/jackliddle/melbourne-timeseries/blob/main/02b%20Poisson%20distributions%2C%20Negative%20Binomial%20and%20Normal%20Distributions..ipynb) Explanation of why we expect the Poisson distribution to tend to a normal distribution when the counts are large. Why might we actually be deviating from the Poisson distribution and seeing a negative binomial distribution.

3. PCA Analysis.
   * 3a [PCA Analysis](https://github.com/jackliddle/melbourne-timeseries/blob/main/03a%20PCA%20Analysis.ipynb) Can apply PCA to reduce a days/weeks worth of data down to a smaller set of numbers? What can we learn about the usage of the space? It turns out we can learn quite a lot.
   * 3b [PCA Outline](https://github.com/jackliddle/melbourne-timeseries/blob/main/03b%20PCA%20Outline.ipynb) Short outline of what PCA does for those unfamiliar.
   * 3c [PCA Analysis - As a time-series](https://github.com/jackliddle/melbourne-timeseries/blob/main/03c%20PCA%20Analysis%20-%20As%20a%20timeseries.ipynb). Looking at the first components of the PCA can we use this to visualise changes over time? Particularly after COVID?
4. [Clustering](https://github.com/jackliddle/melbourne-timeseries/blob/main/04%20Clustering%20Analysis.ipynb) It would be great to be able to cluster these locations together. Do we have true labels for the sites? Sort of, we have the location names and with a little work we can use these to grade the quality of our clustering analysis.

5. Forecasting
   * 5a [Forecasting Introduction](https://github.com/jackliddle/melbourne-timeseries/blob/main/05a%20Forecasting%20Introduction.ipynb) Introduction to some of the key concepts of building forecasting models.
   * 5b [Forecasting](https://github.com/jackliddle/melbourne-timeseries/blob/main/05b%20Forecasting.ipynb) Starting to build forecasting models and setting a baseline.

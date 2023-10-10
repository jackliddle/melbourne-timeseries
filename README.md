# Melbourne Time Series

Here I am gathering my work on the Melbourne Pedestrian footfall time-series.

1. [Data Exploration](https://github.com/jackliddle/melbourne-timeseries/blob/main/01%20Data%20exploration.ipynb)
   Initial exploration of the Melbourne dataset, locations of sensors, missing data.

2. Distributions and Hypothesis testing.
   * 2a [Distributions and Hypothesis testing](https://github.com/jackliddle/melbourne-timeseries/blob/main/02a%20Distributions%20and%20Hypothesis%20Testing.ipynb)
  What distributions should the pedestrian counts follow?
   * 2b [Poisson distributions, Negative Binomial and Normal Distribution](https://github.com/jackliddle/melbourne-timeseries/blob/main/02b%20Poisson%20distributions%2C%20Negative%20Binomial%20and%20Normal%20Distributions..ipynb) Explanation of why we expect the Poisson distribution to tend to a normal distribution when the counts are large. Why might we actually be deviating from the Poisson distribution and seeing a negative binomial distribution.

3. PCA Analysis.
   * 2a [PCA Analysis](https://github.com/jackliddle/melbourne-timeseries/blob/main/03a%20PCA%20Analysis.ipynb) Can apply PCA to reduce a days/weeks worth of data down to a smaller set of numbers? What can we learn about the usage of the space? It turns out we can learn quite a lot.
   * 2b [PCA Outline](https://github.com/jackliddle/melbourne-timeseries/blob/main/03b%20PCA%20Outline.ipynb) Short outline of what PCA does for those unfamiliar.
   
4. [Clustering](https://github.com/jackliddle/melbourne-timeseries/blob/main/04%20Clustering%20Analysis.ipynb) It would be great to be able to cluster these locations together. Do we have true labels for the sites? Sort of, we have the location names and with a little work we can use these to grade the quality of our clustering analysis.

5. Forecasting
   * 5a [Forecasting](https://github.com/jackliddle/melbourne-timeseries/blob/main/05a%20Forecasting.ipynb) Starting to build forecasting models and setting a baseline.

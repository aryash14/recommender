import pandas as pd

metadata = pd.read_csv('../datasets/movies_metadata.csv', low_memory=False)
 #creating the weighted rating formula
'''
WeightedRating(WR)=((v/(v+m))⋅R)+((m/(v+m))⋅C)
v is the number of votes for the movie;
m is the minimum votes required to be listed in the chart;
R is the average rating of the movie;
C is the mean vote across the whole report.
'''
C = metadata['vote_average'].mean()
m = metadata['vote_count'].quantile(0.90)
filtered_dataset = metadata.copy()

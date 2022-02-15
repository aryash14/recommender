from dataclasses import dataclass
import pandas as pd

def weighted_rating(filtered_dataset, m, C):
    v = filtered_dataset['vote_count']
    R = filtered_dataset['vote_average']
    weighted_score = (v/(v+m)*R) + (m/(v+m)*C)
    return weighted_score

if __name__ == '__main__':
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
    filtered_dataset = metadata.copy().loc[metadata['vote_count'] >= m]
    # weighted_score = 
    # print(weighted_score)
    # print(filtered_dataset.head(3))
    filtered_dataset['score'] = filtered_dataset.apply(weighted_rating, axis = 1, args=(m, C))
    # print(filtered_dataset.shape)
    # print(metadata.shape)
    #Sort movies based on score calculated above
    filtered_dataset = filtered_dataset.sort_values('score', ascending=False)

    # #Print the top 15 movies
    # print(filtered_dataset[['title', 'vote_count', 'vote_average', 'score']].head(20))


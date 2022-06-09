import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
'''
We will extract feature with TfIdfVectorizer.

'''

def get_recommendation(title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores.sort(key=lambda x:x[1], reverse = True)   
    sim_scores = sim_scores[1:11]
    movies = [metadata['title'][i[0]] for i in sim_scores]
    return movies

def get_director(crew):
    for people in crew:
        if people['job'] == 'Director':
            return people['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        list_items = [item['name'] for item in x]
        if len(list_items) > 3:
            list_items = list_items[:3]
        return list_items

    return []

def distinct_data(x):
    if (isinstance(x, list)):
        return [item.replace(" ", "").lower() for item in x]
    elif (isinstance(x, str)):
        return x.replace(" ", "").lower()
    else:
        return ''
        
def create_soup(data):
     return ' '.join(data['keywords']) + ' ' + ' '.join(data['cast']) + ' ' + data['director'] + ' ' + ' '.join(data['genres'])

if __name__ == '__main__':
    metadata = pd.read_csv('../datasets/movies_metadata.csv', low_memory=False)
    credits = pd.read_csv('../datasets/credits.csv')
    keywords = pd.read_csv('../datasets/keywords.csv')
    #converting the ids into ints in order to merge them later
    metadata = metadata.drop([19730, 29503, 35587])
    credits['id'] = credits['id'].astype('int32')
    keywords['id'] = keywords['id'].astype('int32')
    metadata['id'] = metadata['id'].astype('int32')
    #adding the columns based on ids for credits which containes cast and crew
    metadata = metadata.merge(credits, on='id')
    #adding the columns based on ids for keywords which containes keywords
    metadata = metadata.merge(keywords, on='id')
    #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')

    metadata['overview'] = metadata['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(metadata['overview'])
    #making the obj type usable
    features = ['cast', 'crew', 'keywords', 'genres']
    for feature in features:
        metadata[feature] = metadata[feature].apply(literal_eval)
    #making a director column
    metadata['director'] = metadata['crew'].apply(get_director)
    features = ['cast', 'keywords', 'genres']
    for feature in features:
        metadata[feature] = metadata[feature].apply(get_list)
    #removing the space and making everything lower case
    features = ['cast', 'keywords', 'genres', 'director']
    for feature in features:
        metadata[feature] = metadata[feature].apply(distinct_data)
    #apply the function to the rows
    metadata['soup'] = metadata.apply(create_soup, axis=1)
    
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(metadata['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    indices = pd.Series(metadata.index, index=metadata['title'])
    metadata = metadata.reset_index()
    movie_name = input("Movie Name: ")
    movies = get_recommendation(movie_name, cosine_sim2)
    for idx,movie in enumerate(movies):
        print(idx+1, " ", movie)
    exit()
    # tfidf_matrix.get_feature_names()[:100]    
    #calculate the cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
   #Construct a reverse map of indices and movie titles
    indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
    # movies = get_recommendation("Star Wars")
    # for idx,movie in enumerate(movies):
    #     print(idx+1, " ", movie)
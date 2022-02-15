from audioop import reverse
from cmath import cos
from curses import meta
import enum
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
'''
We will extract feature with TfIdfVectorizer.

'''

def get_recommendation(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores.sort(key=lambda x:x[1], reverse = True)   
    sim_scores = sim_scores[1:11]
    movies = [metadata['title'][i[0]] for i in sim_scores]
    return movies

if __name__ == '__main__':
    metadata = pd.read_csv('../datasets/movies_metadata.csv', low_memory=False)
    #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')

    metadata['overview'] = metadata['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(metadata['overview'])
    # tfidf_matrix.get_feature_names()[:100]    
    #calculate the cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
   #Construct a reverse map of indices and movie titles
    indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
    movies = get_recommendation("The Dark Knight Rises")
    for idx,movie in enumerate(movies):
        print(idx+1, " ", movie)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels
import json
import numpy as np
import pandas as pd

def clean_text(word):
    return ''.join(word.lower().split(" "))

def get_similarity_between_2_words(options, target):
    # count = CountVectorizer(analyzer='char')
    # words = [clean_text(word1), clean_text(word2)]
    # count_matrix1 = count.transform([target])
    # count_matrix2 = count.fit_transform(options)
    # cosine_sim = cosine_similarity(count_matrix1, count.transform(count_matrix2))
    # print(cosine_sim)
    vec = CountVectorizer(analyzer='char')
    vec.fit(options)

    res = pairwise_kernels(vec.transform([target]),
                    vec.transform(options),
                    metric='cosine')[0]
    # print(options[np.where(res == max(res))[0]])
    # print(res)
    # print(np.where(res == max(res)))
    # print(max(res))
    index = np.where(res == max(res))[0]
    # print(type(index))
    return options[int(index)]

def get_similarity_between_2_words(options, target):
    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(options)

    # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                    columns=count_vectorizer.get_feature_names(),
                    index= options)
    print(df)
    index = np.where(options == target)
    print(index)
    print(cosine_similarity(df, df)[0])

if __name__ == '__main__':
    with open("RPI_ALAC.json", "r") as f:
        data = json.load(f) 
    # print(data.keys())
    options = list(data.keys())
    target = "Physics I"
    result = get_similarity_between_2_words(options, target)
    print(result)
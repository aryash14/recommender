from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



def create_dataframe(matrix, tokens):

    doc_names = [f'doc_{i+1}' for i, _ in enumerate(matrix)]
    # print(doc_names)
    df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    print(df)
count_vectorizer = CountVectorizer()

doc_1 = "Computer Science I"
doc_2 = "Comp Sci I"

data = [doc_1, doc_2]
vector_matrix = count_vectorizer.fit_transform(data)
# print(vector_matrix)
tokens = count_vectorizer.get_feature_names()
# print(tokens)
df = create_dataframe(vector_matrix.toarray(),tokens)
# print(df)
cosine_similarity_matrix = cosine_similarity(vector_matrix)
create_dataframe(cosine_similarity_matrix,['doc_1','doc_2'])
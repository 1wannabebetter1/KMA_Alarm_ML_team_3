## function returns True if the input num
def isNaN(num):
    return num != num

## function takes a sparse matrix in coordinate format (coo_matrix) and sorts its elements by descending order of scores
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

## function extracts the top topn features with their corresponding scores and returns them as a dictionary
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keen track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zio(feature_vals, score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return results

## function then extracts the top 100 words from the matrix using extract_topn_from_vector() and returns them as a dictionary.
def conver_doc_to_vector(doc, cv, tfidf):
    feature_names = cv.get_feature_names_out()
    top_n = 100
    tf_idf_vector = tfidf.transform(cv.transform([doc]))

    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())

    keywords = extract_topn_from_vector(feature_names, sorted_items, top_n)

    return keywords

import json
import sys
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer

MINIMAL_APPEARANCE_THRESHOLD = 10
K_CLUSTER_NUM = 1000
RECIPES_CLUSTER_FILE_BASE = "recipes_cluster"
COMMON_INGREDIENTS_FILE_NAME = 'common_ingredients'


def main(json_path):
    with open(json_path, 'r') as f:
        #consider reading data one-by-one if memory is too large
        data = json.load(f)
    counter_ingredients = Counter((recipe['parsed_ingredients'] for recipe in data))

    common_ingredients = []
    for i, key in enumerate(counter_ingredients):
        if counter_ingredients[key] > MINIMAL_APPEARANCE_THRESHOLD:
            common_ingredients.append((key, i))
    common_ingredients = set(common_ingredients)
    with open(COMMON_INGREDIENTS_FILE_NAME, 'a') as f:
        f.write(json.dumps(common_ingredients))

    ingredients_features_data = []
    for recipe in data:
        ingredients_features_data.append(",".join(
            (ingredient for ingredient in recipe['parsed_ingredients']
             if ingredient in common_ingredients)))

    vectorizer = CountVectorizer(max_features=len(common_ingredients), )
    ingredients_matrix = vectorizer.fit_transform(ingredients_features_data)
    ingredients_matrix = ingredients_matrix.toarray()

    kmeans_clustering = KMeans(n_clusters=K_CLUSTER_NUM)
    idx = kmeans_clustering.fit_predict(ingredients_matrix)

    cluster_files = []
    for i in range(idx.max() + 1):
        cluster_files.append(open("%s_%d" %(RECIPES_CLUSTER_FILE_BASE, i), "a"))
    for i, recipe in enumerate(data):
        recipe['cluster_id'] = idx[i]
        cluster_files[idx[i]].write(json.dumps(recipe) + "\n")
    for f in cluster_files:
        f.close()

if __name__ == '__main__':
    exit(main(sys.argv[1]))

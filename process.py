import json
import sys
from collections import Counter
from collections import OrderedDict
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer


MINIMAL_APPEARANCE_THRESHOLD = 20
K_CLUSTER_NUM = 1000
RECIPES_CLUSTER_FILE_BASE = "recipes_cluster"
COMMON_INGREDIENTS_FILE_NAME = 'common_ingredients'


def main(json_path):
    with open(json_path, 'r') as f:
        #consider reading data one-by-one if memory is too large
        data = [json.loads(recipe) for recipe in f.readlines()]
    for recipe in data:
        recipe['ingredient_types'] = [ingredient_tup[4] for ingredient_tup in recipe['parsed_ingredients']]
    counter_ingredients = Counter((item_type for recipe in data for item_type in recipe['ingredient_types']))

    common_ingredients = OrderedDict()
    for i, key in enumerate(counter_ingredients):
        if counter_ingredients[key] > MINIMAL_APPEARANCE_THRESHOLD:
            common_ingredients[key] = counter_ingredients[key]
    with open(COMMON_INGREDIENTS_FILE_NAME, 'w') as f:
        f.write(json.dumps(common_ingredients))
    #common_ingredients = set(common_ingredients)

    ingredients_features_data = []
    for recipe in data:
        ingredients_features_data.append(",".join(
            (ingredient for ingredient in recipe['ingredient_types']
             if ingredient in common_ingredients.keys())))

    vectorizer = CountVectorizer(max_features=len(common_ingredients))
    ingredients_matrix = vectorizer.fit_transform(ingredients_features_data)
    ingredients_matrix = ingredients_matrix.toarray()

    kmeans_clustering = KMeans(n_clusters=K_CLUSTER_NUM)
    idx = kmeans_clustering.fit_predict(ingredients_matrix)

    cluster_files = []
    for i in range(K_CLUSTER_NUM):
        cluster_files.append(open("%s_%d" %(RECIPES_CLUSTER_FILE_BASE, i), "a"))
    for i, recipe in enumerate(data):
        cluster_id = idx[i]
        recipe['cluster_id'] = str(cluster_id)
        cluster_files[cluster_id].write(json.dumps(recipe) + "\n")
    for f in cluster_files:
        f.close()

if __name__ == '__main__':
    # debug: exit(main("output_test_50"))
    exit(main(sys.argv[1]))


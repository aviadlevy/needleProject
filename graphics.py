import json
import sys
import networkx as nx
from collections import Counter
from collections import OrderedDict
import matplotlib.pyplot as plt

MIN_NODE_SIZE = 100
DIFF_NODE_SIZE = 500  # max is 600


def main(json_path):
    with open(json_path, 'r') as f:
        #consider reading data one-by-one if memory is too large
        data = [json.loads(recipe) for recipe in f.readlines()]

    G = nx.DiGraph()
    recipe_start_nodes = [recipe['title'] for recipe in data]
    G.add_nodes_from(recipe_start_nodes)

    recipe_labels = dict(((recipe['title'], recipe['title']) for recipe in data)) #directions

    ing_counter = Counter((ing for recipe in data for ing in recipe['ingredient_types']))

    max_count = max(ing_counter.values())
    min_count = min(ing_counter.values())
    diff_count = max_count - min_count
    node_sizes =  dict((x, MIN_NODE_SIZE) for x in recipe_start_nodes)

    pos_nodes = OrderedDict()
    pos_name_labels = OrderedDict()
    paths = dict()
    for i, recipe in enumerate(data):
        path =[recipe['title']]+recipe['ingredient_types']
        paths[recipe['title']] = path
        G.add_path(path)

        pos_nodes[recipe['title']] = 0,i*2
        pos_name_labels[recipe['title']] = 0, i*2+1
        x_pos = 5
        for ing in recipe['ingredient_types']:
            if ing not in pos_nodes:
                node_sizes[ing] = MIN_NODE_SIZE + ((ing_counter[ing] - min_count) / diff_count) * DIFF_NODE_SIZE
                pos_nodes[ing] = x_pos, i*2
                x_pos += 1

    nx.draw_networkx_nodes(G, pos_nodes, nodelist=node_sizes.keys(), node_size=[x for x in node_sizes.values()],
                           node_color='k', with_labels=False)
    nx.draw_networkx_labels(G, pos_name_labels, recipe_labels, font_size=9, font_color='r')
    nx.draw_networkx_edges(G, pos_nodes, nodelist=node_sizes.keys(), alpha=0.5)

    plt.show()

if __name__ == '__main__':
    exit(main(sys.argv[1]))


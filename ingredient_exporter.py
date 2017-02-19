import json
import re
import sys

QUANTITIES_TYPES = ['teaspoon', 'tsp', 'tablespoon', 'tbsp', 'cup', 'oz', 'pound', 'gram', 'kilogram', 'kg', 'ml',
                    'millilitre', 'milliliter', 'liter', 'pint', 'pnt', 'quart', 'gallon', 'dash', 'pinch', 'sprig',
                    'bag', 'can', 'package', 'bottle', 'slice', 'ounce']
ADJACTIVES = ['fresh', 'freshly', 'torn', 'chopped', 'condensed', 'small', 'diced', 'petite', 'large']


def parse_ingredients(ingredients):
    parsed_ingredients = []
    for ing in ingredients:
        parsed_ing = ing.split(",")[0]
        regex = re.match(r'(\d+\s?\d*/\d+|\d+\.\d+|\d+)?( \(.*\))?\s*(' + "|".join(
                [q + "s?" for q in QUANTITIES_TYPES]) + ')?\s*(' + "|".join([a for a in ADJACTIVES]) + ')?\s*('
                                                        '.*)', parsed_ing)
        if regex:
            parsed_ingredients.append(regex.groups())
        else:
            parsed_ingredients.append((None, None, None, None, parsed_ing))
    return parsed_ingredients


if __name__ == '__main__':
    file_name = sys.argv[1]
    parsed_recipes = []
    with open(file_name) as f:
        recipes = f.readlines()
    for recipe in recipes:
        rec_json = json.loads(recipe)
        ingredients = rec_json.get("ingredients")
        rec_json["parsed_ingredients"] = parse_ingredients(ingredients)
        parsed_recipes.append(json.dumps(rec_json) + "\n")
    with open("output_" + file_name, "w") as f:
        f.writelines(parsed_recipes)

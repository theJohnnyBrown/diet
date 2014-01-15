import json, uuid, string
for website in ["www.opensourcefood.com","www.halfhourmeals.com"]:
  reduced_recipes = []
  with open('../scraper/all/'+website+'.json') as f:
    for line in f:
      recipe = json.loads(line)
      reduced_recipe = {"link":recipe["link"],"id":uuid.uuid4().hex, "ingredients":[ing.strip(string.whitespace+string.punctuation) for ing in recipe["ingredients"]]}
      reduced_recipes.append(reduced_recipe)
  with open('reduced/'+website+'.json','w+') as f:
    for recipe in reduced_recipes:
      f.write(json.dumps(recipe)+'\n')

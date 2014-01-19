import json, uuid, string
for website in ["www.opensourcefood.com","www.halfhourmeals.com"]:
  reduced_recipes = []
  with open('../scraper/'+website+'.json') as f:
    for line in f:
      recipe = json.loads(line)
      reduced_recipe = {"link":recipe["link"],"id":uuid.uuid4().hex, "ingredients":recipe["ingredients"], "portions":recipe.get("portions", "0")}
      reduced_recipes.append(reduced_recipe)
  with open('reduced/'+website+'.json','w+') as f:
    for recipe in reduced_recipes:
      f.write(json.dumps(recipe)+'\n')

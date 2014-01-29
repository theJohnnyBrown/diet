import csv
files_dict = {"Baked Chicken":6, "Batter Fried Fish":4, "Beef Stir Fry":4, "Chana Masala":6, "Chicken Masala":1, "Chicken Quesadilla":1, "Chicken Satay":4, "Chilli Cauliflower and Broccoli":2, "Chilli Chicken":4, "Lasagne Bolognaise":6, "Mulligatawny":4, "Rajma Masala":3, "Traditional Roast Chicken":4, "Yellow Dal Fry":4}
files = [{"name":recipe_name, "serves":serves} for recipe_name, serves in files_dict.iteritems()]
recipes = []
recipe_names = []
for file in files:
	with open(file["name"]+".csv") as f:
		rows = []
		csvreader = csv.reader(f)
		for row in csvreader:
			rows.append(row)
		recipes.append(rows)
		recipe_names.append(file["name"])

nutrients = {}
for recipe in recipes:
	for nutrient_row in recipe[4:]:
		nutrient = nutrient_row[0]
		if nutrient not in nutrients:
			nutrients[nutrient] = []

for i, recipe in enumerate(recipes):
	for nutrient_row in recipe[4:]:
		nutrients[nutrient_row[0]].append(float(nutrient_row[-1]))
	for nutrient_name, nutrient_values in nutrients.iteritems():
		if len(nutrient_values) == i:
			nutrient_values.append(0)

for nutrient, nutrient_values in nutrients.iteritems():
	for recipe in recipe_names:
		nutrients[nutrient] = [value/files_dict[recipe] for value in nutrient_values]

for nutrient, nutrient_values in nutrients.iteritems():
	m = max(nutrient_values)
	if m != 0:
		nutrients[nutrient] = [value/m for value in nutrient_values]

with open("concat.csv", 'wb+') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(['']+recipe_names)
	for nutrient, nutrient_values in nutrients.iteritems():
		writer.writerow([nutrient]+nutrient_values)


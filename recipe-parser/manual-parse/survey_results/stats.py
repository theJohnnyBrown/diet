import csv, random

#Get nutritional content for recipes
recipes_by_nutrient = {}
recipe_list_for_nutrients = []
'''
recipes_by_nutrient
		r1 |r2
		-------
n1 | a | b
n2 | c | d
'''
with open("concat2.csv") as f:
	reader = csv.reader(f)
	first = True
	for row in reader:
		if first:
			recipe_list_for_nutrients = row[1:]
			first = False
		else:
			recipes_by_nutrient[row[0]] = [float(nutrient_value) for nutrient_value in row[1:]]

#Get food preferences
preferences_by_person = {}
recipe_list_for_preferences = []
'''
preferences_by_person
		r1 |r2
		-------
p1 | a | b
p2 | c | d
'''
with open("results.csv") as f:
	reader = csv.reader(f, delimiter='\t')
	first = True
	for row in reader:
		if first:
			recipe_list_for_preferences = row[1:-2]
			first = False
		elif '4' in row[1:-2] or '5' in row[1:-2]:
			preferences_by_person[row[0]] = [int(preference) for preference in row[1:-2]]

#Match all recipes
recipe_list_for_nutrients = [recipe for recipe in recipe_list_for_nutrients if recipe in recipe_list_for_preferences]

#Get correct order
recipe_order_from_nutrient_to_preferences = []
for recipe in recipe_list_for_nutrients:
	recipe_order_from_nutrient_to_preferences.append(recipe_list_for_preferences.index(recipe))

#Reorder preferences to match recipe order in recipes_by_nutrient
for person, preferences in preferences_by_person.iteritems():
	sorted_preferences = []
	for recipe_index in recipe_order_from_nutrient_to_preferences:
		sorted_preferences.append(preferences[recipe_index])
	preferences_by_person[person] = sorted_preferences

#Normalise values
normalised_recipes_by_nutrient = {}
for nutrient, nutrient_values in recipes_by_nutrient.iteritems():
	m = max(nutrient_values)
	if m != 0:
		normalised_recipes_by_nutrient[nutrient] = [nutrient_value/m for nutrient_value in nutrient_values]

#Split nutrient values by preference
split_nutrient_values_by_nutrients = {}
for person, preferences in preferences_by_person.iteritems():
	for i, preference in enumerate(preferences):
		for nutrient, nutrient_values in normalised_recipes_by_nutrient.iteritems():
			if nutrient not in split_nutrient_values_by_nutrients:
				split_nutrient_values_by_nutrients[nutrient] = [[],[]]
			if preference < 3:
				split_nutrient_values_by_nutrients[nutrient][0].append(nutrient_values[i]*(3-preference))
			elif preference > 3:
				split_nutrient_values_by_nutrients[nutrient][1].append(nutrient_values[i]*(preference-3))

#Get mean difference and p-value for each nutrient
p_values_by_nutrient = {}
mean_difference_by_nutrient = {}
number_done = 0.0
total_nutrients = len(split_nutrient_values_by_nutrients)
for nutrient, split_nutrient_values in split_nutrient_values_by_nutrients.iteritems():
	shuffled_nutrient_values = split_nutrient_values[0]+split_nutrient_values[1]
	number_of_disliked_labels = len(split_nutrient_values[0])
	mean_difference_by_nutrient[nutrient] = sum(split_nutrient_values[1])/len(split_nutrient_values[1]) - sum(split_nutrient_values[0])/len(split_nutrient_values[0])
	score = 0.0
	for x in range(10000):
		random.shuffle(shuffled_nutrient_values)
		shuffled_split_nutrient_values = [shuffled_nutrient_values[:number_of_disliked_labels], shuffled_nutrient_values[number_of_disliked_labels:]]
		shuffled_average = sum(shuffled_split_nutrient_values[1])/len(shuffled_split_nutrient_values[1]) - sum(shuffled_split_nutrient_values[0])/len(shuffled_split_nutrient_values[0])
		if shuffled_average >= mean_difference_by_nutrient[nutrient]:
			score += 1
	p_values_by_nutrient[nutrient] = score/10000
	number_done += 1
	print "Percentage done: %.1f %%" % (100*number_done/total_nutrients)

#Sort nutrients by mean difference
sorted_mean_difference_by_nutrient = sorted([(nutrient, mean_difference) for nutrient, mean_difference in mean_difference_by_nutrient.iteritems()],key=lambda x: x[1])[::-1]

#Save significant results
with open("RevisedResults.csv", 'wb+') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(["Nutrient", "Mean Difference", "P-Value"])
	for (nutrient, mean_difference) in sorted_mean_difference_by_nutrient:
		if p_values_by_nutrient[nutrient]<=0.05 or p_values_by_nutrient[nutrient]>=0.95:
			writer.writerow([nutrient, mean_difference, p_values_by_nutrient[nutrient]])


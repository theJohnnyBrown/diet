import json, csv, difflib, re, nltk
usda = None

def load_usda():
	global usda
	usda = []
	with open('nounUSDA.json') as f:
		for line in f:
			usda.append(json.loads(line))

def get_ratios(ing_name, db):
	reg = re.compile(r"[\w']+")
	ratios = {}
	ing_split = reg.findall(ing_name.lower())
	for ingredient in db:
		usda_name = ingredient["name"]["long"].lower()
		usda_split = []
		for word in reg.findall(usda_name):
			if word in ingredient["name"]["split"]:
				usda_split.append(word)
		if usda_split == []:
			usda_split = reg.findall(usda_name)
		ratio_list = [((ing_word, usda_word), difflib.SequenceMatcher(None, ing_word, usda_word).ratio()) for usda_word in usda_split for ing_word in ing_split]
		ratios[usda_name] = {key: value for (key, value) in ratio_list}
	return ratios

def get_max_ratio(ingredient

def get_bests(ratios):
	matches = (0,[])
	for ingredient, ratio_dict in ratios.iteritems():
		m = max([max(ratios) for ratios in ratio_list])
		if m > matches[0]:
			matches = (m, [ingredient])
		elif m == matches[0]:
			matches[1].append(ingredient)
	return matches

def get_max_averages(ratios):
	matches = (0,[])
	for ingredient, ratio_list in ratios.iteritems():
		average = [max(ratios) for ratios in ratio_list]
		average = sum(average)/len(average)
		if average > matches[0]:
			matches = (average, [ingredient])
		elif average == matches[0]:
			matches[1].append(ingredient)
	return matches

def get_bests_above_threshold(ratios, threshold):
	matches = (threshold,[])
	for ingredient, ratio_list in ratios.iteritems():
		m = max([max(ratios) for ratios in ratio_list])
		if m >= matches[0]:
			matches[1].append(ingredient)
	return matches

def get_averages_above_threshold(ratios, threshold):
	matches = (threshold,[])
	for ingredient, ratio_list in ratios.iteritems():
		average = [max(ratios) for ratios in ratio_list]
		average = sum(average)/len(average)
		if average >= matches[0]:
			matches[1].append(ingredient)
	return matches

def get_weighted_bests(ratios):
	matches = (0,[])
	for ingredient, ratio_list in ratios.iteritems():
		weighted_ratios_list = []
		for ratios in ratio_list:
			length = float(len(ratios))
			weighted_ratios_list.append([ratio*((length-i)/length) for i,ratio in enumerate(ratios)])
		m = max([max(weighted_ratios) for weighted_ratios in weighted_ratios_list])
		if m > matches[0]:
			matches = (m, [ingredient])
		elif m == matches[0]:
			matches[1].append(ingredient)
	return matches

def get_weighted_max_averages(ratios):
	matches = (0,[])
	for ingredient, ratio_list in ratios.iteritems():
		weighted_ratios_list = []
		for ratios in ratio_list:
			length = float(len(ratios))
			weighted_ratios_list.append([ratio*((length-i)/length) for i,ratio in enumerate(ratios)])
		average = [max(weighted_ratios) for weighted_ratios in weighted_ratios_list]
		average = sum(average)/len(average)
		if average > matches[0]:
			matches = (average, [ingredient])
		elif average == matches[0]:
			matches[1].append(ingredient)
	return matches

def get_weighted_bests_above_threshold(ratios, threshold):
	matches = (threshold,[])
	for ingredient, ratio_list in ratios.iteritems():
		weighted_ratios_list = []
		for ratios in ratio_list:
			length = float(len(ratios))
			weighted_ratios_list.append([ratio*((length-i)/length) for i,ratio in enumerate(ratios)])
		m = max([max(weighted_ratios) for weighted_ratios in weighted_ratios_list])
		if m >= matches[0]:
			matches[1].append(ingredient)
	return matches

def get_weighted_averages_above_threshold(ratios, threshold):
	matches = (threshold,[])
	for ingredient, ratio_list in ratios.iteritems():
		weighted_ratios_list = []
		for ratios in ratio_list:
			length = float(len(ratios))
			weighted_ratios_list.append([ratio*((length-i)/length) for i,ratio in enumerate(ratios)])
		average = [max(weighted_ratios) for weighted_ratios in weighted_ratios_list]
		average = sum(average)/len(average)
		if average >= matches[0]:
			matches[1].append(ingredient)
	return matches

def main():
	global usda
	load_usda()
	ingredients = []
	with open('testRecipe.json') as f:
		ingredients = json.load(f)["ingredients_no_quantities_no_units"]
	names = {"large flour tortillas":"tortillas, ready-to-bake or -fry, flour, shelf stable","fresh lime juice":"lime juice, raw","small avocado, stone removed, peeled, mashed":"avocados, raw, all commercial varieties","coarsely grated vintage cheddar":"cheese, cheddar","baby spinach leaves":"spinach, raw","Greek-style feta, crumbled":"cheese, feta","smoked chicken breast fillet, thinly sliced":"chicken, broiler or fryers, breast, skinless, boneless, meat only, cooked, grilled"}
	for i, ingredient in enumerate(ingredients):
		ratios = get_ratios(ingredient, usda)
		print ingredient
		match = []

		match.append((sorted(get_bests(ratios)[1]), "best", ""))

		match.append((sorted(get_max_averages(ratios)[1]), "average", ""))

		threshold = 1.0
		tmp_match = sorted(get_averages_above_threshold(ratios,threshold)[1])
		while all(map(lambda name: name not in tmp_match, [name for orig, name in names.iteritems()])) and threshold != 0:
			threshold -= 0.25
			tmp_match = sorted(get_averages_above_threshold(ratios,threshold)[1])
		match.append((tmp_match, "threshold average", threshold))

		threshold = 1.0
		tmp_match = sorted(get_bests_above_threshold(ratios,threshold)[1])
		while all(map(lambda name: name not in tmp_match, [name for orig, name in names.iteritems()])) and threshold != 0:
			threshold -= 0.25
			tmp_match = sorted(get_bests_above_threshold(ratios,threshold)[1])
		match.append((tmp_match, "threshold max", threshold))

		match.append((sorted(get_weighted_bests(ratios)[1]), "weighted max", ""))

		match.append((sorted(get_weighted_max_averages(ratios)[1]), "weighted average", ""))

		threshold = 1.0
		tmp_match = sorted(get_weighted_bests_above_threshold(ratios,threshold)[1])
		while all(map(lambda name: name not in tmp_match, [name for orig, name in names.iteritems()])) and threshold != 0:
			threshold -= 0.25
			tmp_match = sorted(get_weighted_bests_above_threshold(ratios,threshold)[1])
		match.append((tmp_match, "weighted threshold best", threshold))

		threshold = 1.0
		tmp_match = sorted(get_weighted_averages_above_threshold(ratios,0.5)[1])
		while all(map(lambda name: name not in tmp_match, [name for orig, name in names.iteritems()])) and threshold != 0:
			threshold -= 0.25
			tmp_match = sorted(get_weighted_averages_above_threshold(ratios,0.5)[1])
		match.append((tmp_match, "weighted threshold average", threshold))

		for matched in match:
			if any(map(lambda name: name in matched[0], [name for orig, name in names.iteritems()])):
				print "method: "+matched[1]
				print "length: "+str(len(matched[0]))
				print "threshold: "+str(matched[2])
				print ""
		print '>'*80



if __name__=="__main__":
	main()


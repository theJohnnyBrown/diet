import json, csv, difflib, re, nltk
usda = None

def load_usda():
	global usda
	usda = []
	split_usda = []
	with open('splitUSDA.json') as f:
		for line in f:
			usda.append(json.loads(line))

def get_nouns(ingredient_name):
	text = nltk.word_tokenize(ingredient_name)
	tagged_name = nltk.pos_tag(text)
	nouns = [word for (word, tag) in tagged_name if tag in ["NN","NNP","NNPS","NNS","NP"]]
	if len(nouns) == 0:
		nouns = [word for (word, tag) in tagged_name if tag == "JJ"]
	if len(nouns) == 0:
		nouns = [word for (word, tag) in tagged_name if tag == ["RB","VBN","DT"]]
	if len(nouns) == 0:
		reg = re.compile(r"[\w']+")
		nouns = reg.findall(ingredient_name)
	return nouns

def get_ratios(ingredient_name, db):
	reg = re.compile(r"[\w']+")
	ratios = {}
	ingredient_name_split = reg.findall(ingredient_name.lower())
	for ingredient in db:
		usda_name = ingredient["name"]["long"].lower()
		usda_name_split = reg.findall(usda_name)
		ratios[usda_name] = []
		for ingredient_word in ingredient_name_split:
			ratios[usda_name].append([difflib.SequenceMatcher(None, ingredient_word, usda_word).ratio() for usda_word in usda_name_split])
	return ratios

def get_bests(ratios):
	matches = (0,[])
	for ingredient, ratio_list in ratios.iteritems():
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
	second = False
	for ingredient in ingredients:
		if second:
			ratios = get_ratios(ingredient, usda)
			print ingredient
			name = "spinach, raw"
			match = []

			match.append(sorted(get_bests(ratios)[1]))

			match.append(sorted(get_max_averages(ratios)[1]))

			threshold = 1.0
			tmp_match = sorted(get_averages_above_threshold(ratios,threshold)[1])
			while name not in tmp_match and threshold != 0:
				threshold -= 0.25
				tmp_match = sorted(get_averages_above_threshold(ratios,threshold)[1])
			match.append(tmp_match)
			print(threshold)

			threshold = 1.0
			tmp_match = sorted(get_bests_above_threshold(ratios,threshold)[1])
			while name not in tmp_match and threshold != 0:
				threshold -= 0.25
				tmp_match = sorted(get_bests_above_threshold(ratios,threshold)[1])
			match.append(tmp_match)
			print(threshold)

			match.append(sorted(get_weighted_bests(ratios)[1]))

			match.append(sorted(get_weighted_max_averages(ratios)[1]))

			threshold = 1.0
			tmp_match = sorted(get_weighted_bests_above_threshold(ratios,threshold)[1])
			while name not in tmp_match and threshold != 0:
				threshold -= 0.25
				tmp_match = sorted(get_weighted_bests_above_threshold(ratios,threshold)[1])
			match.append(tmp_match)
			print(threshold)

			threshold = 1.0
			tmp_match = sorted(get_weighted_averages_above_threshold(ratios,0.5)[1])
			while name not in tmp_match and threshold != 0:
				threshold -= 0.25
				tmp_match = sorted(get_weighted_averages_above_threshold(ratios,0.5)[1])
			match.append(tmp_match)
			print(threshold)

			for matched in match:
				print len(matched)
				print json.dumps(matched,indent=4)
				print '-'*80
			print '*'*80
			raw_input()
		else:
			second = True



if __name__=="__main__":
	main()


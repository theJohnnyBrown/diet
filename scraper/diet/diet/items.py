from scrapy.item import Item, Field

class RecipeItem(Item):
	title = Field()
	link = Field()
	ingredients = Field()
	steps = Field()
	portions = Fiel()
	difficulty = Field()
	time = Field()

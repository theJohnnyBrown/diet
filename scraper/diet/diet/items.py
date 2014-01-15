from scrapy.item import Item, Field

class RecipeItem(Item):
  title = Field()
  link = Field()
  ingredients = Field()
  method = Field()
  portions = Field()
  difficulty = Field()
  time = Field()

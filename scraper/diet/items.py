from scrapy.item import Item, Field

class RecipeItem(Item):
  title = Field()
  link = Field()
  ingredients = Field()
  method = Field()
  description = Field()
  portions = Field()
  difficulty = Field()
  prep_time = Field()
  cook_time = Field()

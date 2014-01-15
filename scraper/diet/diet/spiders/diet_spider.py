from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from diet.items import RecipeItem

from bs4 import BeautifulSoup


class OpenSourceFoodSpider(CrawlSpider):
  name = "diet"
  allowed_domains = ["opensourcefood.com"]
  start_urls = ["http://www.opensourcefood.com/recipes/popular"]
  rules = [Rule(SgmlLinkExtractor(allow=('.*/people/.*?/recipes/.*')), callback='parse_recipe', follow=True)]

  def parse_recipe(self, response):
    sel = Selector(response)
    item = RecipeItem()
    if "opensourcefood" in response.url:
      item["title"] = sel.xpath('//h1[@class="subheading"]/text()').extract()
      item["link"] = response.url
      ingredient_html = sel.xpath('//div[@id="recipe_ingredients"]//ul').extract()[0]
      soup = BeautifulSoup(ingredient_html)
      ingredient_list = soup.find_all("li")
      item["ingredients"] = []
      for ingredient in ingredient_list:
        item["ingredients"].append(ingredient.get_text())
      item["method"] = sel.xpath('//div[@id="method_inner"]').extract()
    return item

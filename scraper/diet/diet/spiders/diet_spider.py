from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from diet.items import RecipeItem
from bs4 import BeautifulSoup

count = [True, True]

class OpenSourceFoodSpider(CrawlSpider):
  name = "diet"
  allowed_domains = ["opensourcefood.com", "halfhourmeals"]
  start_urls = ["http://www.opensourcefood.com/recipes/popular", "http://www.opensourcefood.com/recipes/all_time_best"]
  rules = [Rule(SgmlLinkExtractor(allow=('.*/people/.*?/recipes/.*')), callback='parse_recipe', follow=True)]

  def parse_recipe(self, response):
    sel = Selector(response)
    item = RecipeItem()
    item["link"] = response.url
    if "opensourcefood" in response.url:
      item["title"] = sel.xpath('//h1[@class="subheading"]/text()').extract()[0]
      ingredient_html = ''.join(sel.xpath('//div[@id="recipe_ingredients"]').xpath('.//ul[not (@id)]').extract())
      soup = BeautifulSoup(ingredient_html)
      ingredient_list = soup.find_all("li")
      item["ingredients"] = []
      for ingredient in ingredient_list:
        item["ingredients"].append(ingredient.get_text())
      item["method"] = ''.join(sel.xpath('//div[@id="method_inner"]/node()').extract())
    elif "halfhourmeals" in response.url:
      item["title"] = sel.xpath('//h1[@itemprop="name"]/text()').extract()[0]
      item["portions"] = sel.xpath('//span[@itemprop="yield"]/text()').extract()[0]
      item["prep_time"] = sel.xpath('//time[@itemprop="prepTime"]/text()').extract()[0]
      item["cook_time"] = sel.xpath('//time[@itemprop="cookTime"]/text()').extract()[0]
      item["difficulty"] = sel.xpath('//li[@class="difficulty"]/span/text()').extract()[0]
      item["description"] = ''.join(sel.xpath('//p[@itemprop="summary"]/text()').extract())
      item["ingredients"] = ''.join(sel.xpath('//p[@class="desc ingredients"]/text()').extract()).split(',')
      method = sel.xpath('//div[@class="section"]').xpath('.//p[@class="desc"]').extract()[1]
      soup = BeautifulSoup(method)
      item["method"] = soup.get_text()
    return item

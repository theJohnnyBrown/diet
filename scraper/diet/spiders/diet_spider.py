from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from diet.items import RecipeItem
from bs4 import BeautifulSoup

count = [True, True]

class OpenSourceFoodSpider(CrawlSpider):
  total = 0.0
  faulty = 0.0
  name = "diet"
  allowed_domains = ["opensourcefood.com", "halfhourmeals"]
  start_urls = ["http://www.opensourcefood.com/recipes/popular", "http://www.opensourcefood.com/recipes/all_time_best"]
  rules = [Rule(SgmlLinkExtractor(allow=('.*/people/.*?/recipes/.*')), follow=True, callback='parse_recipe'),\
  Rule(SgmlLinkExtractor(allow=('.*/recipes/.*?/page/.*')), follow=True)]

  def parse_recipe(self, response):
    sel = Selector(response)
    item = RecipeItem()
    item["link"] = response.url
    if "opensourcefood" in response.url:
      item["title"] = sel.xpath('//h1[@class="subheading"]/text()').extract()[0]
      ingredient_html = sel.xpath('//div[@id="recipe_ingredients"]').extract()[0]
      soup = BeautifulSoup(ingredient_html)
      item["ingredients"] = []
      for div in soup.div.find_all("div"):
        div.extract()
      if len(soup.find_all("ul")) > 0:
        for ingredient in soup.find_all("li"):
          item["ingredients"].append(ingredient.get_text())
      else:
        soup.div.h3.extract()
        for ingredient in soup.div.stripped_strings:
          if any(c.isalpha() for c in ingredient):
            item["ingredients"].append(ingredient)
        if len(item["ingredients"]) == 1:
          item["ingredients"] = soup.div.get_text().split(',')
        if len(item["ingredients"]) == 1:
          item["ingredients"] = soup.div.get_text().split('.')
      item["method"] = ''.join(sel.xpath('//div[@id="method_inner"]/node()').extract())
    elif "halfhourmeals" in response.url:
      item["title"] = sel.xpath('//h1[@itemprop="name"]/text()').extract()[0]
      item["portions"] = sel.xpath('//span[@itemprop="yield"]/text()').extract()[0]
      item["prep_time"] = sel.xpath('//time[@itemprop="prepTime"]/text()').extract()[0]
      item["cook_time"] = sel.xpath('//time[@itemprop="cookTime"]/text()').extract()[0]
      item["difficulty"] = sel.xpath('//li[@class="difficulty"]/span/text()').extract()[0]
      item["description"] = ''.join(sel.xpath('//p[@itemprop="summary"]/text()').extract())
      ingredient_html = sel.xpath('//p[@class="desc ingredients"]').extract()[0]
      soup = BeautifulSoup(ingredient_html)
      item["ingredients"] = []
      for string in soup.p.stripped_strings:
        item["ingredients"].append(string)
      if len(item["ingredients"]) == 1:
        item["ingredients"] = soup.p.get_text().split(',')
      if len(item["ingredients"]) == 1:
        item["ingredients"] = soup.p.get_text().split('.')
      method = sel.xpath('//div[@class="section"]').xpath('.//p[@class="desc"]').extract()[1]
      soup = BeautifulSoup(method)
      item["method"] = soup.get_text()
    OpenSourceFoodSpider.total+=1
    if len(item["ingredients"])==1:
      OpenSourceFoodSpider.faulty+=1
      print item["link"]
      print OpenSourceFoodSpider.faulty/OpenSourceFoodSpider.total
    return item

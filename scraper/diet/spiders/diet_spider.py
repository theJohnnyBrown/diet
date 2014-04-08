from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from diet.items import RecipeItem
from bs4 import BeautifulSoup
import string

count = [True, True]

class USDARecipeSpider(CrawlSpider):
  total = 0.0
  faulty = 0.0
  name = "usda"
  allowed_domains = ["recipefinder.nal.usda.gov"]
  start_urls = ["http://recipefinder.nal.usda.gov/recipes"]
  rules = [
    Rule(SgmlLinkExtractor(allow=(r'/recipes\?page=\d+'),), follow=True,
         callback="parse"),
    Rule(SgmlLinkExtractor(allow=('/recipes/*'),
                           restrict_xpaths='//h2[@property="schema:name"]/a'),
         follow=True, callback='parse_recipe')]
  log = open('log','w+')

  def parse(self, response):
    # import pdb;pdb.set_trace()
    return super(USDARecipeSpider, self).parse(response)

  def parse_recipe(self, response):
    sel = Selector(response)
    item = RecipeItem()
    item["link"] = response.url

    item["title"] = sel.xpath('//h1[@id="page-title"]/text()').extract()[0]
    ingredient_html = (sel.xpath("//div[contains(@class,'recipe-ingredients')]")
                       .extract()[0])
    soup = BeautifulSoup(ingredient_html)
    item["ingredients"] = []
    if len(soup.find_all('tr')) > 0:
      for ingredient in soup.find_all('tr'):
        item["ingredients"].append(ingredient.get_text())

    ptns = sel.xpath('//form[@id="recipe-yield-form--2"]/div/text()').extract()[0]
    ptns = ptns.strip().lower().strip("\u00a0serving")
    item["portions"] = ptns

    USDARecipeSpider.total += 1
    if len(item["ingredients"]) <= 1:
      USDARecipeSpider.faulty+=1
      USDARecipeSpider.log.write(item["link"]+'\n')
      USDARecipeSpider.log.write("Incorrectly parsed items: {percent:.2%}\n".format(percent=USDARecipeSpider.faulty/USDARecipeSpider.total))
      return None
    else:
      return item


class OpenSourceFoodSpider(CrawlSpider):
  total = 0.0
  faulty = 0.0
  name = "diet"
  allowed_domains = ["opensourcefood.com", "halfhourmeals"]
  start_urls = ["http://www.opensourcefood.com/recipes/popular", "http://www.opensourcefood.com/recipes/all_time_best"]
  rules = [
    Rule(SgmlLinkExtractor(allow=('.*/people/.*?/recipes/.*')),
         follow=True, callback='parse_recipe'),
    Rule(SgmlLinkExtractor(allow=('.*/recipes/.*?/page/.*')), follow=True)]
  log = open('log','w+')

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
      item["ingredients"] = [ing.strip(string.whitespace+string.punctuation) for ing in item["ingredients"]]
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
      for s in soup.p.stripped_strings:
        item["ingredients"].append(s)
      if len(item["ingredients"]) == 1:
        item["ingredients"] = soup.p.get_text().split(',')
      if len(item["ingredients"]) == 1:
        item["ingredients"] = soup.p.get_text().split('.')
      item["ingredients"] = [ing.strip(string.whitespace+string.punctuation) for ing in item["ingredients"]]
      method = sel.xpath('//div[@class="section"]').xpath('.//p[@class="desc"]').extract()[1]
      soup = BeautifulSoup(method)
      item["method"] = soup.get_text()
    OpenSourceFoodSpider.total+=1
    if len(item["ingredients"])<=1:
      OpenSourceFoodSpider.faulty+=1
      OpenSourceFoodSpider.log.write(item["link"]+'\n')
      OpenSourceFoodSpider.log.write("Incorrectly parsed items: {percent:.2%}\n".format(percent=OpenSourceFoodSpider.faulty/OpenSourceFoodSpider.total))
      return None
    else:
      return item

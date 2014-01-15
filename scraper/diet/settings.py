# Scrapy settings for diet project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'diet'

SPIDER_MODULES = ['diet.spiders']
NEWSPIDER_MODULE = 'diet.spiders'
ITEM_PIPELINES = {'diet.pipelines.DomainSeparatorPipeline': 000}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'diet (+http://www.yourdomain.com)'

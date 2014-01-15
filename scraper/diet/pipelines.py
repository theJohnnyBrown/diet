from scrapy import signals
from urlparse import urlparse
from scrapy.contrib.exporter import JsonLinesItemExporter

class DomainSeparatorPipeline(object):

  def __init__(self):
    self.files = {}
    self.exporters = {}

  def process_item(self, item, spider):
    url = urlparse(item["link"])
    if url.hostname not in self.files:
      file = open(url.hostname+'.json', 'w+')
      self.files[url.hostname] = file
      self.exporters[url.hostname] = JsonLinesItemExporter(file)
    self.exporters[url.hostname].export_item(item)
    return item

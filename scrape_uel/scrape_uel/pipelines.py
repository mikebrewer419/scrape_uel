# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter


class CsvExportPipeline(object):
    def __init__(self):
        self.file = open('out.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = ['volume', 'year', 'title', 'description', 'pdf_url', 'issn']
  
    def open_spider(self, spider):
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        print('this is very good')
        self.exporter.export_item(item)
        return item

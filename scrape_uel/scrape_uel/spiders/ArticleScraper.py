from gc import callbacks
import scrapy
from scrapy.loader import ItemLoader
import re
from scrape_uel.items import ArticleItem



class ArticlescraperSpider(scrapy.Spider):
	name = 'ArticleScraper'
	start_urls = [
		'https://www.uel.br/revistas/uel/index.php/semagrarias/issue/archive?issuesPage=4#issues']
	
	def __init__(self, category=None, *args, **kwargs):
		super(ArticlescraperSpider, self).__init__(*args, **kwargs)
	
	def parse(self, response):
		article_list_page_anchors = response.xpath("//div[starts-with(@id,'issue')]/h4/a")
		yield from response.follow_all(article_list_page_anchors, callback=self.parse_article_list_page)
		pagination_anchors = response.xpath("//a[starts-with(@href, 'https://www.uel.br/revistas/uel/index.php/semagrarias/issue/archive?issuesPage=')]")
		yield from response.follow_all(pagination_anchors, callback=self.parse_volume_list_page)
	
	def parse_volume_list_page(self, response):
		article_list_page_anchors = response.xpath("//div[starts-with(@id,'issue')]/h4/a")
		yield from response.follow_all(article_list_page_anchors, callback=self.parse_article_list_page)
		

	def parse_article_list_page(self, response):
		anchors = response.xpath("//table[@class='tocArticle']//div[@class='tocTitle']/a")
		yield from response.follow_all(anchors, callback=self.parse_article)

	def parse_article(self, response):
		loader = ItemLoader(item = ArticleItem(), response=response)
		item = ArticleItem()
		title = response.xpath("//div[@id='articleTitle']/h3/text()").get()
		description = response.xpath("//div[@id='articleAbstract']/div/text()").get()
		pdf_url = response.xpath("//div[@id='articleFullText']/a/@href").get()
		issn = response.xpath("//center/descendant::span/text()").re_first(r'E-ISSN [0-9]*-[0-9]*')

		volume = response.xpath("//div[@id='breadcrumb']/a/text()").getall()
		
		if len(volume) > 1:
			volume = volume[1].split()
		volume, year = re.match("Vol (\d*), No \d \((\d*)\)", "Vol 1, No 1 (1978)").groups()
		yield {
			'volume': volume,
			'year': year,
			'title': title,
			'description': description,
			'pdf_url': pdf_url,
			'issn': issn
		}
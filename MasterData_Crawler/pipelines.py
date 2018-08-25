
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import XmlItemExporter
from lxml import etree


class XmlExportPipeline(object):

	def __init__(self):
		self.XML_FILE = "MasterSearch.xml"
		self.root = ""
		self.count = 0

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		self.root = etree.Element("Data")
		self.doc = etree.ElementTree(self.root)
		

	def spider_closed(self, spider):
		self.doc.write(self.XML_FILE, pretty_print=True)


	def process_item(self, item, spider):
		if item["element"] == 'LOCAL_BODY':
			new_sub = etree.SubElement(self.root, "LocalBody", value=item['value'] + " ", text=item['text'])
		if item["element"] == 'DIVISION':
			new_sub = etree.SubElement(self.root, "Division", value=item['value'] + " ", text=item['text'])
		if item["element"] == 'DISTRICT':
			new_sub = etree.SubElement(self.root, "District", value=item['value'] + " ", text=item['text']+" ",division=item['division'])
		if item['element'] == 'ELECTION_PROGRAM':
			new_sub = etree.SubElement(self.root, "ElectionProgram", value=item['value'] + " ", text=item['text']+" ",district=item['district'])
		if item['element'] == 'Electoral_Division_Number':
			new_sub = etree.SubElement(self.root, "ElectoralDivisionNumber", value=item['value'] + " ", text=item['text']+" ",electionProgram=item['electionProgram'])
		if item['element'] == 'CANDIDATE_LIST':
			new_sub = etree.SubElement(self.root, "CANDIDATE_DATA", RegistrationNo=item['RegistrationNo'] + " ", 
			FULLNAME=item['FULLNAME']+" ",NameofElectoralDivision=item['NameofElectoralDivision']+" ",
			ElectoralDivisionID=item['ElectoralDivisionID'])
			
		
		
		self.doc.write(self.XML_FILE, pretty_print=True)
		return item





# class MarutiCrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item
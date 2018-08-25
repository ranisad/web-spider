# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
	text = scrapy.Field()
	value = scrapy.Field()  
	element = scrapy.Field()
	division = scrapy.Field()
	district = scrapy.Field()
	electionProgram = scrapy.Field()
	RegistrationNo = scrapy.Field()
	FULLNAME = scrapy.Field()
	NameofElectoralDivision = scrapy.Field()
	ElectoralDivisionID = scrapy.Field()

	


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
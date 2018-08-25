import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import Selector
from MasterData_Crawler.items import CrawlerItem
from lxml import etree
# from utility import utils
import json
from scrapy.crawler import CrawlerProcess
import logging

class MasterDataSpider(scrapy.Spider):
	name = "web_spider"

	def start_requests(self):
		return [Request(url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx",callback = self.parse_models)]


	def parse_models(self,response):		
		html = etree.HTML(response.body)
		localBodies = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLLocalBody']/option[position() > 1]/@value")
		localBodiesText = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLLocalBody']/option[position() > 1]/text()")

		for i in range(len(localBodies)):
			item  = CrawlerItem()
			item['text'] = localBodiesText[i]
			item['value'] = localBodies[i]
			item['element'] = "LOCAL_BODY"
			yield item

		for localBody in localBodies:
			__EVENTTARGET = "ContentPlaceHolder1_SearchControl1_DDLLocalBody"
			__EVENTARGUMENT = ""
			__LASTFOCUS = ""
			__VIEWSTATE= html.xpath("//input[@id='__VIEWSTATE']/@value")
			__VIEWSTATEGENERATOR = html.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value")
			__EVENTVALIDATION = html.xpath("//input[@id='__EVENTVALIDATION']/@value")
			ddllocalBody = localBody
			__ASYNCPOST = "true"
			ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody"
			payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,'__EVENTTARGET':__EVENTTARGET, '__EVENTARGUMENT':__EVENTARGUMENT, '__LASTFOCUS':__LASTFOCUS,'__VIEWSTATE':__VIEWSTATE,'__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			'__EVENTVALIDATION':__EVENTVALIDATION,'__ASYNCPOST':__ASYNCPOST,'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody
			} 
			url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
			headers = {'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
			request = FormRequest(url=url,formdata=payload_states,callback = self.parse_division,headers = headers,meta = {"localBody":localBody,"ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision":0})

			yield request



	def parse_division(self,response):
		matching = [s for s in response.body.split("\n") if "__VIEWSTATE" in s]
		html = etree.HTML(response.body)
		hidden_values = response.body.split("\n")[0]
		values = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLDivision']/option[position() > 1]/@value")
		texts = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLDivision']/option[position() > 1]/text()")
		
		for i in range(len(values)):
			item  = CrawlerItem()
			item['text'] = texts[i]
			item['value'] = values[i]
			item['element'] = "DIVISION"
			yield item

		hidden_values = matching[0]

		for val in values:
			__EVENTTARGET = "ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision"
			__EVENTARGUMENT = ""
			__LASTFOCUS = ""
			__VIEWSTATE= hidden_values.split("|")[16]
			# __VIEWSTATEGENERATOR = hidden_values.split("|")[20]
			__EVENTVALIDATION = hidden_values.split("|")[20]
			localBody = response.meta["localBody"]
			division = val
			__ASYNCPOST = "true"
			ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision"
			payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,
			'__EVENTTARGET':__EVENTTARGET, 
			'__EVENTARGUMENT':__EVENTARGUMENT, 
			'__LASTFOCUS':__LASTFOCUS,
			'__VIEWSTATE':__VIEWSTATE,
			# '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			'__EVENTVALIDATION':__EVENTVALIDATION,
			'__ASYNCPOST':__ASYNCPOST,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision':division
			} 
			url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
			headers = {'X-MicrosoftAjax': 'Delta=true',
			'ASP.NET_SessionId':'lkcm5tekxol32uxujtalve2i',
			'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
			request = FormRequest(url=url,formdata=payload_states,callback = self.parse_district,headers = headers,meta = {'localBody':localBody,'division':division})
			
			yield request

	def parse_district(self,response):
		html = etree.HTML(response.body)
		values = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLDistrict']/option[position() > 1]/@value")
		texts = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLDistrict']/option[position() > 1]/text()")

		for i in range(len(values)):
			item  = CrawlerItem()
			item['text'] = texts[i]
			item['value'] = values[i]
			item['division'] = response.meta['division']
			item['element'] = "DISTRICT"
			yield item
		
		matching = [s for s in response.body.split("\n") if "__VIEWSTATE" in s]
		hidden_values = matching[0]

		for val in values:
			__EVENTTARGET = "ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict"
			__EVENTARGUMENT = ""
			__LASTFOCUS = ""
			__VIEWSTATE= hidden_values.split("|")[16]
			# __VIEWSTATEGENERATOR = hidden_values.split("|")[20]
			__EVENTVALIDATION = hidden_values.split("|")[20]
			localBody = response.meta["localBody"]
			division = response.meta['division']
			__ASYNCPOST = "true"
			ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict"
			payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,
			'__EVENTTARGET':__EVENTTARGET, 
			'__EVENTARGUMENT':__EVENTARGUMENT, 
			'__LASTFOCUS':__LASTFOCUS,
			'__VIEWSTATE':__VIEWSTATE,
			# '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			'__EVENTVALIDATION':__EVENTVALIDATION,
			'__ASYNCPOST':__ASYNCPOST,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision':division,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict':val
			} 
			url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
			headers = {'X-MicrosoftAjax': 'Delta=true',
			'ASP.NET_SessionId':'lkcm5tekxol32uxujtalve2i',
			'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
			request = FormRequest(url=url,formdata=payload_states,callback = self.parse_electionProgram,headers = headers,meta = {'localBody':localBody,'division':division,'district':val})
			yield request

	def parse_electionProgram(self,response):
		html = etree.HTML(response.body)
		values = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_ddlEP']/option[position() > 1]/@value")
		texts = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_ddlEP']/option[position() > 1]/text()")
		hdnLocalBody = html.xpath("//input[@id='ContentPlaceHolder1_SearchControl1_hdnLocalBody']/@value")

		for i in range(len(values)):
			item  = CrawlerItem()
			item['text'] = texts[i]
			item['value'] = values[i]
			item['district'] = response.meta['district']
			item['element'] = "ELECTION_PROGRAM"
			yield item

		matching = [s for s in response.body.split("\n") if "__VIEWSTATE" in s]
		hidden_values = matching[0]


		for val in values:
			__EVENTTARGET = "ctl00$ContentPlaceHolder1$SearchControl1$ddlEP"
			__EVENTARGUMENT = ""
			__LASTFOCUS = ""
			__VIEWSTATE= hidden_values.split("|")[16]
			# __VIEWSTATEGENERATOR = hidden_values.split("|")[20]
			__EVENTVALIDATION = hidden_values.split("|")[20]
			localBody = response.meta["localBody"]
			division = response.meta['division']
			district = response.meta['district']
			__ASYNCPOST = "true"
			ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict"
			payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,
			'__EVENTTARGET':__EVENTTARGET, 
			'__EVENTARGUMENT':__EVENTARGUMENT, 
			'__LASTFOCUS':__LASTFOCUS,
			'__VIEWSTATE':__VIEWSTATE,
			# '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			'__EVENTVALIDATION':__EVENTVALIDATION,
			'__ASYNCPOST':__ASYNCPOST,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision':division,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict':district,
			'ctl00$ContentPlaceHolder1$SearchControl1$ddlEP':val,
			'ctl00$ContentPlaceHolder1$SearchControl1$hdnElectionProgram':'',
			'ctl00$ContentPlaceHolder1$SearchControl1$hdnLocalBody':hdnLocalBody[0]
			} 

			url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
			headers = {'X-MicrosoftAjax': 'Delta=true',
			'ASP.NET_SessionId':'lkcm5tekxol32uxujtalve2i',
			'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
			request = FormRequest(url=url,formdata=payload_states,callback = self.parse_electoralDivisionNumber,headers = headers,meta = {'localBody':localBody,'division':division,'district':district,"EP":val})
			yield request

	def parse_electoralDivisionNumber(self,response):
		html = etree.HTML(response.body)
		values = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLEDnumber']/option[position() > 1]/@value")
		texts = html.xpath("//select[@id='ContentPlaceHolder1_SearchControl1_DDLEDnumber']/option[position() > 1]/text()")
		hdnLocalBody = html.xpath("//input[@id='ContentPlaceHolder1_SearchControl1_hdnLocalBody']/@value")

		for i in range(len(values)):
			item  = CrawlerItem()
			item['text'] = texts[i]
			item['value'] = values[i]
			item['electionProgram'] = response.meta['EP']
			item['element'] = "Electoral_Division_Number"
			yield item

		matching = [s for s in response.body.split("\n") if "__VIEWSTATE" in s]
		hidden_values = matching[0]


		for val in values:
			__EVENTTARGET = "ctl00$ContentPlaceHolder1$SearchControl1$DDLEDnumber"
			__EVENTARGUMENT = ""
			__LASTFOCUS = ""
			__VIEWSTATE= hidden_values.split("|")[16]
			# __VIEWSTATEGENERATOR = hidden_values.split("|")[20]
			__EVENTVALIDATION = hidden_values.split("|")[20]
			localBody = response.meta["localBody"]
			division = response.meta['division']
			district = response.meta['district']
			EP = response.meta['EP']
			__ASYNCPOST = "true"
			ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$SearchControl1$DDLEDnumber"
			payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,
			'__EVENTTARGET':__EVENTTARGET, 
			'__EVENTARGUMENT':__EVENTARGUMENT, 
			'__LASTFOCUS':__LASTFOCUS,
			'__VIEWSTATE':__VIEWSTATE,
			# '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			'__EVENTVALIDATION':__EVENTVALIDATION,
			'__ASYNCPOST':__ASYNCPOST,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision':division,
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict':district,
			'ctl00$ContentPlaceHolder1$SearchControl1$ddlEP':EP,
			'ctl00$ContentPlaceHolder1$SearchControl1$hdnElectionProgram':EP,
			'ctl00$ContentPlaceHolder1$SearchControl1$hdnLocalBody':hdnLocalBody[0],
			'ctl00$ContentPlaceHolder1$SearchControl1$DDLEDnumber':val
			} 
			url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
			headers = {'X-MicrosoftAjax': 'Delta=true',
			'ASP.NET_SessionId':'lkcm5tekxol32uxujtalve2i',
			'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
			request = FormRequest(url=url,formdata=payload_states,callback = self.parse_searchData,headers = headers,meta = {'localBody':localBody,'division':division,'district':district,"EP":EP,"EDN":val})
			yield request



			# __EVENTTARGET = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$btnSearch"
			# __EVENTARGUMENT = ""
			# __LASTFOCUS = ""
			# __VIEWSTATE= hidden_values.split("|")[16]
			# # __VIEWSTATEGENERATOR = hidden_values.split("|")[20]
			# __EVENTVALIDATION = hidden_values.split("|")[20]
			# localBody = response.meta["localBody"]
			# division = response.meta['division']
			# district = response.meta['district']
			# EP = response.meta['EP']
			# __ASYNCPOST = "true"
			# ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict"
			# payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,
			# '__EVENTTARGET':__EVENTTARGET, 
			# '__EVENTARGUMENT':__EVENTARGUMENT, 
			# '__LASTFOCUS':__LASTFOCUS,
			# '__VIEWSTATE':__VIEWSTATE,
			# # '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
			# '__EVENTVALIDATION':__EVENTVALIDATION,
			# '__ASYNCPOST':__ASYNCPOST,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision':division,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict':district,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$ddlEP':val,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$hdnElectionProgram':EP,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$hdnElectionProgram': EP,
			# 'ctl00$ContentPlaceHolder1$SearchControl1$hdnLocalBody':hdnLocalBody[0],
			# 'ctl00$ContentPlaceHolder1$SearchControl1$DDLEDnumber':val
			# } 
			# url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
			# headers = {'X-MicrosoftAjax': 'Delta=true',
			# 'ASP.NET_SessionId':'lkcm5tekxol32uxujtalve2i',
			# 'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
			# request = FormRequest(url=url,formdata=payload_states,callback = self.parse_searchData,headers = headers,meta = {'localBody':localBody,'division':division,'district':district,"EP":val})
			# yield request

	def parse_searchData(self,response):
		html = etree.HTML(response.body)
		hdnLocalBody = html.xpath("//input[@id='ContentPlaceHolder1_SearchControl1_hdnLocalBody']/@value")
		# # values = html.xpath("//select[@id='ContentPlaceHolder1_GVData']/tbody/tr[position() > 1]/td/text()")
		# # texts = html.xpath("//select[@id='ContentPlaceHolder1_GVData']/tbody/tr/option[position() > 1]/text()")

		matching = [s for s in response.body.split("\n") if "__VIEWSTATE" in s]
		hidden_values = matching[0]

		__EVENTTARGET = ""
		__EVENTARGUMENT = ""
		__LASTFOCUS = ""
		__VIEWSTATE= hidden_values.split("|")[16]
		# __VIEWSTATEGENERATOR = hidden_values.split("|")[20]
		__EVENTVALIDATION = hidden_values.split("|")[20]
		localBody = response.meta["localBody"]
		division = response.meta['division']
		district = response.meta['district']
		EP = response.meta['EP']
		EDN = response.meta['EDN']
		__ASYNCPOST = "true"
		ScriptManager1 = "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$btnSearch"
		payload_states = {'ctl00$ContentPlaceHolder1$ScriptManager1':ScriptManager1,
		'__EVENTTARGET':__EVENTTARGET, 
		'__EVENTARGUMENT':__EVENTARGUMENT, 
		'__LASTFOCUS':__LASTFOCUS,
		'__VIEWSTATE':__VIEWSTATE,
		# '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
		'__EVENTVALIDATION':__EVENTVALIDATION,
		'__ASYNCPOST':__ASYNCPOST,
		'ctl00$ContentPlaceHolder1$SearchControl1$DDLLocalBody':localBody,
		'ctl00$ContentPlaceHolder1$SearchControl1$DDLDivision':division,
		'ctl00$ContentPlaceHolder1$SearchControl1$DDLDistrict':district,
		'ctl00$ContentPlaceHolder1$SearchControl1$ddlEP':EP,
		'ctl00$ContentPlaceHolder1$SearchControl1$hdnElectionProgram':EP,
		'ctl00$ContentPlaceHolder1$SearchControl1$hdnLocalBody':hdnLocalBody[0],
		'ctl00$ContentPlaceHolder1$SearchControl1$DDLEDnumber':EDN,
		"ctl00$ContentPlaceHolder1$btnSearch":"Search"
		} 
		url = "https://panchayatelection.maharashtra.gov.in/MasterSearch.aspx"
		headers = {'X-MicrosoftAjax': 'Delta=true',
		'ASP.NET_SessionId':'lkcm5tekxol32uxujtalve2i',
		'X-Requested-With':'XMLHttpRequest',"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}
		request = FormRequest(url=url,formdata=payload_states,callback = self.parse_searchData1,headers = headers,meta = {'localBody':localBody,'division':division,'district':district,"EP":EP,"EDN":EDN})
		print("============================")
		print(payload_states)
		yield request

	def parse_searchData1(self,response):
		# print(response.body)
		html = etree.HTML(response.body)
		
		table =  html.xpath("//table[@id='ContentPlaceHolder1_GVData']")[0]

		for row in table.xpath(".//tr"):
			TDS = [td.text for td in row.xpath(".//td/span")]
			if TDS != []:
				item  = CrawlerItem()
				item['RegistrationNo'] = TDS[0]
				item['FULLNAME'] = TDS[1]
				item['NameofElectoralDivision'] = TDS[2]
				item['ElectoralDivisionID'] = TDS[3]
				item['element'] = "CANDIDATE_LIST"
				yield item
		




		

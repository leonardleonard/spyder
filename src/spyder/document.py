#coding=utf-8

import time
from pyquery import PyQuery as pq
from pybits import ansicolor
import re, urlparse
from db import Store
import _mysql
from fetch import Fetch
import feedparser

r"""
 getElementData(doc, "a", text)
	=> pq(doc.find("a").text())

	@href => getAttr
	#text => method

"""
def getElementData(obj, token):
	#parse token
	p = re.compile("(\w+?)\[([@|#])?(\w+)?\]");
	m = p.match(token);
	if m:
		tag, flag, val = m.groups() 
		d = pq(obj.find(tag))
		if flag == "@":
			return d.attr(val);
		elif flag == "#":
			#目前没找其他方法....
			return eval("d."+val+"()");

#Grab List
class Grab(object):
	def __init__(self, seed, savable = True):
		rule = seed.rule;
		self.seed = seed
		self.savable = savable
		self.type = seed.type

		self.items = {}
		if self.type == "feed":
			self.parseFeed();
			#rss, atom 都是标准, 所以直接提取即可
		else:
			self.listRule = rule.getListRule();
			self.listRule.setPrefixUrl(seed.prefixurl);
			self.prefixurl = seed.prefixurl;
			self.fetchPage();

		self.fetchArticles();

	def parseFeed(self):
		print "Start to fetch and parse Feed list"
		seed = self.seed
		doc = Fetch(seed.prefixurl, seed.charset, self.seed.timeout).read();
		feed = feedparser.parse(doc)
		items = feed["entries"]
		if len(items) > 0:
			for item in items:
				link = item["link"]
				title = item["title"]
				date = item["published"]
				self.items[link] = {
					"url" : link,
					"title" : title,
					"date" : date
				}

		print "List has finished parsing. It has %s docs." % ansicolor.red(len(self.items.items()));

	def fetchPage(self):
		print "Start to fetch and parse List"
		listUrls = self.listRule.getFormatedUrls();
		for url in listUrls:
			doc = Fetch(url, self.seed.charset, self.seed.timeout).read()
			if doc:
				self.parserHtml(doc)
		
		print "List has finished parsing. It has %s docs." % ansicolor.red(len(self.items.items()));
	
	def fetchArticles(self):
		if len(self.items.items()) > 0:
			for url in self.items:
				self.items[url]["article"] = Document(url, self.seed, self.savable)
	
	def parserHtml(self, doc):
		doc = pq(doc);
		list = doc.find(self.listRule.getListParent());
		if list:
			def entry(i, e):
				#link
				url = self.listRule.getItemLink()
				link = getElementData(e, url)
				link = urlparse.urljoin(self.prefixurl, link);

				#title
				title = getElementData(e, self.listRule.getItemTitle());

				#date
				dateparent = self.listRule.getItemDate();
				date = None
				if dateparent:
					date = getElementData(e, self.listRule.getItemDate());


				self.items[link] = {
					"url" : link,
					"title" : title,
					"date" : date
				}

			list(self.listRule.getEntryItem()).map(entry)

class Document(object):
	def __init__(self, url, seed, savable = True):
		self.url = url;
		self.articleRule = seed.rule.getArticleRule();

		self.content = ""
		self.pages   = []
		self.contentData = {}
		self.sid = seed.sid
		self.savable = savable
		self.filterscript = self.articleRule.filterscript
		

		if self.checkUrl(url) == False:
			print "Document %s is fetcing" % ansicolor.green(url)
			self.firstPage = Fetch(url, seed.charset, seed.timeout).read();
			self.parse(self.firstPage, True)
			self.contentData["content"] = self.content

			if self.saveArticle() > 0:
				print ansicolor.green(self.url) + " saved!"
		else:
			print "Document %s has exists." % ansicolor.red(url)

	def checkUrl(self, url):
		#check url in articles
		return Store("SELECT aid FROM spyder.articles WHERE url='%s'" % self.url).is_exists()

	def saveArticle(self):
		content = ""
		title = ""
		tags = ""
		author = ""
		date = ""

		if "content" in self.contentData:
			if not self.content:
				return
			content = content.strip();
			content = (self.contentData["content"]).encode("utf-8", "ignore")
			content = _mysql.escape_string( content )

		if "title" in self.contentData:
			title = self.contentData["title"].strip()
			title = _mysql.escape_string(title.encode("utf-8", "ignore"))

		self.url = self.url.encode("utf-8", "ignore")

		sql = "INSERT INTO spyder.articles (title, content, url, sid, status, fetchtime) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (title, content, self.url, str(self.sid), "0", str(int(time.time())))
		
		if not self.savable:
			return

		return Store(sql).insert_id()

	def getContentData(self):
		return self.contentData

	def parse(self, doc, first=False):
		doc = pq(doc);
		article = doc.find(self.articleRule.getWrapParent())

		def getContent():
			if not article:
				return
			content = article(self.articleRule.getContentParent())
			if content:
				#filter
				if self.filterscript:
					content = content.remove("script");
				
				content = content.html();
				if content:
					self.content = self.content +  content

		if first:
			#need parse pages, title, tags
			####title
			self.contentData["title"] = getElementData(article, self.articleRule.getTitleParent())

			#pages
			self.parsePage(article)
			#get content
			getContent();
			article = None #fetch over

			for purl in self.pages:
				self.parse(purl)

		#context
		#_context = article("div[class='contF']").remove("script").remove('p[align="right"]')
		getContent();
		#print self.content

	def parsePage(self, doc):
		p = self.articleRule.getPageParent()
		if len(p) == 0:
			return
		pages = doc.find(p)

		if len(pages) > 0:
			for p in pages:
				p = pq(p)
				url = p.attr("href")
				if not url:
					continue
				linkText = p.text().strip()
				if re.match(r"[0-9]+?", linkText):
					#filter javascript
					if re.match(r"javascript", url) == None:
						url = urlparse.urljoin(self.url, url)
						self.pages.append(url)


if __name__ == "__main__":
	r"""
	html, RSS, Atom, Ajax
	"""
	#test rss
	doc = Fetch("http://www.265g.com/api/feed.php", "gb2312", 300).read()
	import feedparser
	feed = feedparser.parse(doc)
	#print feed["encoding"] # encoding?
	#print feed["version"] # rss20, atom?

	items = feed["entries"]
	if len(items) > 0:
		for item in items:
			# get title, href, date
			print item["title"], item["link"], item["published"]

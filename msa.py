import httplib2
import os.path
import lxml.etree
import lxml.html
import lxml.cssselect
import re

class WikiPage(object):
    def get_xml_url(self):
        self.xml_url = 'http://en.wikipedia.org/w/api.php?action=parse&prop=text&page=%s&format=xml' % (self.title,)

    def get_xml_filename(self):
        self.xml_filename = self.title + '.xml'

    def download_xml(self):
        self.get_xml_url()
        h = httplib2.Http()
        headers = {"Accept": "application/xml"}
        resp, xml = h.request(self.xml_url, headers=headers)
        with open(self.xml_filename, 'w') as f:
            f.write(xml)

    def get_xml(self):
        self.get_xml_filename()
        if not os.path.exists(self.xml_filename):
            self.download_xml()
        with open(self.xml_filename) as f:
            self.xml = f.read()

    def get_xml_tree(self):
        self.get_xml()
        utf8_parser = lxml.etree.XMLParser(encoding='utf-8')
        self.xml_tree = lxml.etree.fromstring(self.xml, parser=utf8_parser)

    def get_html(self):
        self.get_xml_tree()
        self.html = self.xml_tree.xpath('//text')[0].text

    def get_html_tree(self):
        self.get_html()
        utf8_parser = lxml.html.HTMLParser(encoding='utf-8')
        self.html_tree = lxml.html.fromstring(self.html, parser=utf8_parser)

class MSA(WikiPage):
    title = 'Table_of_United_States_Metropolitan_Statistical_Areas'
    count = 50

    def get_table(self):
        self.get_html_tree()
        sortable_select = lxml.cssselect.CSSSelector('table.sortable')
        self.table = sortable_select(self.html_tree)[0]

    def get_all_data(self):
        self.get_table()
        self.all_data = []
        for tr in self.table.xpath('.//tr'):
            td = tr.xpath('.//td')
            if len(td) > 2:
                area = {}
                area['rank'] = int(''.join(td[0].xpath('text()')))
                area['name'] = ''.join(td[1].xpath('a/text()'))
                self.all_data.append(area)

    def get_data(self):
        self.get_all_data()
        self.data = self.all_data[:self.count]
                
    def build(self):
        self.get_data()

class Regions(WikiPage):
    title = "List_of_regions_of_the_United_States"

    def get_ul(self):
        self.get_html_tree()
        ul_select = lxml.cssselect.CSSSelector('ul:contains("Region 1")')
        self.ul = ul_select(self.html_tree)[0]

    def get_data(self):
        self.get_ul()
        self.data = []
        for region_li in self.ul.xpath('./li'):
            region = {}
            region["name"] = region_li.xpath('.//a/text()')[0]
            region["divisions"] = []
            for division_li in region_li.xpath('.//li'):
                division = {}
                division["name"] = division_li.xpath('.//a/text()')[0]
                division["states"] = division_li.xpath('.//a/text()')[1:]
                region["divisions"].append(division)
            self.data.append(region)

    def build(self):
        self.get_data()

class Abbreviations(WikiPage):
    pass

if __name__ == "__main__":
    msa = MSA()
    msa.build()
    print msa.data
    regions = Regions()
    regions.build()
    print regions.data

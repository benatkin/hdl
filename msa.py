import httplib2
import os.path
import lxml.etree
import lxml.html
import lxml.cssselect
import re
import json

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

    def build(self):
        self.get_data()

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

class Abbreviations(WikiPage):
    title = "List_of_U.S._state_abbreviations"
    state_column = 0
    usps_column = 1
    last_usps = 'WY'

    def get_table(self):
        self.get_html_tree()
        table_select = lxml.cssselect.CSSSelector('table:contains("FIPS")')
        self.table = table_select(self.html_tree)[0]

    def get_data(self):
        self.get_table()
        self.data = {}
        for abbr_tr in self.table.xpath('./tr'):
            col_td = abbr_tr.xpath('./td')
            if len(col_td) > self.usps_column:
                abbr = {}
                abbr['usps'] = col_td[self.usps_column].xpath('./text()')[0]
                abbr['state'] = col_td[self.state_column].xpath('.//a/text()')[0]
                self.data[abbr['usps']] = abbr['state']
                if abbr['usps'] == self.last_usps:
                    break

class MSAOutline(object):
    msa_re = re.compile(r'(\S+)\s*MSA\s*$')
    region_for_state = {}

    def get_msa(self):
        msa = MSA()
        msa.build()
        self.msa = msa.data

    def get_regions(self):
        regions = Regions()
        regions.build()
        self.regions = regions.data

    def get_abbreviations(self):
        abbreviations = Abbreviations()
        abbreviations.build()
        self.abbreviations = abbreviations.data
    
    def add_states_to_msa(self):
        for area in self.msa:
            area["states"] = []
            for abbr in self.msa_re.search(area["name"]).group(1).split("-"):
                area["states"].append(self.abbreviations[abbr])

    def build_region_for_state(self):
        self.region_for_state = {}
        for region in self.regions:
            for division in region["divisions"]:
                for state in division["states"]:
                    self.region_for_state[state] = region["name"]

    def build_outline(self):
        outline = {}
        for msa in self.msa:
            state = msa["states"][0]
            region = self.region_for_state[state]
            if not region in outline:
                outline[region] = {}
            if not state in outline[region]:
                outline[region][state] = []
            outline[region][state].append("%s (%d)" % (msa["name"], msa["rank"]))
            self.outline = outline
        self.outline = [(region["name"], outline[region["name"]]) for region in self.regions]

    def render_row(self, level, text):
        return "    " * level + "*   " + text + "\n"

    def render_outline(self):
        self.markdown = self.render_row(0, "Metropolitain Statistical Areas")
        for region in self.outline:
            self.markdown += self.render_row(1, region[0])
            states = region[1].keys()
            states.sort()
            for state in states:
                self.markdown += self.render_row(2, state)
                for msa in region[1][state]:
                    self.markdown += self.render_row(3, msa)

    def get_data(self):
        self.get_msa()
        self.get_regions()
        self.get_abbreviations()
        self.add_states_to_msa()
        self.build_region_for_state()
        self.build_outline()
        self.render_outline()
        self.data = {}
        self.data["msa"] = self.msa
        self.data["regions"] = self.regions
        self.data["abbreviations"] = self.abbreviations
        self.data["region_for_state"] = self.region_for_state
        self.data["outline"] = self.outline

    def build(self):
        self.get_data()

if __name__ == "__main__":
    print '-- data --'
    msa_outline = MSAOutline()
    msa_outline.build()
    print '-- json --'
    print json.dumps(msa_outline.data, indent=2, sort_keys=True)
    print
    print '-- markdown --'
    print msa_outline.markdown

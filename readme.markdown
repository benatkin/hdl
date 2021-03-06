# Introduction

*Hoisting* and *Deep Linking* are a couple of related software terms I've
encountered recently. They both help large documents behave like smaller
documents.

# Hoisting

I learned about hoisting about a year ago when I encountered outliners.com in
Dave Winer's sidebar. Hoisting is taking one node of an outline and making it
the root node of a view. It dates back until the 80s, and still shows up
today, usually under different names.

## City Example

As an example, I'll use an unordered list, of the 50
[largest metropolitain areas in the U. S., by state](http://en.wikipedia.org/wiki/Table_of_United_States_Metropolitan_Statistical_Areas).
Some of these metro areas are spread across states; I'll use the state which
has most of the metro's people living in it, which is conveniently listed
first. To add an additional level, I've broken these into regions.

*   Metropolitain Statistical Areas
    *   Northeast
        *   Connecticut
            *   Hartford-West Hartford-East Hartford, CT MSA (45)
        *   Massachusetts
            *   Boston-Cambridge-Quincy, MA-NH MSA (10)
        *   New York
            *   New York-Northern New Jersey-Long Island, NY-NJ-PA MSA (1)
            *   Buffalo-Niagara Falls, NY MSA (50)
        *   Pennsylvania
            *   Philadelphia-Camden-Wilmington, PA-NJ-DE-MD MSA (5)
            *   Pittsburgh, PA MSA (22)
        *   Rhode Island
            *   Providence-New Bedford-Fall River, RI-MA MSA (37)
    *   Midwest
        *   Illinois
            *   Chicago-Joliet-Naperville, IL-IN-WI MSA (3)
        *   Indiana
            *   Indianapolis-Carmel, IN MSA (34)
        *   Michigan
            *   Detroit-Warren-Livonia, MI MSA (11)
        *   Minnesota
            *   Minneapolis-St. Paul-Bloomington, MN-WI MSA (16)
        *   Missouri
            *   St. Louis, MO-IL MSA (18)
            *   Kansas City, MO-KS MSA (29)
        *   Ohio
            *   Cincinnati-Middletown, OH-KY-IN MSA (24)
            *   Cleveland-Elyria-Mentor, OH MSA (26)
            *   Columbus, OH MSA (32)
        *   Wisconsin
            *   Milwaukee-Waukesha-West Allis, WI MSA (39)
    *   South
        *   Alabama
            *   Birmingham-Hoover, AL MSA (47)
        *   District of Columbia
            *   Washington-Arlington-Alexandria, DC-VA-MD-WV MSA (8)
        *   Florida
            *   Miami-Fort Lauderdale-Pompano Beach, FL MSA (7)
            *   Tampa-St. Petersburg-Clearwater, FL MSA (19)
            *   Orlando-Kissimmee-Sanford, FL MSA (27)
            *   Jacksonville, FL MSA (40)
        *   Georgia
            *   Atlanta-Sandy Springs-Marietta, GA MSA (9)
        *   Kentucky
            *   Louisville/Jefferson County, KY-IN MSA (42)
        *   Louisiana
            *   New Orleans-Metairie-Kenner, LA MSA (46)
        *   Maryland
            *   Baltimore-Towson, MD MSA (20)
        *   North Carolina
            *   Charlotte-Gastonia-Rock Hill, NC-SC MSA (33)
            *   Raleigh-Cary, NC MSA (49)
        *   Oklahoma
            *   Oklahoma City, OK MSA (44)
        *   Tennessee
            *   Nashville-Davidson–Murfreesboro–Franklin, TN MSA (38)
            *   Memphis, TN-MS-AR MSA (41)
        *   Texas
            *   Dallas-Fort Worth-Arlington, TX MSA (4)
            *   Houston-Sugar Land-Baytown, TX MSA (6)
            *   San Antonio-New Braunfels, TX MSA (28)
            *   Austin-Round Rock-San Marcos, TX MSA (35)
        *   Virginia
            *   Virginia Beach-Norfolk-Newport News, VA-NC MSA (36)
            *   Richmond, VA MSA (43)
    *   West
        *   Arizona
            *   Phoenix-Mesa-Glendale, AZ MSA (12)
        *   California
            *   Los Angeles-Long Beach-Santa Ana, CA MSA (2)
            *   San Francisco-Oakland-Fremont, CA MSA (13)
            *   Riverside-San Bernardino-Ontario, CA MSA (14)
            *   San Diego-Carlsbad-San Marcos, CA MSA (17)
            *   Sacramento–Arden-Arcade–Roseville, CA MSA (25)
            *   San Jose-Sunnyvale-Santa Clara, CA MSA (31)
        *   Colorado
            *   Denver-Aurora-Broomfield, CO MSA (21)
        *   Nevada
            *   Las Vegas-Paradise, NV MSA (30)
        *   Oregon
            *   Portland-Vancouver-Hillsboro, OR-WA MSA (23)
        *   Utah
            *   Salt Lake City, UT MSA (48)
        *   Washington
            *   Seattle-Tacoma-Bellevue, WA MSA (15)

This is a lot of information. The outline is a bit unweildly if I just
want to see which MSAs in Florida are in the top 50 in the country. If I
just wanted that, information, I could make a new outline with the root
at Florida. Or, better yet, I could keep the same outline, but just
view Florida and its children. In outliner parlance, this is called
*hoisting*.

The previous outline, with the *Florida* node hoisted, looks like this:

*   Florida
    *   Miami-Fort Lauderdale-Pompano Beach, FL MSA (7)
    *   Tampa-St. Petersburg-Clearwater, FL MSA (19)
    *   Orlando-Kissimmee-Sanford, FL MSA (27)
    *   Jacksonville, FL MSA (40)

# Deep Linking

I read about the term Deep Linking a few days ago when a 
[NYTimes article about a new open source project](http://open.blogs.nytimes.com/2011/01/11/emphasis-update-and-source/#h[WtEIyw,2]) got 
[posted to Hacker News](http://news.ycombinator.com/item?id=2093820).

After looking further, there are several things deep linking can mean:

*   Linking to an individual page or image within a site, rather than
    the hope page. This is [the meaning on Wikipedia](http://en.wikipedia.org/wiki/Deep_linking),
    but it's not what this page is about.
*   Linking to a section within a page using anchor tags. This is fairly
    common. It's supported on Wikipedia through a MediaWiki feature that
    [generates anchor tags and a table of contents for pages](http://en.wikibooks.org/wiki/MediaWiki_User_Guide/Sections_and_Headings#Headings_not_in_TOC).
*   Linking to some content using a fancy tool like the [NYTimes deep linking
    project, Emphasis.](https://github.com/NYTimes/Emphasis)

The middle one, the facility Wikipedia has, is the one I've used the
most. I've found it very useful for linking to Wikipedia. It would
be nice if it was supported on markdown documents on GitHub, like this
one.

## In This Document

github doesn't put anchors in markdown headers, and neither do most
markdown libraries. Python's Markdown library has an extension for it,
though. It replaces a \[TOC\] token with a ul containing a table of
contents, and generates anchors. The extension is included; after
running `pip install Markdown`, the following code can be run to convert
this page's markdown to HTML with a table of contents:

    import markdown
    import codecs

    HTML_START = """
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Hoisting and Deep Linking</title>
    </head>
    <body>
    """.lstrip()

    HTML_END = """
    </body>
    </html>
    """

    class IndexPage(object):
        md_filename = 'readme.markdown'
        html_filename = 'index.html'

        def read_md(self):
            with codecs.open(self.md_filename, mode="r", encoding="utf8") as f:
                self.md = f.read()

        def render(self):
            self.read_md()
            self.md = "\[TOC\]\n\n" + self.md
            md = markdown.Markdown(extensions=['toc'])
            return HTML_START + md.convert(self.md) + HTML_END

        def write_html(self):
            with codecs.open(self.html_filename, mode="w", encoding="utf8") as f:
                f.write(self.render())

    if __name__ == '__main__':
        IndexPage().write_html()

Using the Table of Contents, a section, for example the [City
Example](http://benatkin.github.com/hdl/#city-example), can be linked to.

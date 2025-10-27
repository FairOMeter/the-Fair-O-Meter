import requests
from xml.etree import ElementTree as ET

YEARS_RANGE = range(2023, 2025)
DBLP_SOURCES = [f"https://dblp.org/search/publ/api?q=toc%3Adb/conf/ecai/ecai{year}.bht%3A&h=1000&format=xml" for year in YEARS_RANGE]


for source in DBLP_SOURCES:
    print(f"Fetching papers from: {source}")
    # Opening XML and reading 
    # Papers are represented as <hit> elements in the XML
    # <results> / <hits> / <hit>

    response = requests.get(source)
    if response.status_code == 200:
        xml_content = response.content
        root = ET.fromstring(xml_content)

        hits = root.find('hits')
        if hits is not None:
            for hit in hits.findall('hit'):
                info = hit.find('info')
                if info is not None:
                    authors = info.find('authors')
                    if authors is not None:
                        author_names = [author.text for author in authors.findall('author')]
                        print("Authors:", author_names)

                else:
                    print("No info found for this hit.")
        else:
            print("No hits found in the XML.")

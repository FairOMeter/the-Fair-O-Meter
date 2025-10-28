import re
import requests
from xml.etree import ElementTree as ET

YEARS_RANGE = range(2000, 2025)

def scrape_papers(year: int) -> None:
    source = f"https://dblp.org/search/publ/api?q=toc%3Adb/conf/ecai/ecai{year}.bht%3A&h=1000&format=xml"
    source_alt = f"https://dblp.org/search/publ/api?q=toc%3Adb/conf/ijcai/ijcai{year}.bht%3A&h=1000&format=xml"
    print(f"Fetching papers published in {year} from: '{source}'")
    # Opening XML and reading 
    # Papers are represented as <hit> elements in the XML
    # <results> / <hits> / <hit>

    response = requests.get(source)
    response_alt = requests.get(source_alt)
    
    xml_content = response.content
    xml_content_alt = response_alt.content

    root = ET.fromstring(xml_content)
    root_alt = ET.fromstring(xml_content_alt)

    hits = root.find('hits')
    hits_alt = root_alt.find('hits')

    papers = hits.findall('hit') if hits is not None else []
    papers_alt = hits_alt.findall('hit') if hits_alt is not None else []

    if len(papers) == 0 and len(papers_alt) > 0:
        print(f"No papers found for year {year} in primary source, switching to alternative source.")
        papers = papers_alt

    if len(papers) == 0:
        print(f"No papers found for year {year} in both sources.")
        return
    else:
        print(f"Found {len(papers)} papers published in {year}.")

        authors_names = set()

        for hit in papers:
            info = hit.find('info')
            if info is not None:
                authors = info.find('authors')
                if authors is not None:
                    author_names = [author.text for author in authors.findall('author')]

                    # Collect unique author names by adding every name to a set
                    for name in author_names:
                        authors_names.add(name)

            else:
                print("No info found for this hit.")

        print(f"Total unique authors in {year}: {len(authors_names)}")

        # For every year, we print every author name into a CSV file
        with open(f"data/ecai_authors_{year}.csv", "w", encoding="utf-8") as f:

            # But before we should clean every name that has a four-digit number in it (to avoid including paper IDs)
            def clean_name_from_digits(name):
                return re.sub(r'[0-9]+', '', name).strip()

            authors_names = list(map(clean_name_from_digits, authors_names))

            f.write("author_name\n")
            for name in authors_names:
                f.write(f"{name}\n")

def main() -> None:
    for year in YEARS_RANGE:
        scrape_papers(year)

if __name__ == "__main__":
    main()
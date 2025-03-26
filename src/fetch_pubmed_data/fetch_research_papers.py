# import argparse
# import requests
# import xml.etree.ElementTree as ET
# import csv
# import re
# from typing import List, Dict, Optional

# def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[str]:
#     """Fetch research papers from PubMed based on a query."""
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     params = {
#         "db": "pubmed",
#         "term": query,
#         "retmax": max_results,
#         "retmode": "xml"
#     }
#     response = requests.get(base_url, params=params)
#     if response.status_code != 200:
#         raise Exception("Error fetching data from PubMed")

#     root = ET.fromstring(response.content)

#     pmids: List[str] = [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text]
    
#     return pmids

# def fetch_paper_details(pmids: List[str]) -> ET.Element:
#     """Fetch paper details from PubMed given a list of PMIDs."""
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
#     params = {
#         "db": "pubmed",
#         "id": ",".join(pmids),
#         "retmode": "xml"
#     }

#     response = requests.get(base_url, params=params)
#     if response.status_code != 200:
#         raise Exception("Error fetching paper details from PubMed")

#     return ET.fromstring(response.content)

# def extract_papers_with_industry_affiliations(root: ET.Element) -> List[Dict[str, str]]:
#     """Extract papers where at least one author is affiliated with a pharmaceutical or biotech company."""
#     papers: List[Dict[str, str]] = []

#     for article in root.findall(".//PubmedArticle"):
#         title_elem = article.find(".//ArticleTitle")
#         title: str = title_elem.text if title_elem is not None else "N/A"

#         pmid_elem = article.find(".//PMID")
#         pmid: str = pmid_elem.text if pmid_elem is not None else "N/A"

#         year_elem = article.find(".//PubDate/Year")
#         pub_year: str = year_elem.text if year_elem is not None else ""
#         month_elem = article.find(".//PubDate/Month")
#         pub_month: str = month_elem.text if month_elem is not None else ""
#         day_elem = article.find(".//PubDate/Day")
#         pub_day: str = day_elem.text if day_elem is not None else ""

#         pub_date: str = "Not available" if not (pub_day or pub_month or pub_year) else f"{pub_day} {pub_month} {pub_year}"

#         affiliations: List[str] = [aff.text for aff in article.findall(".//AffiliationInfo/Affiliation") if aff.text]

#         non_academic_author: str = "Unknown"
#         corresponding_author_email: str = "Unknown"

#         for author in article.findall(".//Author"):
#             last_name_elem = author.find("LastName")
#             fore_name_elem = author.find("ForeName")
#             author_name: str = (
#                 f"{fore_name_elem.text} {last_name_elem.text}"
#                 if fore_name_elem is not None and last_name_elem is not None
#                 else "Unknown"
#             )

#             for aff in author.findall(".//AffiliationInfo/Affiliation"):
#                 aff_text: str = aff.text.strip() if aff.text else ""

#                 if "@" in aff_text:
#                     email_match: Optional[re.Match] = re.search(r"\s([^ ]+@[^ ]+)\s", f" {aff_text} ")
#                     corresponding_author_email = email_match.group(1).strip() if email_match else aff_text

#                     non_academic_author = author_name
#                     break  

#         papers.append({
#             "PubmedID": pmid,
#             "Title": title,
#             "Publication Date": pub_date,
#             "Non-academic Author": non_academic_author,
#             "Corresponding Author Email": corresponding_author_email,
#             "Company Affiliation(s)": "; ".join(affiliations),
#         })

#     return papers

# def save_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
#     """Save research papers to a CSV file."""
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=[
#             "PubmedID", "Title", "Publication Date", "Non-academic Author", "Corresponding Author Email", "Company Affiliation(s)"
#         ])
#         writer.writeheader()
#         writer.writerows(papers)
    
#     print(f"Saved {len(papers)} papers to {filename}")

# def main() -> None:
#     parser = argparse.ArgumentParser(description="Fetch research papers from PubMed and filter those with pharmaceutical/biotech affiliations.")
#     parser.add_argument("query", type=str, help="Search query for PubMed")
#     parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
#     parser.add_argument("-f", "--file", type=str, help="Filename to save the results. If not specified, prints output to console.")
    
#     args = parser.parse_args()

#     if args.debug:
#         print("Fetching PubMed papers...")

#     pmids: List[str] = fetch_pubmed_papers(args.query)

#     if not pmids:
#         print("No papers found.")
#         return

#     root: ET.Element = fetch_paper_details(pmids)

#     papers: List[Dict[str, str]] = extract_papers_with_industry_affiliations(root)

#     if papers:
#         if args.file:
#             save_to_csv(papers, args.file)
#         else:
#             for paper in papers:
#                 print(paper)
#     else:
#         print("No papers found with industry affiliations.")

# if __name__ == "__main__":
#     main()

import requests
import xml.etree.ElementTree as ET
import csv
import re
from typing import List, Dict, Optional

def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[str]:
    """Fetch research papers from PubMed based on a query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    return [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text]

def fetch_paper_details(pmids: List[str]) -> ET.Element:
    """Fetch paper details from PubMed given a list of PMIDs."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    return ET.fromstring(response.content)

def extract_papers_with_industry_affiliations(root: ET.Element) -> List[Dict[str, str]]:
    """Extract papers where at least one author is affiliated with a pharmaceutical or biotech company."""
    papers: List[Dict[str, str]] = []

    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="N/A")
        pmid = article.findtext(".//PMID", default="N/A")
        
        year = article.findtext(".//PubDate/Year", default="")
        month = article.findtext(".//PubDate/Month", default="")
        day = article.findtext(".//PubDate/Day", default="")
        pub_date = f"{day} {month} {year}".strip() if year or month or day else "Not available"

        affiliations: List[str] = [aff.text for aff in article.findall(".//AffiliationInfo/Affiliation") if aff.text]

        non_academic_author = "Unknown"
        corresponding_author_email = "Unknown"

        for author in article.findall(".//Author"):
            last_name = author.findtext("LastName", default="Unknown")
            fore_name = author.findtext("ForeName", default="")
            author_name = f"{fore_name} {last_name}".strip()

            for aff in author.findall(".//AffiliationInfo/Affiliation"):
                aff_text = aff.text.strip() if aff.text else ""

                if "@" in aff_text:
                    email_match: Optional[re.Match] = re.search(r"\s([^ ]+@[^ ]+)\s", f" {aff_text} ")
                    corresponding_author_email = email_match.group(1).strip() if email_match else aff_text
                    non_academic_author = author_name
                    break  

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author": non_academic_author,
            "Corresponding Author Email": corresponding_author_email,
            "Company Affiliation(s)": "; ".join(affiliations),
        })

    return papers

def save_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
    """Save research papers to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID", "Title", "Publication Date", "Non-academic Author", "Corresponding Author Email", "Company Affiliation(s)"
        ])
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Saved {len(papers)} papers to {filename}")


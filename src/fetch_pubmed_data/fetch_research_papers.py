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


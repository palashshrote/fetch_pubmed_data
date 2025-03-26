import argparse
import requests
import xml.etree.ElementTree as ET
import csv
import re


def fetch_pubmed_papers(query, max_results=10):
    """Fetch research papers from PubMed based on a query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching data from PubMed")

    root = ET.fromstring(response.content)

    pmids = [id_elem.text for id_elem in root.findall(".//Id")]

    return pmids

def fetch_paper_details(pmids):
    """Fetch paper details from PubMed given a list of PMIDs."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching paper details from PubMed")
    return ET.fromstring(response.content)

def extract_papers_with_industry_affiliations(root):
    """Extract papers where at least one author is affiliated with a pharmaceutical or biotech company."""
    papers = []
    # keywords = ["pharmaceutical", "biotech", "biopharma", "drug", "therapeutics"]

    for article in root.findall(".//PubmedArticle"):
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "N/A"
        pmid_elem = article.find(".//PMID")
        pmid = pmid_elem.text if pmid_elem is not None else "N/A"

        year_elem = article.find(".//PubDate/Year")
        pub_year = year_elem.text if year_elem is not None else ""
        month_elem = article.find(".//PubDate/Month")
        pub_month = month_elem.text if month_elem is not None else ""
        day_elem = article.find(".//PubDate/Day")
        pub_day = day_elem.text if day_elem is not None else ""
        if pub_day == "" and pub_month == "" and pub_year == "":
            pub_date = "Not available"
        else:
            pub_date = pub_day + " " + pub_month + " " + pub_year

        affiliations = [aff.text for aff in article.findall(".//AffiliationInfo/Affiliation") if aff.text]
        # authors = [author.text for author in article.findall(".//Author/LastName") if author.text]
        # firstName = [author.text for author in article.findall(".//Author/ForeName") if author.text]
        non_academic_author = "Unknown"
        corresponding_author_email = "Unknown"  # PubMed doesn't always provide emails

        for author in article.findall(".//Author"):
            last_name_elem = author.find("LastName")
            fore_name_elem = author.find("ForeName")
            author_name = (
                f"{fore_name_elem.text} {last_name_elem.text}"
                if fore_name_elem is not None and last_name_elem is not None
                else "Unknown"
            )

            for aff in author.findall(".//AffiliationInfo/Affiliation"):
                aff_text = aff.text.strip() if aff.text else ""

                if "@" in aff_text:
                    # Extract the email by finding spaces around it
                    email_match = re.search(r"\s([^ ]+@[^ ]+)\s", f" {aff_text} ")
                    if email_match:
                        corresponding_author_email = email_match.group(1).strip()
                    else:
                        corresponding_author_email = aff_text  # Fallback to full text if spaces not found

                    non_academic_author = author_name
                    break  # Stop searching once we find an email

        # company_affiliations = [aff for aff in affiliations if any(keyword in aff.lower() for keyword in keywords)]
        # non_academic_authors = [
        #     authors[i] for i, aff in enumerate(affiliations)
        #     if i < len(authors) and any(keyword in aff.lower() for keyword in keywords)
        # ]

        # if company_affiliations:
        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            # "Non-academic Author(s)": "; ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Non-academic Author": non_academic_author,
            "Corresponding Author Email": corresponding_author_email,
            "Company Affiliation(s)": "; ".join(affiliations),

        })

    return papers

def save_to_csv(papers, filename):
    """Save research papers to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID", "Title", "Publication Date", "Non-academic Author", "Corresponding Author Email","Company Affiliation(s)"
        ])
        writer.writeheader()
        writer.writerows(papers)
    print(f"Saved {len(papers)} papers to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed and filter those with pharmaceutical/biotech affiliations.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str,
                        help="Filename to save the results. If not specified, prints output to console.")
    args = parser.parse_args()
    print(args)

    if args.debug:
        print("Fetching PubMed papers...")

    pmids = fetch_pubmed_papers(args.query)
    print(pmids)
    if not pmids:
        print("No papers found.")
        return

    root = fetch_paper_details(pmids)
    print(root)



    papers = extract_papers_with_industry_affiliations(root)

    if papers:
        if args.file:
            save_to_csv(papers, args.file)
        else:
            for paper in papers:
                print(paper)
    else:
        print("No papers found with industry affiliations.")


if __name__ == "__main__":
    main()
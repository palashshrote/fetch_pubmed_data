import argparse
from src.fetch_pubmed_data.fetch_research_papers import fetch_pubmed_papers, fetch_paper_details, extract_papers_with_industry_affiliations, save_to_csv 
from typing import List, Dict

def fetch_data() -> None:
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed and filter those with pharmaceutical/biotech affiliations.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results. If not specified, prints output to console.")
    parser.add_argument("-m", "--max-results", type=int, default=10, help="Maximum number of results to fetch from PubMed")
    
    args = parser.parse_args()

    if args.debug:
        print(f"Fetching PubMed papers for query: {args.query}")

    pmids: List[str] = fetch_pubmed_papers(args.query, max_results=args.max_results)

    if not pmids:
        print("No papers found.")
        return

    if args.debug:
        print(f"Found PMIDs: {pmids}")

    root = fetch_paper_details(pmids)
    papers: List[Dict[str, str]] = extract_papers_with_industry_affiliations(root)

    if papers:
        if args.file:
            save_to_csv(papers, args.file)
        else:
            for paper in papers:
                print(paper)
    else:
        print("No papers found with industry affiliations.")

if __name__ == "__main__":
    fetch_data()

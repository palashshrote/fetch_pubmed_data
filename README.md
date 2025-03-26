# PubMed Research Papers Fetcher

## Overview

This Python project provides a robust tool to fetch research papers from PubMed using NCBI's E-utilities API. The application allows users to search for research papers, retrieve detailed information, and export the results to a CSV file.

## Background

[PubMed](https://pubmed.ncbi.nlm.nih.gov/) is a free resource maintained by the National Center for Biotechnology Information (NCBI), hosting millions of biomedical and life sciences research papers. The project leverages NCBI's E-utilities public API to efficiently search and retrieve research paper information.

## Key Features

- Search research papers using flexible query terms
- Retrieve comprehensive paper details
- Export results to CSV
- Debug mode for troubleshooting
- Lightweight and easy to use

## Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) package manager
- Internet connection

## Installation

1. Install Poetry
```bash
pip install poetry
```

2. Clone the repository
```bash
git clone https://github.com/yourusername/fetch_research_papers.git
cd fetch_research_papers
```

3. Configure Poetry (Optional but Recommended)
```bash
# Set virtual environment in project directory
poetry config virtualenvs.in-project true

# Install dependencies
poetry install
```

## Usage Examples

### Basic Search
```bash
# Search for papers about diabetes drug
poetry run python src/fetch_pubmed_data/fetch_research_papers.py "diabetes drug"
```

### Export to CSV
```bash
# Save results to info.csv
poetry run python src/fetch_pubmed_data/fetch_research_papers.py "diabetes drug" -f info.csv
```

### Debug Mode
```bash
# Enable verbose debugging
poetry run python src/fetch_pubmed_data/fetch_research_papers.py "diabetes drug" -d
```

## Program Workflow

### 1. Search API
- Retrieves list of Unique Identifiers (UIDs) matching the query
- Endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- Example Query: `term="diabetes drug", db="pubmed"`

### 2. Downloading API
- Fetches document summaries for input UIDs
- Endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

### 3. Data Extraction
- Parses XML response
- Extracts relevant information:
  - PubMed ID
  - Article Title
  - Publication Date
  - Authors
- Stores data in CSV format

## Dependencies

- `requests`: HTTP library for API calls
- `argparse`: Command-line argument parsing
- `xml.etree.ElementTree`: XML parsing

## Limitations and Considerations

- Respects NCBI's usage guidelines
- Rate-limited by NCBI
- Requires stable internet connection

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- [PubMed E-utilities Documentation](https://eutils.ncbi.nlm.nih.gov/)
- AI Tools (ChatGPT, Claude) for debugging assistance
- Poetry for dependency management


## Contact
- Name: Palash Shrote
- Email: palash.shrote.58@gmail.com
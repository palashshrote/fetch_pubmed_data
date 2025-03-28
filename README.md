# 🔬 Research Papers Data Extractor

## 📝 Overview

A powerful Python tool designed to efficiently extract and analyze research papers from PubMed using NCBI's E-utilities API. This application empowers researchers, academics, and data enthusiasts to:
- Search research papers with precise query terms
- Retrieve comprehensive paper details
- Export results seamlessly to CSV
- Debug and track search processes

## 🌐 Background

[PubMed](https://pubmed.ncbi.nlm.nih.gov/), maintained by the National Center for Biotechnology Information (NCBI), is a comprehensive free resource hosting millions of biomedical and life sciences research papers. This project leverages NCBI's E-utilities public API to provide programmatic access to this vast scientific knowledge repository.

## ✨ Key Features

- 🔍 Flexible and precise paper searching
- 📊 Comprehensive paper information retrieval
- 💾 Effortless CSV export
- 🐞 Integrated debug mode
- 🚀 Lightweight and user-friendly design

## 🛠 Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) package manager

## 💻 Installation

1. Clone the repository
```bash
git clone https://github.com/palashshrote/fetch_research_papers.git
cd fetch_research_papers
```

2. Configure Poetry (Recommended)
```bash
# Install project dependencies
poetry install
```

## 🚀 Usage Examples

### Basic Search
```bash
# Search for papers about diabetes drug
poetry run get-papers-list "diabetes drug"
```

### Export to CSV
```bash
# Save results to info.csv
poetry run get-papers-list "diabetes drug" -f info.csv
```

### Debug Mode
```bash
# Enable verbose debugging
poetry run get-papers-list "diabetes drug" -d
```

## 🔬 Program Workflow

### 1. Search API
- **Purpose**: Retrieve Unique Identifiers (UIDs) matching search query
- **Endpoint**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- **Example Query**: `term="diabetes drug", db="pubmed"`

### 2. Downloading API
- **Purpose**: Fetch document summaries for input UIDs
- **Endpoint**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

### 3. Data Extraction
- **Process**:
  - Parse XML response
  - Extract detailed information:
    - PubMed ID
    - Article Title
    - Publication Date
    - Authors (Non academic) and corresponding email
    - Company Affiliation(s)
- **Output**: Structured CSV file

## 📦 Dependencies

- `requests`: Robust HTTP library for API calls
- `argparse`: Flexible command-line argument parsing
- `xml.etree.ElementTree`: Efficient XML parsing

## ⚠️ Limitations and Considerations

- Adheres to NCBI's usage guidelines
- Subject to NCBI's rate limiting
- Requires stable internet connection
- Dependent on PubMed's XML structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🙏 Acknowledgments

- [PubMed E-utilities Documentation](https://eutils.ncbi.nlm.nih.gov/)
- AI Assistants (ChatGPT, Claude) for debugging support
- Poetry for elegant dependency management

## 📞 Contact

- **Name**: Palash Shrote
- **Email**: palash.shrote.58@gmail.com

---

**Disclaimer**: This tool is designed for research and academic purposes. Please use responsibly and respect scientific community guidelines.
# 🔬 Research Papers Data Extractor

## 📝 Overview

A powerful Python tool designed to streamline research paper discovery from PubMed, leveraging NCBI's E-utilities API. This lightweight application enables researchers, academics, and data enthusiasts to:
- Search research papers with flexible query terms
- Retrieve comprehensive paper details
- Export results directly to CSV
- Debug and track search processes

## 🌐 Background

[PubMed](https://pubmed.ncbi.nlm.nih.gov/), maintained by the National Center for Biotechnology Information (NCBI), is a free, comprehensive database housing millions of biomedical and life sciences research papers. Our project harnesses NCBI's E-utilities public API to provide efficient, programmatic access to this vast repository of scientific knowledge.

## ✨ Key Features

- 🔍 Flexible paper searching capabilities
- 📊 Comprehensive paper information retrieval
- 💾 Seamless CSV export functionality
- 🐞 Integrated debug mode
- 🚀 Lightweight and user-friendly design

## 🛠 Prerequisites

- Python 3.8+
- Poetry (recommended for dependency management)
- Internet connection

## 💻 Installation

### Installation from TestPyPI

```bash
# Install from TestPyPI with dependencies from PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fetch-pubmed-data
```

## 🚀 Usage Examples
### Create a new python file (for ex- app.py)

### Basic Search
```bash
# Search for papers about diabetes drug
python app.py "diabetes drug"
```

### Export to CSV
```bash
# Save results to info.csv
python app.py "diabetes drug" -f info.csv
```

### Debug Mode
```bash
# Enable verbose debugging
python app.py "diabetes drug" -d
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

## ⚠️ Limitations and Considerations

- Adheres to NCBI's usage guidelines
- Subject to NCBI's rate limiting
- Requires stable internet connection
- Dependent on PubMed's XML structure

## 🙏 Acknowledgments

- [PubMed E-utilities Documentation](https://eutils.ncbi.nlm.nih.gov/)
- AI Assistants (ChatGPT, Claude) for debugging support
- Poetry for elegant dependency management

## 📞 Contact

- **Name**: Palash Shrote
- **Email**: palash.shrote.58@gmail.com
- **GitHub**: https://github.com/palashshrote

---

**Disclaimer**: This tool is designed for research and academic purposes. Please use responsibly and respect scientific community guidelines.
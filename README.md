This "fetch_papers" contains python program to fetch research papers from "PubMed", and stores the relevant information in info.csv file.

PubMed is a Entrez db comes under NCBI Entrez system.

E-utilities are the public API to access PubMed.

Procedure 
1. Basic searching API - It retrieve list of UID matching the query.
   
   Let's say we want to search for the articles about diabetes drug.

   query/term = "diabetes drug", db = "pubmed"

   API - https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=diabetes%2Bdrug

   Result = [40127974,40127847,...]


2. Basic Downloading API - Returns document summaries (DocSums) for a list of input UIDs, and saving the result in root variable.

   API - https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&term=diabetes%2Bdrug&id=40127974,40127847


3. Data extraction from XML and saving into .CSV - "root" contains PubmedArticleSet, running a loop for each article and using find/findall method to extract the relevant data and storing it in dict such as pubmed ID, title ...

   and storing the dict for each article in a list "papers" will give us relevant information, which we can store in a info.csv file